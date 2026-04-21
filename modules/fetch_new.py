#!/usr/bin/env python3
"""
fetch_new.py — Cron-friendly fetcher for NEW YouTube content.

Fetches only videos/shorts published since the last successful run.
Saves description + transcript as Markdown files. No scoring, no selection.

State is tracked in state.json so each run knows where it left off.

Usage:
    python fetch_new.py
    python fetch_new.py --channels "@IBMTechnology" "@SomeOtherChannel"
    python fetch_new.py --days-back 14 --no-transcripts

Cron example (runs every day at 6 AM):
    0 6 * * * cd /path/to/project && python fetch_new.py >> logs/cron.log 2>&1
"""

import argparse
import json
import logging
import os
import re
import sys
import time
import unicodedata
from datetime import datetime, date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from modules.fetcher import (
    fetch_channel_videos,
    resolve_channel_url,
    _scrape_tab,
    _slugify_name,
)
from modules.classifier import classify_all
from modules.filter import filter_by_date
from modules.transcript import enrich_with_transcripts

# ── Config ────────────────────────────────────────────────────────────────────

# Channels to watch. Override with --channels flag.
DEFAULT_CHANNELS = [
    "@IBMTechnology",
]

STATE_FILE  = "state.json"       # tracks last-run dates per channel
OUTPUT_DIR  = "output_new"       # separate from the top-performer output
LOG_FILE    = "logs/fetch_new.log"
DAYS_BACK   = 7                  # fallback window when no state exists

# ── Logging ───────────────────────────────────────────────────────────────────

def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    fmt   = "[%(asctime)s] %(levelname)-8s %(message)s"
    handlers = [logging.StreamHandler(sys.stdout)]
    if LOG_FILE:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        handlers.append(logging.FileHandler(LOG_FILE, encoding="utf-8"))
    logging.basicConfig(level=level, format=fmt, datefmt="%Y-%m-%d %H:%M:%S",
                        handlers=handlers)

logger = logging.getLogger(__name__)

# ── State (last-run tracking) ─────────────────────────────────────────────────

def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not read state file: {e}")
    return {}


def save_state(state: dict):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        logger.error(f"Could not write state file: {e}")


def get_last_run(state: dict, channel_slug: str, days_back: int) -> date:
    """Return the date to fetch from — last run date, or N days ago."""
    key = f"last_run_{channel_slug}"
    if key in state:
        try:
            return date.fromisoformat(state[key])
        except Exception:
            pass
    fallback = date.today() - timedelta(days=days_back)
    logger.info(f"No previous run for '{channel_slug}' — fetching last {days_back} days")
    return fallback

# ── Markdown writer (simplified — no scoring metadata) ────────────────────────

MAX_FILENAME_LEN = 100

def _slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    text = re.sub(r"[\s\-]+", "-", text).strip("-")
    return text[:MAX_FILENAME_LEN]


def _dur(seconds) -> str:
    try:
        s   = int(seconds)
        h, rem = divmod(s, 3600)
        m, sec = divmod(rem, 60)
        return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"
    except Exception:
        return "unknown"


def _render_markdown(item: dict) -> str:
    title       = item.get("title", "Untitled")
    d           = item.get("date")
    date_str    = d.strftime("%Y-%m-%d") if isinstance(d, date) else "Unknown"
    video_type  = item.get("type", "video").capitalize()
    duration    = _dur(item.get("duration", 0))
    views       = f"{item.get('views', 0):,}"
    url         = item.get("url", "")
    channel     = item.get("channel", "")
    channel_url = item.get("channel_url", "")
    thumbnail   = item.get("thumbnail", "")
    description = (item.get("description") or "").strip() or "_No description provided._"
    transcript  = (item.get("transcript") or "Transcript not available").strip()

    thumb_block = f"![Thumbnail]({thumbnail})\n\n" if thumbnail else ""

    return (
        f"{thumb_block}"
        f"# {title}\n\n"
        f"---\n\n"
        f"## 📋 Info\n\n"
        f"| Field | Value |\n"
        f"|-------|-------|\n"
        f"| **Date** | {date_str} |\n"
        f"| **Type** | {video_type} |\n"
        f"| **Duration** | {duration} |\n"
        f"| **Views** | {views} |\n"
        f"| **Channel** | [{channel}]({channel_url}) |\n"
        f"| **URL** | [Watch on YouTube]({url}) |\n\n"
        f"---\n\n"
        f"## 📖 Description\n\n"
        f"{description}\n\n"
        f"---\n\n"
        f"## 📝 Transcript\n\n"
        f"{transcript}\n"
    )


