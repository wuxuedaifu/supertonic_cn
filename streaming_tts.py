"""Streaming synthesis for Supertonic-ZH — inference-layer chunked streaming.

Incremental text (e.g. an LLM token stream) is cut at clause boundaries,
each clause is synthesized with the frozen ONNX pipeline (tts_core.TTSCore),
and audio chunks are emitted while later text is still arriving.
Design: docs/superpowers/specs/2026-08-13-streaming-synthesis-design.md
(private monorepo).
"""
from dataclasses import dataclass, field
import queue
import threading
import numpy as np


def _default_silence():
    return {"、": 80, "，": 150, ",": 150, "：": 150, ":": 150,
            "；": 200, ";": 200, "": 0}


@dataclass
class StreamConfig:
    hard_boundaries: str = "。！？；…\n.!?;"
    soft_boundaries: str = "，、：,:"
    soft_min_chars: int = 8
    first_chunk_soft_min: int = 6
    max_chunk_chars: int = 30
    forced_split_terminator: str = "，"
    crossfade_ms: int = 30
    silence_ms: dict = field(default_factory=_default_silence)
    hard_silence_ms: int = 300          # any punct not in silence_ms
    first_chunk_total_step: int = 16
    total_step: int = 16
    speed: float = 1.05


@dataclass
class Clause:
    text: str
    punct: str
    forced: bool = False


class TextAccumulator:
    """Cuts an incremental text stream into synthesizable clauses."""

    def __init__(self, config=None):
        self.cfg = config or StreamConfig()
        self.buf = ""
        self.first_done = False

    def feed(self, piece):
        out = []
        for ch in piece:
            self.buf += ch
            clause = self._maybe_cut(ch)
            if clause is not None:
                out.append(clause)
        return out

    def flush(self):
        text = self.buf.strip()
        self.buf = ""
        if not text:
            return None
        punct = text[-1] if text[-1] in (self.cfg.hard_boundaries
                                         + self.cfg.soft_boundaries) else ""
        self.first_done = True
        return Clause(text, punct)

    # -- internals ----------------------------------------------------------
    def _emit(self, punct, forced=False):
        text = self.buf.strip()
        self.buf = ""
        if not text or not text.strip(self.cfg.hard_boundaries
                                      + self.cfg.soft_boundaries + " \n"):
            return None                  # nothing pronounceable
        self.first_done = True
        return Clause(text, punct, forced)

    def _maybe_cut(self, ch):
        cfg = self.cfg
        if ch in cfg.hard_boundaries:
            return self._emit(ch)
        if ch in cfg.soft_boundaries:
            need = cfg.soft_min_chars if self.first_done else cfg.first_chunk_soft_min
            if len(self.buf) >= need:
                return self._emit(ch)
            return None
        if len(self.buf) > cfg.max_chunk_chars:
            return self._forced_split()
        return None

    def _forced_split(self):
        b = self.buf
        cut = None
        for i in range(len(b) - 1, -1, -1):  # include index 0: leading CJK before long ASCII is a valid cut
            if b[i] == " ":
                cut = i                  # cut at the space, drop it
                break
            if not (b[i].isascii() and b[i].isalnum()):
                cut = i + 1              # cut after a CJK / non-alnum char
                break
        if cut is None or cut == 0:
            cut = self.cfg.max_chunk_chars   # one giant ASCII run: hard cut
        head, self.buf = b[:cut].strip(), b[cut:].lstrip(" ")
        if not head:
            return None
        self.first_done = True
        return Clause(head, "", forced=True)


def trim_trailing_silence(wav, sr, threshold=1e-3, keep_ms=50):
    """Drop the padded tail so no dead air lands inside a sentence."""
    if wav.size == 0:
        return wav
    keep = int(sr * keep_ms / 1000)
    idx = np.nonzero(np.abs(wav) > threshold)[0]
    if idx.size == 0:
        return wav[:keep]
    return wav[: min(wav.size, int(idx[-1]) + keep)]


