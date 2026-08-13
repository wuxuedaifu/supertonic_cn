"""Streaming synthesis benchmark: first-audio latency, barge-in latency,
and A/B listening wav generation (streaming vs one-shot).

    python public-preview/benchmark/run_streaming_benchmark.py \
        --onnx-dir onnx \
        --vocoder onnx/vocoder.onnx [--gpu] [--steps 16 8] [--ab-dir eval/streaming_ab]
"""
import argparse
import os
import statistics
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from streaming_tts import StreamConfig, StreamingTTS  # noqa: E402
from tts_core import SR, TTSCore  # noqa: E402

DIALOGUE = [
    "你好呀！今天有什么可以帮你的吗？",
    "好的，我来帮你查一下明天的天气。",
    "这个问题有点复杂，我们一步一步来分析。",
    "没问题，订单已经提交成功了，请注意查收短信。",
    "抱歉让你久等了，刚才系统有点慢。",
    "我觉得这个方案可行，不过还有两个细节要确认。",
    "现在是北京时间下午三点二十分。",
    "这个模型叫SuperTonic，它在CPU上也跑得很快。",
    "如果你还有其他问题，随时告诉我。",
    "祝你今天过得愉快，再见！",
]


def bench_first_audio(onnx_dir, vocoder, providers, steps, n_warm=1):
    cfg = StreamConfig(first_chunk_total_step=steps, total_step=steps)
    tts = StreamingTTS(onnx_dir=onnx_dir, vocoder_path=vocoder,
                       config=cfg, providers=providers)
    lat = []
    for i, text in enumerate(DIALOGUE):
        t0 = time.perf_counter()
        gen = tts.synthesize(iter([text]))     # text available instantly
        next(gen)
        dt = (time.perf_counter() - t0) * 1000
        for _ in gen:
            pass
        if i >= n_warm:                        # drop session warm-up runs
            lat.append(dt)
    return lat


def bench_barge_in(onnx_dir, vocoder, providers):
    tts = StreamingTTS(onnx_dir=onnx_dir, vocoder_path=vocoder, providers=providers)
    long_text = "这是一段很长的话，" * 8 + "结束了。"
    results = []
    for _ in range(3):
        gen = tts.synthesize(iter([long_text]))
        next(gen)                              # synthesis is mid-flight
        t0 = time.perf_counter()
        tts.cancel()
        for _ in gen:
            pass                               # drain to full stop
        results.append((time.perf_counter() - t0) * 1000)
    return results


def gen_ab_wavs(onnx_dir, vocoder, providers, out_dir):
    import soundfile as sf
    os.makedirs(out_dir, exist_ok=True)
    core = TTSCore(onnx_dir, vocoder_path=vocoder, providers=providers)
    tts = StreamingTTS(core=core, config=StreamConfig())
    for i, text in enumerate(DIALOGUE):
        one = core.synthesize(text)
        chunks = list(tts.synthesize(iter([text])))
        sf.write(f"{out_dir}/{i:02d}_oneshot.wav", one, SR)
        sf.write(f"{out_dir}/{i:02d}_stream.wav",
                 np.concatenate(chunks) if chunks else np.zeros(1, np.float32), SR)
    print(f"A/B pairs written to {out_dir}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--onnx-dir", default="onnx")
    ap.add_argument("--vocoder", default="onnx/vocoder.onnx")
    ap.add_argument("--gpu", action="store_true")
    ap.add_argument("--steps", nargs="+", type=int, default=[16, 8])
    ap.add_argument("--ab-dir", default=None)
    args = ap.parse_args()
    # HEURISTIC conv-algo search matters: the CUDA EP default (EXHAUSTIVE)
    # re-benchmarks cuDNN kernels for every new input shape, and streaming
    # produces a new latent length per clause — ~800ms of pure search cost
    # on the first-audio path (measured: 1073ms -> ~245ms median @16 steps).
    providers = ([("CUDAExecutionProvider",
                   {"cudnn_conv_algo_search": "HEURISTIC"}),
                  "CPUExecutionProvider"]
                 if args.gpu else ["CPUExecutionProvider"])
    dev = "gpu" if args.gpu else "cpu"

    print(f"| Metric ({dev}) | Value |\n|---|---|")
    for steps in args.steps:
        lat = bench_first_audio(args.onnx_dir, args.vocoder, providers, steps)
        print(f"| First-audio latency, {steps} steps (median ms) "
              f"| {statistics.median(lat):.0f} |")
        print(f"| First-audio latency, {steps} steps (p95 ms) "
              f"| {sorted(lat)[int(0.95 * (len(lat) - 1))]:.0f} |")
    bi = bench_barge_in(args.onnx_dir, args.vocoder, providers)
    print(f"| Barge-in latency (median ms) | {statistics.median(bi):.0f} |")
    if args.ab_dir:
        gen_ab_wavs(args.onnx_dir, args.vocoder, providers, args.ab_dir)


if __name__ == "__main__":
    main()
