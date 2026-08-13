# Changelog

All notable changes to the Supertonic-ZH public preview are documented in
this file.

## v0.2.0 — 2026-08-13

Streaming synthesis (Stage 1).

- New `streaming_tts.py` module: incremental text in, low-latency streamed
  PCM audio out, built on the same frozen ONNX graphs used by
  `examples/onnx_infer.py` — no model changes. Text is cut at clause
  boundaries as it arrives (e.g. from an LLM), so audio for earlier clauses
  streams out while later text is still being generated.
- Barge-in support via `StreamingTTS.cancel()`; an async variant
  `asynthesize()` is available for async LLM SDKs.
- New demo: [`examples/streaming_infer.py`](examples/streaming_infer.py).
- New benchmark section in [`BENCHMARK.md`](BENCHMARK.md#streaming-stage-1):
  first-audio latency 245 ms median (A100 GPU, 16 steps) / 757 ms (CPU,
  8 steps), vs a 609 ms whole-utterance GPU baseline; barge-in latency ~6-7 ms
  median. GPU numbers require creating the CUDA session with
  `cudnn_conv_algo_search: "HEURISTIC"` — the default exhaustive search
  re-tunes kernels per clause length and adds ~800 ms.
- Inference-only change: no model weights, graphs, or training data are
  affected.

## v0.1.0-preview (2026-07-11)

First public preview release.

- Mandarin Chinese (`zh`) text-to-speech built on frozen, unmodified
  upstream Supertonic-3, distributed as optimized / fused ONNX graphs that
  run in pure ONNX Runtime.
- Text normalization for numbers, dates, money, percentages, and phone
  numbers (read as spoken Chinese).
- Benchmark results published in [`BENCHMARK.md`](BENCHMARK.md): CER, RTF,
  latency, footprint, drop rate, with a per-category CER breakdown and an
  explicit honesty note about the Whisper-small ASR judge and the
  deliberately hard test set.
- Audio demos published in [`demo/`](demo/README.md): seven languages
  (Mandarin, English, Russian, Arabic, French, Japanese, Korean) plus
  seven hard Chinese text categories (date, English acronym, long text,
  money, percent, polyphone, rare character).
- A minimal, self-contained ONNX-runtime inference example
  ([`examples/onnx_infer.py`](examples/onnx_infer.py)).
- **Model weights are not publicly distributed** — available on request
  under an evaluation license. The current build is **non-commercial use
  only** (Baker/CSMSC-encumbered training data); commercial licensing is
  available separately for a Baker-free build. The demos and benchmark in
  this release were produced with this model, so quality can be evaluated
  without holding the weights.
- Synthesizes in a single preset voice (style-embedding JSON,
  `assets/F1.json`); custom-voice cloning is out of scope for this preview.
- **Known limitations:** residual high-frequency artifact from the frozen
  vocoder; Chinese⇄English code-switching is currently unreliable; tone /
  polyphone / erhua accuracy are model-inherent; single preset voice only.
