<div align="center">

# 🗣️ Supertonic-ZH

### 为端侧 Supertonic TTS 家族带来**普通话中文**

[English](README.md) · **简体中文**

<br>

[![status](https://img.shields.io/badge/状态-公开预览-blueviolet)](CHANGELOG.md)
[![license](https://img.shields.io/badge/代码-MIT-green)](LICENSE)
[![build](https://img.shields.io/badge/当前构建-非商用-red)](LICENSE)
[![python](https://img.shields.io/badge/python-3.11-blue)](requirements.txt)
[![HF Model](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-model-yellow)](https://huggingface.co/dove88/supertonic-zh)

<em>原生普通话 · 数字 · 日期 · 金额 · 轻量 · 快速 · 端侧运行。</em>

</div>

---

> **⚠️ 非官方普通话扩展 · 基于 Supertonic-3 构建。** Supertonic-ZH 是基于公开发布的 Supertonic-3 模型构建的独立普通话扩展。`v0.1.0-preview` · 2026-07-11。

## ✨ 为什么需要 Supertonic-ZH?

官方 **Supertonic-3** 是一个快速、轻量、可端侧运行的 TTS 家族,但开箱**不支持普通话中文合成**。Supertonic-ZH 补上这一块:普通话微调以**优化、算子融合的 ONNX 图**形式分发,在**纯 ONNX Runtime** 上运行,叠加在**冻结、未改动**的上游声码器之上。

<div align="center">

| ❌ 官方 Supertonic-3 | ✅ Supertonic-ZH |
|---|---|
| 无法合成普通话 | 可听懂的原生普通话 |
| 把 "12,580.60元" 逐位念 | 日期 / 金额 / 百分比 / 电话 规范成口语中文 |
| — | 公开 benchmark · 可复现测试集 |

</div>

## 🚀 亮点

- 🈶 **原生普通话**,统一的**预置音色** —— 声调、多音字、儿化、轻声、一/不变调。
- 🔢 **智能文本规范化** —— 日期、金额、百分比、电话号码、全角标点都按人的读法处理。
- ⚡ **快** —— GPU 上约 **10 倍实时**生成(RTF ≈ 0.10),见 [`BENCHMARK.md`](BENCHMARK.md)。
- 🪶 **轻量** —— 体积小,面向端侧 / 离线 / 低延迟场景。
- 🧊 **声码器零改动** —— 四个上游 ONNX 图全部**冻结**使用,不损伤基座模型。
- 🔎 **诚实且可复现** —— 附带公开的百句测试集,以及其背后的确切 CER 数字。

## 🎧 试听

冻结基座保留的多语种输出,加上微调模型生成的原生普通话 —— 点击 ▶️ 播放:

| 语言 | 文字 | 语音 |
|---|---|---|
| 🇨🇳 普通话 | 今天天气很好，我们一起去公园散步吧。 | [▶️ 播放](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_mandarin.wav) |
| 🇬🇧 英语 | The quick brown fox jumps over the lazy dog. | [▶️ 播放](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_english.wav) |
| 🇷🇺 俄语 | Сегодня прекрасная погода, давайте прогуляемся в парке. | [▶️ 播放](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_russian.wav) |
| 🇸🇦 阿拉伯语 | الطقس جميل اليوم، دعونا نذهب في نزهة。 | [▶️ 播放](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_arabic.wav) |
| 🇫🇷 法语 | Il fait très beau aujourd'hui, allons nous promener dans le parc. | [▶️ 播放](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_french.wav) |
| 🇯🇵 日语 | 今日はいい天気ですね、公園を散歩しましょう。 | [▶️ 播放](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_japanese.wav) |
| 🇰🇷 韩语 | 오늘 날씨가 좋네요, 공원을 산책합시다. | [▶️ 播放](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_korean.wav) |

另有七条覆盖最难中文类别(日期、英文缩写、长文本、金额、百分比、多音字、生僻字)的样音在 [`demo/`](demo/README.md):

| 类别 | 文字 | 语音 |
|---|---|---|
| 日期 | 会议定在2026年8月15日上午举行。 | [▶️ 播放](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/date.wav) |
| 英文缩写 | 训练模型需要用到GPU加速。 | [▶️ 播放](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/en_acronym.wav) |
| 长文本 | 这次旅行我们先去了西安看兵马俑，又去了敦煌欣赏壁画，最后到了张掖看七彩丹霞，一路上风景美不胜收。 | [▶️ 播放](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/long_text.wav) |
| 金额 | 这件外套售价12,580.60元。 | [▶️ 播放](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/money.wav) |
| 百分比 | 今年公司营收增长了23.7%。 | [▶️ 播放](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/percent.wav) |
| 多音字 | 他去银行取钱，然后在路上行走回家。 | [▶️ 播放](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/polyphone.wav) |
| 生僻字 | 他觉得这件事有点囧，不知道怎么解释。 | [▶️ 播放](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/rare_char.wav) |

> ▶️ 会在 GitHub 原始内容域打开音频,在浏览器直接播放。

## 📊 Benchmark

完整指标 —— CER、RTF、首包延迟、生成速度、体积、漏字率,**以及按类别的 CER 拆分** —— 见 [`BENCHMARK.md`](BENCHMARK.md)。

> **请客观解读:** CER 由 **Whisper-small** 判定,它对中文本就偏弱,尤其在最难的类别(生僻字、数字/缩写串)上会**高估**错误率。测试集也是**刻意做难**的 —— 过采样边角情况,而非日常普通话。请看按类别拆分,而不是单一均值。

## 🔐 权重

模型权重**不公开分发**,在 Hugging Face **门控**提供 —— 到 **[🤗 dove88/supertonic-zh](https://huggingface.co/dove88/supertonic-zh)** 申请访问(评估许可)。**当前构建为非商用**(训练数据包含 Baker/CSMSC 语料);面向商用授权的 Baker-free 构建另行提供。评估本项目**无需**权重 —— [`demo/`](demo/README.md) 的音频与 [`BENCHMARK.md`](BENCHMARK.md) 的指标都由该模型生成。

## 🧑‍💻 运行

普通话模型以**融合/优化的 ONNX 图**分发,在 Hugging Face **门控** —— **[🤗 dove88/supertonic-zh](https://huggingface.co/dove88/supertonic-zh)**(申请访问)。推理是**纯 ONNX Runtime**(无 PyTorch)。[`examples/onnx_infer.py`](examples/onnx_infer.py) 是完整管线:

```bash
pip install onnxruntime numpy soundfile
# 把门控 ONNX + 上游 vocoder.onnx + indexer + voice 放到 ./onnx
python examples/onnx_infer.py "今天天气很好，我们一起去公园散步吧。"
```

## 🎙️ 音色

本预览以单一**预置音色**合成,以 voice-style 嵌入 JSON 形式提供([`assets/F1.json`](assets/F1.json))。**自定义音色 / 语音克隆**(从一段参考音频克隆新说话人)**不属于本预览** —— 它是仅在私有/商用授权下提供的独立能力,此处不描述、不分发。

## 🧾 许可证

- **代码** —— MIT([`LICENSE`](LICENSE))。
- **模型权重** —— 独立的评估许可,按需提供;当前构建仅限非商用(训练数据包含 Baker/CSMSC 语料)。

## ⚠️ 限制

(1) 残留高频伪影由**冻结的上游声码器**决定 —— 是天花板,不是 bug;(2) **中英文混读目前不可靠**,本展示未演示该能力;(3) 声调 / 多音字 / 儿化 的准确度是**模型固有**(字级声学模型),前端修不了;(4) 仅一个预置音色,无自定义音色。请把它当作**可行性演示**,而非成品。

## 🗺️ 路线图

更干净的高频细节 · 可靠的中英混读 · 更多预置音色 · 流式 · 端侧 SDK · 可商用授权的 Baker-free 构建。

## 🙌 致谢

基于公开发布的 [Supertonic-3](https://huggingface.co/Supertone/supertonic-3) 模型与示例代码构建。训练数据为 AISHELL-3(OpenSLR SLR93)与 Baker/CSMSC。

<div align="center">
<sub>Supertonic-ZH · 非官方普通话扩展 · 基于 Supertonic-3 构建</sub>
</div>