def apply_fades(wav, sr, fade_ms):
    """Cosine fade-in/out; kills seam clicks even across silence gaps."""
    n = min(int(sr * fade_ms / 1000), wav.size // 2)
    if n <= 0:
        return wav
    t = np.linspace(0.0, np.pi / 2, n, dtype=np.float32)
    out = wav.copy()
    out[:n] *= np.sin(t)
    out[-n:] *= np.cos(t)
    return out


class AudioJoiner:
    """Per-chunk post-processing: trim, level-match, fade, punctuation gap."""

    def __init__(self, config, sr=44100):
        self.cfg = config
        self.sr = sr
        self._rms_avg = None

    def process(self, wav, punct):
        if wav.size == 0:
            return wav
        wav = trim_trailing_silence(wav, self.sr)
        wav = self._match_rms(wav)
        wav = apply_fades(wav, self.sr, self.cfg.crossfade_ms)
        gap_ms = self.cfg.silence_ms.get(punct, self.cfg.hard_silence_ms)
        gap = int(self.sr * gap_ms / 1000)
        if gap:
            wav = np.concatenate([wav, np.zeros(gap, np.float32)])
        return wav

    def _match_rms(self, wav):
        rms = float(np.sqrt(np.mean(wav ** 2)))
        if rms < 1e-6:
            return wav
        if self._rms_avg is None:
            self._rms_avg = rms
            return wav
        gain = float(np.clip(self._rms_avg / rms, 0.7, 1.4))
        out = (wav * gain).astype(np.float32)
        self._rms_avg = 0.8 * self._rms_avg + 0.2 * rms * gain
        return out


class StreamingTTS:
    """Streaming facade: text pieces in -> processed audio chunks out.

    Pull-based: the consumer's iteration pace is the back-pressure, no
    unbounded buffering. One active stream per instance; a new synthesize()
    call is a new turn and resets any previous cancel().
    """

    def __init__(self, onnx_dir=None, voice_path=None, vocoder_path=None,
                 config=None, core=None, on_chunk_error=None, providers=None):
        self.cfg = config or StreamConfig()
        if core is None:
            if onnx_dir is None:
                raise ValueError("onnx_dir is required when no core is injected")
            from tts_core import TTSCore
            core = TTSCore(onnx_dir, voice_path, vocoder_path, providers)
        self.core = core
        self.on_chunk_error = on_chunk_error
        self._cancel = threading.Event()
        self._active = False

    def cancel(self):
        self._cancel.set()

    def synthesize(self, text_iter):
        if self._active:
            raise RuntimeError("a stream is already active on this instance")
        self._active = True
        self._cancel.clear()
        try:
            acc = TextAccumulator(self.cfg)
            joiner = AudioJoiner(self.cfg)
            first = True
            for piece in text_iter:
                if self._cancel.is_set():
                    return
                for clause in acc.feed(piece):
                    wav = self._synth_clause(clause, first)
                    if self._cancel.is_set():
                        return
                    if wav is not None and wav.size:
                        first = False
                        yield joiner.process(wav, clause.punct)
            if not self._cancel.is_set():
                clause = acc.flush()
                if clause is not None:
                    wav = self._synth_clause(clause, first)
                    if wav is not None and wav.size:
                        yield joiner.process(wav, clause.punct)
        finally:
            self._active = False

    async def asynthesize(self, text_aiter):
        """Async adapter over synthesize(): bridges an async text iterator
        through a worker thread. Cancellation: call cancel() as usual."""
        import asyncio

        loop = asyncio.get_running_loop()
        text_q = queue.Queue()
        audio_q = asyncio.Queue()
        _DONE = object()

        def _text_gen():
            while True:
                item = text_q.get()
                if item is _DONE:
                    return
                yield item

        def _worker():
            try:
                for pcm in self.synthesize(_text_gen()):
                    loop.call_soon_threadsafe(audio_q.put_nowait, pcm)
            except BaseException as exc:  # surfaced to the async consumer
                loop.call_soon_threadsafe(audio_q.put_nowait, exc)
            finally:
                loop.call_soon_threadsafe(audio_q.put_nowait, _DONE)

        async def _feeder():
            try:
                async for piece in text_aiter:
                    text_q.put(piece)
            except asyncio.CancelledError:
                raise
            except BaseException as exc:
                audio_q.put_nowait(exc)   # surface text-source errors to consumer
            finally:
                text_q.put(_DONE)

        worker = threading.Thread(target=_worker, daemon=True)
        worker.start()
        feeder = asyncio.ensure_future(_feeder())
        try:
            while True:
                item = await audio_q.get()
                if item is _DONE:
                    break
                if isinstance(item, BaseException):
                    raise item
                yield item
        finally:
            feeder.cancel()
            self._cancel.set()       # unblocks the worker if the consumer bailed
            text_q.put(_DONE)        # unblocks _text_gen if it is waiting
            # never block the event loop on cleanup: join off-loop
            await loop.run_in_executor(None, worker.join, 5)

    def _synth_clause(self, clause, first):
        # Rate indexability on the text minus edge punctuation: boundary
        # marks are always indexable, so a punctuation-only clause (e.g. a
        # lone "，" left over at flush) would otherwise score 1.0 and reach
        # the ONNX core. indexable_ratio("") is 0.0 -> correctly skipped.
        text_for_indexing = clause.text.strip(self.cfg.hard_boundaries + self.cfg.soft_boundaries)
        if self.core.indexable_ratio(text_for_indexing) < 0.5:
            return None                      # mostly un-synthesizable: skip
        steps = self.cfg.first_chunk_total_step if first else self.cfg.total_step
        term = self.cfg.forced_split_terminator if clause.forced else "。"
        try:
            return self.core.synthesize(clause.text, total_step=steps,
                                        speed=self.cfg.speed, terminator=term,
                                        cancel=self._cancel)
        except Exception as exc:             # skip bad chunk, keep the stream alive
            if self.on_chunk_error is not None:
                self.on_chunk_error(clause.text, exc)
            return None
