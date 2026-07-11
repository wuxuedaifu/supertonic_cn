<div align="center">

# 🗣️ Supertonic-ZH

### Bring **Mandarin Chinese** to the on-device Supertonic TTS family

**English** · [简体中文](README.zh.md)

<br>

[![status](https://img.shields.io/badge/status-public%20preview-blueviolet)](CHANGELOG.md)
[![license](https://img.shields.io/badge/code-MIT-green)](LICENSE)
[![build](https://img.shields.io/badge/current%20build-non--commercial-red)](LICENSE)
[![python](https://img.shields.io/badge/python-3.11-blue)](requirements.txt)
[![HF Model](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-model-yellow)](https://huggingface.co/dove88/supertonic-zh)

<em>Native Mandarin · numbers · dates · money · lightweight · fast · on-device.</em>

</div>

---

> **⚠️ Unofficial Mandarin extension · built on Supertonic-3.** Supertonic-ZH is an independent Mandarin extension built on the publicly released Supertonic-3 model. `v0.1.0-preview` · 2026-07-11.

## ✨ Why Supertonic-ZH?

The official **Supertonic-3** is a fast, lightweight, on-device TTS family — but out of the box it **does not synthesize Mandarin Chinese**. Supertonic-ZH closes that gap: a Mandarin fine-tune distributed as **optimized, fused ONNX graphs** that run in **pure ONNX Runtime**, on top of the **frozen, unmodified** upstream vocoder.

<div align="center">

| ❌ Official Supertonic-3 | ✅ Supertonic-ZH |
|---|---|
| No Mandarin synthesis | Intelligible native Mandarin |
| Reads "12,580.60元" digit-by-digit | Normalizes dates / money / % / phone to spoken Chinese |
| — | Public benchmark · reproducible test set |

</div>

## 🚀 Highlights

- 🈶 **Native Mandarin** in a consistent **preset voice** — tones, polyphones, 儿化, neutral tone, 一/不 sandhi.
- 🔢 **Smart text normalization** — dates, money, percentages, phone numbers, and full-width punctuation are read the way a person would.
- ⚡ **Fast** — ~**10× real-time** generation on GPU (RTF ≈ 0.10). See [`BENCHMARK.md`](BENCHMARK.md).
- 🪶 **Lightweight** — small footprint, built for on-device / offline / low-latency use.
- 🧊 **Vocoder untouched** — the four upstream Supertonic-3 ONNX graphs are used **frozen**; nothing about the base model is degraded.
- 🔎 **Honest & reproducible** — a public 100-sentence test set and the exact CER numbers behind it are both included.

## 🎧 Listen

Retained multilingual output from the frozen base model, plus native Mandarin from the fine-tune — click ▶️ to play:

| Language | Text | Audio |
|---|---|---|
| 🇨🇳 Mandarin | 今天天气很好，我们一起去公园散步吧。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_mandarin.wav) |
| 🇬🇧 English | The quick brown fox jumps over the lazy dog. | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_english.wav) |
| 🇷🇺 Russian | Сегодня прекрасная погода, давайте прогуляемся в парке. | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_russian.wav) |
| 🇸🇦 Arabic | الطقس جميل اليوم، دعونا نذهب في نزهة。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_arabic.wav) |
| 🇫🇷 French | Il fait très beau aujourd'hui, allons nous promener dans le parc. | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_french.wav) |
| 🇯🇵 Japanese | 今日はいい天気ですね、公園を散歩しましょう。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_japanese.wav) |
| 🇰🇷 Korean | 오늘 날씨가 좋네요, 공원을 산책합시다. | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_korean.wav) |

Seven more samples across the hardest Chinese text categories (date, English acronym, long text, money, percent, polyphone, rare character) are in [`demo/`](demo/README.md):

| Category | Text | Audio |
|---|---|---|
| Date | 会议定在2026年8月15日上午举行。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/date.wav) |
| English acronym | 训练模型需要用到GPU加速。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/en_acronym.wav) |
| Long text | 这次旅行我们先去了西安看兵马俑，又去了敦煌欣赏壁画，最后到了张掖看七彩丹霞，一路上风景美不胜收。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/long_text.wav) |
| Money | 这件外套售价12,580.60元。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/money.wav) |
| Percent | 今年公司营收增长了23.7%。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/percent.wav) |
| Polyphone | 他去银行取钱，然后在路上行走回家。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/polyphone.wav) |
| Rare character | 他觉得这件事有点囧，不知道怎么解释。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/rare_char.wav) |

