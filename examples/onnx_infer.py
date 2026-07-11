"""Minimal Supertonic-ZH Mandarin inference — pure ONNX Runtime (no PyTorch).

The Mandarin model ships as fused / optimized ONNX graphs, gated on Hugging
Face: https://huggingface.co/dove88/supertonic-zh (request access).

Put these in an ONNX dir (default: ./onnx):
    text_encoder_zh.onnx  duration_predictor_zh.onnx  vector_estimator_zh.onnx   (gated HF repo)
    vocoder.onnx                                                                 (upstream Supertone/supertonic-3)
    unicode_indexer_zh.json   voice_zh.json                                      (gated HF repo)

Run:
    pip install onnxruntime numpy soundfile
    python examples/onnx_infer.py "今天天气很好，我们一起去公园散步吧。"
"""
import json
import math
import sys
import unicodedata

import numpy as np
import onnxruntime as ort
import soundfile as sf

SR = 44100
FRAME = 512 * 6            # samples per latent frame
LATENT_DIM = 144          # 24 * 6
TOTAL_STEP = 16
SPEED = 1.05
ONNX_DIR = "onnx"


def _sess(path):
    o = ort.SessionOptions()
    o.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    return ort.InferenceSession(path, o, providers=["CPUExecutionProvider"])


def tokenize_zh(text, indexer):
    text = unicodedata.normalize("NFKC", text).replace(" ", "")
    if not text or text[-1] not in "。！？；：，、）】":
        text += "。"
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


def synthesize(text, onnx_dir=ONNX_DIR):
    te = _sess(f"{onnx_dir}/text_encoder_zh.onnx")
    dp = _sess(f"{onnx_dir}/duration_predictor_zh.onnx")
    ve = _sess(f"{onnx_dir}/vector_estimator_zh.onnx")
    voc = _sess(f"{onnx_dir}/vocoder.onnx")
    indexer = json.load(open(f"{onnx_dir}/unicode_indexer_zh.json"))
    style_ttl, style_dp = load_style(f"{onnx_dir}/voice_zh.json")

    text_ids, text_mask = tokenize_zh(text, indexer)
    text_emb = te.run(None, {"text_ids": text_ids, "style_ttl": style_ttl,
                             "text_mask": text_mask})[0]
    dur = dp.run(None, {"text_ids": text_ids, "style_dp": style_dp,
                        "text_mask": text_mask})[0]
    dur_sec = max(float(dur.reshape(-1)[0]) / SPEED, 0.1)
    L = max(1, math.ceil(dur_sec * SR / FRAME))

    latent_mask = np.ones((1, 1, L), np.float32)
    xt = np.random.randn(1, LATENT_DIM, L).astype(np.float32) * latent_mask
    tot = np.full(1, float(TOTAL_STEP), np.float32)
    for step in range(TOTAL_STEP):
        xt = ve.run(None, {"noisy_latent": xt, "text_emb": text_emb,
                           "style_ttl": style_ttl, "latent_mask": latent_mask,
                           "text_mask": text_mask,
                           "current_step": np.full(1, float(step), np.float32),
                           "total_step": tot})[0]
    wav = voc.run(None, {"latent": xt})[0]
    return wav.reshape(-1), SR


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "今天天气很好，我们一起去公园散步吧。"
    wav, sr = synthesize(text)
    sf.write("out.wav", wav, sr)
    print(f"wrote out.wav ({len(wav)/sr:.2f}s) for: {text}")
