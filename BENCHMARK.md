# Supertonic-ZH Benchmark

- model: supertonic-zh acoustic model (v0.1) — **weights not publicly distributed; available on request under an evaluation license. Current build is non-commercial (Baker/CSMSC data); commercial licensing available separately for a Baker-free build.**
- voice: preset voice (style-embedding JSON)
- date: 2026-07-11
- device: cuda
- rows: 114

> CER is judged by Whisper-small (a weak ASR judge for Mandarin, especially on rare characters / code-switch / digit strings); the test set is deliberately hard. Read per-category numbers, not just the mean.

| Metric | Value |
|---|---|
| CER (mean) | 0.4444 |
| RTF (mean) | 0.1043 |
| First packet (ms) | 609.0 |
| Generation speed (audio-sec/wall-sec) | 10.54 |
| Model footprint (MB) | ~89 |
| Drop rate | 0.0088 |
| Code-switch CER (mix_cer) | 0.6156 |

| Category | CER | n |
|---|---|---|
| common | 0.2285 | 6 |
| polyphone | 0.2442 | 6 |
| long_text | 0.2675 | 6 |
| yi_bu_sandhi | 0.2797 | 6 |
| erhua | 0.2827 | 6 |
| neutral_tone | 0.2877 | 6 |
| person_name | 0.3822 | 6 |
| repeat_drop | 0.4142 | 6 |
| place_name | 0.4464 | 6 |
| punctuation | 0.4582 | 6 |
| en_acronym | 0.4706 | 6 |
| tone1234 | 0.4840 | 6 |
| time | 0.5063 | 6 |
| date | 0.5184 | 6 |
| rare_char | 0.5561 | 6 |
| money | 0.5849 | 6 |
| code_switch | 0.6156 | 6 |
| percent | 0.6255 | 6 |
| phone | 0.7912 | 6 |
