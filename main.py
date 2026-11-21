"""Entrypoint for the news-image-20261121 poster.

Copies the pre-rendered poster (assets/poster.png) to entry.png in the
output directory. Standard library only, no network access. The output
directory comes from MAKEFUN_OUTPUT_DIR, defaulting to /output.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
POSTER = HERE / "assets" / "poster.png"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(POSTER, target)
    print(target)


if __name__ == "__main__":
    main()
