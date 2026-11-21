# The Daily Compass — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/aizen99829/entry-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/aizen99829/entry-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A dense newspaper front-page poster for the make.fun
[news-image-20261121](https://make.fun/bounty/news-image-20261121) competition. One 1024x1024 image carries 38
verified stories reported on Saturday 21 November 2026: three lead
panels, ten smaller illustrated panels, a schematic world map with
numbered pins 1-13, and a numbered text index for stories 14-38.

Lead stories: Poland seeking NATO help after Russian missiles land on
its soil, Wall Street entering correction as the AI rout deepens, and
Denmark expelling Russia's defence attache over an alleged plot to kill
rapper Kyivstoner. All figures are attributed on the poster; market
figures are Friday's closes, reported on Saturday.

## Files

- `main.py` — stdlib-only entrypoint. Copies `assets/poster.png`
  to `entry.png` in the output directory (`MAKEFUN_OUTPUT_DIR`
  env override, default `/output`). No network access.
- `assets/poster.png` — the rendered poster, 1024x1024 PNG.
- `tools/render.py` — Pillow generator that draws the poster
  from scratch and writes `assets/poster.png`. Deterministic:
  repeated runs produce byte-identical output.
- `LICENSE` — MIT license.

## Run

Regenerate the poster (requires Pillow and DejaVu fonts):

```sh
python3 tools/render.py
```

Produce the entry image:

```sh
python3 main.py
# or, with a custom output directory:
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=2a9s4gx3&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
