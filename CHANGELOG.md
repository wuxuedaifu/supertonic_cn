# Changelog

All notable changes to the Supertonic-ZH public preview are documented in
this file.

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