> ▶️ opens the audio on GitHub's raw content host and plays in your browser.

## 📊 Benchmark

Full numbers — CER, RTF, first-packet latency, generation speed, footprint, drop rate, **and a per-category CER breakdown** — are in [`BENCHMARK.md`](BENCHMARK.md).

> **Read honestly:** CER is judged by **Whisper-small**, a comparatively weak Mandarin ASR that inflates measured error on exactly the hardest categories (rare characters, digit/acronym strings). The test set is *deliberately* hard — it over-samples edge cases, not everyday Mandarin. Use the per-category breakdown, not a single blended mean.

## 🔐 Weights

Model weights are **not publicly distributed**. They are **gated** on Hugging Face — request access at **[🤗 dove88/supertonic-zh](https://huggingface.co/dove88/supertonic-zh)** (evaluation license). The **current build is non-commercial** (its training data includes the Baker/CSMSC corpus); a Baker-free build for commercial licensing is available separately. You do **not** need the weights to evaluate this project — the [`demo/`](demo/README.md) audio and the [`BENCHMARK.md`](BENCHMARK.md) numbers were both produced with this model.

## 🧑‍💻 Run

The Mandarin model ships as **fused / optimized ONNX graphs**, gated on Hugging Face — **[🤗 dove88/supertonic-zh](https://huggingface.co/dove88/supertonic-zh)** (request access). Inference is **pure ONNX Runtime** (no PyTorch). [`examples/onnx_infer.py`](examples/onnx_infer.py) is the full pipeline:

```bash
pip install onnxruntime numpy soundfile
# place the gated ONNX + upstream vocoder.onnx + indexer + voice in ./onnx
python examples/onnx_infer.py "今天天气很好，我们一起去公园散步吧。"
```

## 🎙️ Voices

This preview synthesizes in a single **preset voice**, shipped as a voice-style embedding JSON ([`assets/F1.json`](assets/F1.json)). **Custom voice / voice cloning** (a new speaker from a reference sample) is **not part of this preview** — it is a separate capability available only under a private/commercial license, and is not described or shipped here.

## 🧾 License

- **Code** — MIT ([`LICENSE`](LICENSE)).
- **Model weights** — separate evaluation license, available on request; the current build is non-commercial only (Baker/CSMSC-encumbered training data). Commercial licensing is available for a separate Baker-free build.

## ⚠️ Limitations

(1) Residual high-frequency artifact bounded by the **frozen upstream vocoder** — a ceiling, not a bug; (2) **Chinese⇄English code-switching is currently unreliable** and not demonstrated in this showcase; (3) tone / polyphone / erhua accuracy are **model-inherent** (character-level acoustic model), not front-end-fixable; (4) one preset voice only, no custom voices. Treat this as a **feasibility demonstration**, not a finished product.

## 🗺️ Roadmap

Cleaner high-frequency detail · reliable code-switching · additional preset voices · streaming · on-device SDKs · a Baker-free build eligible for commercial licensing.

## 🙌 Acknowledgements

Built on the publicly released [Supertonic-3](https://huggingface.co/Supertone/supertonic-3) model and sample code. Trained on AISHELL-3 (OpenSLR SLR93) and Baker/CSMSC.

<div align="center">
<sub>Supertonic-ZH · unofficial Mandarin extension · built on Supertonic-3</sub>
</div>
