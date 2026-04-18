"""
utils.py — Shared utilities.

Covers: logging setup, date validation, CLI banner, run summary.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional


# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------

def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stderr,
    )


# ------------------------------------------------------------------
# Date helpers
# ------------------------------------------------------------------

def validate_date(date_str: str, param_name: str) -> datetime:
    """
    Parse YYYY-MM-DD string into datetime.
    Exits with a clear message on bad input.
    """
    try:
        return datetime.strptime(date_str.strip(), "%Y-%m-%d")
    except ValueError:
        print(f"❌ Invalid date for --{param_name}: '{date_str}'. Expected YYYY-MM-DD")
        sys.exit(1)


# ------------------------------------------------------------------
# CLI display
# ------------------------------------------------------------------

BANNER = r"""
 ____                       _ _
/ ___|  ___ _ __ __ _ _ __ | (_)_ __   __ _
\___ \ / __| '__/ _` | '_ \| | | '_ \ / _` |
 ___) | (__| | | (_| | |_) | | | | | | (_| |
|____/ \___|_|  \__,_| .__/|_|_|_| |_|\__, |
                      |_|              |___/
  YouTube Channel Intelligence Tool
"""

def print_banner() -> None:
    print(BANNER)


def print_summary(
    channel_name: str,
    top_videos: List[dict],
    top_shorts: List[dict],
    output_dir: str,
) -> None:
    """Print a clean post-run summary."""
    total = len(top_videos) + len(top_shorts)
    out   = Path(output_dir) / channel_name

    print("\n" + "─" * 60)
    print(f"✅  Done! {total} files written for channel '{channel_name}'")
    print(f"   📁 Output: {out.resolve()}")
    print(f"   🎬 Videos : {len(top_videos):>4}  →  {out / 'videos'}")
    print(f"   ⚡ Shorts : {len(top_shorts):>4}  →  {out / 'shorts'}")

    if top_videos:
        best = top_videos[0]
        print(f"\n   🏅 Top Video : \"{best['title']}\" (score {best['score']:.4f})")
    if top_shorts:
        best = top_shorts[0]
        print(f"   🏅 Top Short : \"{best['title']}\" (score {best['score']:.4f})")

    print("─" * 60 + "\n")