def write_item(item: dict, output_dir: str, seen_filenames: set) -> str:
    os.makedirs(output_dir, exist_ok=True)
    d    = item.get("date")
    ds   = d.strftime("%Y-%m-%d") if isinstance(d, date) else "no-date"
    base = f"{_slugify(item.get('title', 'untitled'))}-{ds}.md"
    name = base
    ctr  = 1
    while name in seen_filenames:
        name = f"{base[:-3]}-{ctr}.md"
        ctr += 1
    seen_filenames.add(name)

    path = os.path.join(output_dir, name)
    # Skip if already written in a previous run
    if os.path.exists(path):
        logger.debug(f"Already exists, skipping: {path}")
        return path

    with open(path, "w", encoding="utf-8") as f:
        f.write(_render_markdown(item))
    logger.info(f"  Wrote: {path}")
    return path


# ── Per-channel fetch ─────────────────────────────────────────────────────────

def fetch_new_for_channel(
    channel: str,
    from_date: date,
    output_dir: str,
    fetch_transcripts: bool,
) -> int:
    """Fetch new content for one channel. Returns number of new items written."""

    logger.info(f"=== Channel: {channel} | from: {from_date} ===")

    # Fetch from both tabs
    all_entries: list[dict] = []
    channel_name = "unknown_channel"

    for tab in ("videos", "shorts"):
        entries, name = _scrape_tab(resolve_channel_url(channel), tab)
        all_entries.extend(entries)
        if name and name != "unknown_channel":
            channel_name = name

    if not all_entries:
        logger.warning(f"No entries found for {channel}")
        return 0

    logger.info(f"Scraped {len(all_entries)} raw entries")

    # Classify
    videos, shorts = classify_all(all_entries)

    # Date filter — only NEW content
    videos = filter_by_date(videos, from_date=from_date, to_date=None)
    shorts = filter_by_date(shorts, from_date=from_date, to_date=None)

    new_items = videos + shorts
    logger.info(f"After date filter: {len(videos)} videos, {len(shorts)} shorts — {len(new_items)} total new")

    if not new_items:
        logger.info("Nothing new. All caught up.")
        return 0

    # Enrich all new items (not just top-%) to get exact dates, descriptions etc.
    logger.info(f"Enriching {len(new_items)} new items...")
    from modules.fetcher import enrich_video_page
    for idx, item in enumerate(new_items, 1):
        logger.debug(f"  [{idx}/{len(new_items)}] {item.get('title', '')[:55]}")
        enrich_video_page(item)
        time.sleep(0.3)

    # Transcripts
    if fetch_transcripts:
        logger.info("Fetching transcripts...")
        enrich_with_transcripts(new_items)

    # Write
    slug        = _slugify_name(channel_name)
    videos_dir  = os.path.join(output_dir, slug, "videos")
    shorts_dir  = os.path.join(output_dir, slug, "shorts")
    seen: set[str] = set()

    written = 0
    for item in videos:
        write_item(item, videos_dir, seen)
        written += 1
    for item in shorts:
        write_item(item, shorts_dir, seen)
        written += 1

    logger.info(f"Written {written} new files for '{channel_name}'")
    return written, slug


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(
        prog="fetch-new",
        description="Fetch fresh YouTube content (cron-friendly). Saves description + transcript.",
    )
    p.add_argument("--channels", "-c", nargs="+", default=DEFAULT_CHANNELS,
                   help="Channel handles to watch (default: see DEFAULT_CHANNELS in script)")
    p.add_argument("--days-back", type=int, default=DAYS_BACK,
                   help=f"Fallback window when no previous run exists (default: {DAYS_BACK})")
    p.add_argument("--output-dir", "-o", default=OUTPUT_DIR,
                   help=f"Output directory (default: {OUTPUT_DIR})")
    p.add_argument("--no-transcripts", action="store_true",
                   help="Skip transcript fetching (faster)")
    p.add_argument("--force-from", metavar="YYYY-MM-DD",
                   type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
                   help="Override last-run date for all channels")
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args()


def main():
    args   = parse_args()
    setup_logging(args.verbose)
    state  = load_state()

    logger.info("=" * 60)
    logger.info(f"fetch_new.py starting — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Channels: {args.channels}")
    logger.info("=" * 60)

    total_written = 0
    today_str     = date.today().isoformat()

    for channel in args.channels:
        slug = re.sub(r"[^\w]", "_", channel.strip("@").lower())
        try:
            from_date = args.force_from or get_last_run(state, slug, args.days_back)
            result    = fetch_new_for_channel(
                channel=channel,
                from_date=from_date,
                output_dir=args.output_dir,
                fetch_transcripts=not args.no_transcripts,
            )
            # result is (count, slug) or 0
            if isinstance(result, tuple):
                count, _ = result
            else:
                count = result
            total_written += count
            # Update state — mark today as last run for this channel
            state[f"last_run_{slug}"] = today_str
            save_state(state)
        except Exception as e:
            logger.error(f"Failed to process {channel}: {e}", exc_info=True)

    logger.info("=" * 60)
    logger.info(f"Done. Total new files written: {total_written}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
