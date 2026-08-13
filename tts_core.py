"""Shared pure-ONNX inference core for Supertonic-ZH (no PyTorch).

Used by examples/onnx_infer.py (one-shot) and streaming_tts.py (chunked).
Expects in onnx_dir: text_encoder_zh.onnx, duration_predictor_zh.onnx,
vector_estimator_zh.onnx, vocoder.onnx, unicode_indexer_zh.json, voice_zh.json
(vocoder/voice paths overridable).
"""
import json
import math
import unicodedata

import numpy as np
import onnxruntime as ort

SR = 44100
FRAME = 512 * 6            # samples per latent frame
LATENT_DIM = 144           # 24 * 6


def _sess(path, providers=None):
    o = ort.SessionOptions()
    o.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    return ort.InferenceSession(path, o, providers=providers or ["CPUExecutionProvider"])


def tokenize_zh(text, indexer, terminator="。"):
    text = unicodedata.normalize("NFKC", text).replace(" ", "")
    # NFKC maps fullwidth ？！，：； to ASCII, so the ender check must accept
    # both forms or comma/question-terminated chunks would grow a spurious 。
    if text and text[-1] not in "。！？；：，、）】,.!?;:)]":
        text += terminator
    s = f"<zh>{text}</zh>"
    ids = [indexer[ord(c)] for c in s if ord(c) < len(indexer) and indexer[ord(c)] != -1]
    ids = np.array([ids], dtype=np.int64)
    mask = np.ones((1, 1, ids.shape[1]), np.float32)
    return ids, mask


def load_style(path):
    d = json.load(open(path))
    ttl = np.array(d["style_ttl"]["data"], np.float32).reshape(d["style_ttl"]["dims"])
    dp = np.array(d["style_dp"]["data"], np.float32).reshape(d["style_dp"]["dims"])
    return ttl, dp


class TTSCore:
    """Holds the four ONNX sessions + one voice; synthesizes one text chunk."""

    def __init__(self, onnx_dir, voice_path=None, vocoder_path=None, providers=None):
        self.te = _sess(f"{onnx_dir}/text_encoder_zh.onnx", providers)
        self.dp = _sess(f"{onnx_dir}/duration_predictor_zh.onnx", providers)
        self.ve = _sess(f"{onnx_dir}/vector_estimator_zh.onnx", providers)
        self.voc = _sess(vocoder_path or f"{onnx_dir}/vocoder.onnx", providers)
        self.indexer = json.load(open(f"{onnx_dir}/unicode_indexer_zh.json"))
        self.style_ttl, self.style_dp = load_style(voice_path or f"{onnx_dir}/voice_zh.json")

    def indexable_ratio(self, text):
        if not text:
            return 0.0
        ok = sum(1 for c in text
                 if ord(c) < len(self.indexer) and self.indexer[ord(c)] != -1)
        return ok / len(text)

    def synthesize(self, text, total_step=16, speed=1.05, terminator="。",
                   cancel=None, seed=None):
        text_ids, text_mask = tokenize_zh(text, self.indexer, terminator)
        if text_ids.shape[1] == 0:
            return np.zeros(0, np.float32)
        text_emb = self.te.run(None, {"text_ids": text_ids, "style_ttl": self.style_ttl,
                                      "text_mask": text_mask})[0]
        dur = self.dp.run(None, {"text_ids": text_ids, "style_dp": self.style_dp,
                                 "text_mask": text_mask})[0]
        dur_sec = float(dur.reshape(-1)[0]) / speed
        # lower clamp (degenerate short) + upper sanity clamp (~3x a 0.25 s/char
        # speaking-rate heuristic; guards the repeat/drop runaway mode)
        dur_sec = min(max(dur_sec, 0.1), max(1.0, 0.75 * len(text)))
        L = max(1, math.ceil(dur_sec * SR / FRAME))

        latent_mask = np.ones((1, 1, L), np.float32)
        rng = np.random.default_rng(seed)
        xt = rng.standard_normal((1, LATENT_DIM, L)).astype(np.float32) * latent_mask
        tot = np.full(1, float(total_step), np.float32)
        for step in range(total_step):
            if cancel is not None and cancel.is_set():
                return np.zeros(0, np.float32)
            xt = self.ve.run(None, {"noisy_latent": xt, "text_emb": text_emb,
                                    "style_ttl": self.style_ttl,
                                    "latent_mask": latent_mask,
                                    "text_mask": text_mask,
                                    "current_step": np.full(1, float(step), np.float32),
                                    "total_step": tot})[0]
        wav = self.voc.run(None, {"latent": xt})[0]
        return wav.reshape(-1).astype(np.float32)
