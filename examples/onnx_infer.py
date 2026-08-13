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
import os
import sys

import soundfile as sf

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from tts_core import SR, TTSCore  # noqa: E402

TOTAL_STEP = 16
SPEED = 1.05
ONNX_DIR = "onnx"


def synthesize(text, onnx_dir=ONNX_DIR):
    core = TTSCore(onnx_dir)
    wav = core.synthesize(text, total_step=TOTAL_STEP, speed=SPEED)
    return wav, SR


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "今天天气很好，我们一起去公园散步吧。"
    wav, sr = synthesize(text)
    sf.write("out.wav", wav, sr)
    print(f"wrote out.wav ({len(wav)/sr:.2f}s) for: {text}")
