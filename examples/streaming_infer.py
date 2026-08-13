"""Supertonic-ZH streaming synthesis demo — pure ONNX Runtime.

Simulates an LLM emitting text word-by-word; audio chunks stream out while
"generation" is still in progress. Writes out_stream.wav and prints the
first-audio latency.

Put the model files in an ONNX dir (default: ./onnx) — same layout as
examples/onnx_infer.py — then:

    python examples/streaming_infer.py "你好呀！今天有什么可以帮你的吗？我们可以聊聊天气。"
"""
import os
import sys
import time

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from streaming_tts import StreamingTTS  # noqa: E402
from tts_core import SR  # noqa: E402

ONNX_DIR = "onnx"


def fake_llm_stream(text, piece_chars=3, delay_s=0.04):
    """Stand-in for an LLM token stream: a few characters at a time."""
    for i in range(0, len(text), piece_chars):
        yield text[i:i + piece_chars]
        time.sleep(delay_s)


def main():
    text = sys.argv[1] if len(sys.argv) > 1 else \
        "你好呀！今天有什么可以帮你的吗？我们可以聊聊天气，也可以聊聊别的。"
    tts = StreamingTTS(onnx_dir=ONNX_DIR)

    t0 = time.perf_counter()
    first_at = None
    chunks = []
    for pcm in tts.synthesize(fake_llm_stream(text)):
        if first_at is None:
            first_at = time.perf_counter() - t0
            print(f"first audio after {first_at * 1000:.0f} ms")
        chunks.append(pcm)
        print(f"  chunk {len(chunks)}: {pcm.size / SR:.2f}s")

    wav = np.concatenate(chunks) if chunks else np.zeros(0, np.float32)
    sf.write("out_stream.wav", wav, SR)
    print(f"wrote out_stream.wav ({wav.size / SR:.2f}s) for: {text}")


if __name__ == "__main__":
    main()
