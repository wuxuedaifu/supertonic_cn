# Supertonic-ZH Demo Audio

All clips below were generated with the licensed supertonic-zh model
(weights available on request under an evaluation license, not publicly
distributed), F1 preset voice, `total_step=16`.

## Languages

Retained multilingual output from the frozen base Supertonic-3 model, plus
native Mandarin from the fine-tune.

| Language | Text | Audio |
|---|---|---|
| Mandarin | 今天天气很好，我们一起去公园散步吧。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_mandarin.wav) |
| English | The quick brown fox jumps over the lazy dog. | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_english.wav) |
| Russian | Сегодня прекрасная погода, давайте прогуляемся в парке. | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_russian.wav) |
| Arabic | الطقس جميل اليوم، دعونا نذهب في نزهة。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_arabic.wav) |
| French | Il fait très beau aujourd'hui, allons nous promener dans le parc. | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_french.wav) |
| Japanese | 今日はいい天気ですね、公園を散歩しましょう。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_japanese.wav) |
| Korean | 오늘 날씨가 좋네요, 공원을 산책합시다. | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/lang_korean.wav) |

## Chinese hard categories

Each row covers a "hard" text category from the public test set
(`../tests/zh_testset_public.jsonl`); sentences are copied verbatim from
that test set.

| Category | Text | Audio |
|---|---|---|
| date | 会议定在2026年8月15日上午举行。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/date.wav) |
| en_acronym | 训练模型需要用到GPU加速。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/en_acronym.wav) |
| long_text | 这次旅行我们先去了西安看兵马俑，又去了敦煌欣赏壁画，最后到了张掖看七彩丹霞，一路上风景美不胜收。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/long_text.wav) |
| money | 这件外套售价12,580.60元。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/money.wav) |
| percent | 今年公司营收增长了23.7%。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/percent.wav) |
| polyphone | 他去银行取钱，然后在路上行走回家。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/polyphone.wav) |
| rare_char | 他觉得这件事有点囧，不知道怎么解释。 | [▶️ Play](https://raw.githubusercontent.com/wuxuedaifu/supertonic_cn/main/demo/rare_char.wav) |

## Known limitations

Residual high-frequency artifact (frozen-vocoder ceiling — the vocoder
graph is never fine-tuned by this project) remains audible in these
samples; this is a ceiling, not a fixable bug. Chinese⇄English
code-switching is currently unreliable and is not demonstrated in this
showcase. Tone/polyphone/erhua accuracy is a model capability learned
from training data, not something the text front-end can fix.

Regenerating these samples requires the licensed model weights and is not
reproducible from the public repository alone.
