#!/usr/bin/env python3
"""
fetch_new.py — Cron-friendly incremental YouTube fetcher.

Fetches ONLY videos/shorts published since the last successful run.
Saves description + transcript as Markdown files.
State is tracked in state.json so each run only pulls what is genuinely new.

Usage:
    python fetch_new.py
    python fetch_new.py --channels "https://www.youtube.com/ibmtechnology"
    python fetch_new.py --channels "@IBMTechnology" --transcripts
    python fetch_new.py --days-back 14 --no-transcripts
    python fetch_new.py --force-from 2025-01-01

Cron — every day at 07:00:
    0 7 * * * cd /path/to/scrapling_cli && python fetch_new.py >> logs/cron.log 2>&1
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

# ── Path fix: ensure project root is on sys.path ─────────────────────────────
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from modules.fetcher import (
    resolve_channel_url,
    _scrape_tab,
    _slugify_name,
    enrich_video_page,
)
from modules.classifier import classify_all
from modules.filter import filter_by_date
from modules.transcript import enrich_with_transcripts

# ── Config ────────────────────────────────────────────────────────────────────

DEFAULT_CHANNELS = [
    "https://www.youtube.com/ibmtechnology",
]

STATE_FILE = "state.json"        # tracks last-run dates per channel
OUTPUT_DIR = "output_new"        # separate from top-performer output
LOG_FILE   = "logs/fetch_new.log"
DAYS_BACK  = 7                   # fallback window when no prior state exists

# ── Logging ───────────────────────────────────────────────────────────────────

def setup_logging(verbose: bool) -> None:
    level   = logging.DEBUG if verbose else logging.INFO
    fmt     = "[%(asctime)s] %(levelname)-8s %(message)s"
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    handlers: list[logging.Handler] = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
    ]
    logging.basicConfig(level=level, format=fmt, datefmt="%Y-%m-%d %H:%M:%S",
                        handlers=handlers)

logger = logging.getLogger(__name__)

# ── State tracking ────────────────────────────────────────────────────────────

def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not read state file: {e}")
    return {}


def save_state(state: dict) -> None:
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        logger.error(f"Could not write state file: {e}")


def get_last_run(state: dict, channel_slug: str, days_back: int) -> date:
    key = f"last_run_{channel_slug}"
    if key in state:
        try:
            return date.fromisoformat(state[key])
        except Exception:
            pass
    fallback = date.today() - timedelta(days=days_back)
    logger.info(f"No prior run for '{channel_slug}' — fetching last {days_back} days")
    return fallback

# ── Markdown rendering ────────────────────────────────────────────────────────

MAX_FNAME = 100


def _slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    text = re.sub(r"[\s\-]+", "-", text).strip("-")
    return text[:MAX_FNAME]


def _dur(seconds) -> str:
    try:
        s = int(seconds)
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
    tags        = item.get("tags", [])
    tag_str     = " ".join(f"`{t}`" for t in tags[:30]) if tags else "_No tags._"

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
        f"## 🏷️ Tags\n\n"
        f"{tag_str}\n\n"
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
) -> tuple[int, str]:
    """
    Fetch new content for one channel since `from_date`.
    Returns (number_of_files_written, channel_slug).
    Always returns a tuple — never raises.
    """
    logger.info(f"=== Channel: {channel} | from: {from_date} ===")

    all_entries: list[dict] = []
    channel_name = "unknown_channel"

    for tab in ("videos", "shorts"):
        try:
            entries, name = _scrape_tab(resolve_channel_url(channel), tab)
            all_entries.extend(entries)
            if name and name != "unknown_channel":
                channel_name = name
        except Exception as e:
            logger.warning(f"Failed scraping tab '{tab}' for {channel}: {e}")

    slug = _slugify_name(channel_name)

    if not all_entries:
        logger.warning(f"No entries found for {channel}")
        return 0, slug

    logger.info(f"Scraped {len(all_entries)} raw entries")

    # Classify → date-filter (new content only)
    videos, shorts = classify_all(all_entries)
    videos = filter_by_date(videos, from_date=from_date, to_date=None)
    shorts = filter_by_date(shorts, from_date=from_date, to_date=None)
    new_items = videos + shorts

    logger.info(
        f"After date filter: {len(videos)} videos, {len(shorts)} shorts "
        f"— {len(new_items)} total new"
    )

    if not new_items:
        logger.info("Nothing new. All caught up.")
        return 0, slug

    # Full enrichment on every new item (dates, descriptions, tags)
    logger.info(f"Enriching {len(new_items)} new items…")
    for idx, item in enumerate(new_items, 1):
        logger.debug(f"  [{idx}/{len(new_items)}] {item.get('title', '')[:60]}")
        try:
            enrich_video_page(item)
        except Exception as e:
            logger.warning(f"  Enrichment failed for {item.get('id', '?')}: {e}")
        time.sleep(0.3)

    # Transcripts
    if fetch_transcripts:
        logger.info("Fetching transcripts…")
        try:
            enrich_with_transcripts(new_items)
        except Exception as e:
            logger.warning(f"Transcript enrichment failed: {e}")

    # Write Markdown
    videos_dir = os.path.join(output_dir, slug, "videos")
    shorts_dir = os.path.join(output_dir, slug, "shorts")
    seen: set[str] = set()
    written = 0

    for item in videos:
        try:
            write_item(item, videos_dir, seen)
            written += 1
        except Exception as e:
            logger.warning(f"Write failed for '{item.get('title', '?')}': {e}")

    for item in shorts:
        try:
            write_item(item, shorts_dir, seen)
            written += 1
        except Exception as e:
            logger.warning(f"Write failed for '{item.get('title', '?')}': {e}")

    logger.info(f"Written {written} new files for '{channel_name}'")
    return written, slug

# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="fetch-new",
        description=(
            "Incremental YouTube channel watcher — cron-friendly.\n"
            "Saves only NEW videos/shorts (since last run) as Markdown with transcripts."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with defaults (IBM Technology, last 7 days on first run):
  python fetch_new.py

  # Watch a specific channel, fetch transcripts:
  python fetch_new.py --channels "https://www.youtube.com/ibmtechnology" --transcripts

  # Watch multiple channels:
  python fetch_new.py --channels "@IBMTechnology" "@mkbhd"

  # Force re-fetch from a specific date:
  python fetch_new.py --force-from 2025-01-01

Cron (every day at 07:00):
  0 7 * * * cd /path/to/scrapling_cli && python fetch_new.py >> logs/cron.log 2>&1
        """,
    )
    p.add_argument(
        "--channels", "-c", nargs="+", default=DEFAULT_CHANNELS,
        help="Channel handle(s) or URL(s) to watch",
    )
    p.add_argument(
        "--days-back", type=int, default=DAYS_BACK,
        help=f"Days to look back on first run (default: {DAYS_BACK})",
    )
    p.add_argument(
        "--output-dir", "-o", default=OUTPUT_DIR,
        help=f"Output directory (default: {OUTPUT_DIR})",
    )
    p.add_argument(
        "--transcripts", action="store_true",
        help="Fetch full transcripts for every new item",
    )
    p.add_argument(
        "--force-from", metavar="YYYY-MM-DD",
        type=lambda s: datetime.strptime(s, "%Y-%m-%d").date(),
        help="Override last-run date for ALL channels",
    )
    p.add_argument("--verbose", "-v", action="store_true")
    return p.parse_args()


def main() -> None:
    args  = parse_args()
    setup_logging(args.verbose)
    state = load_state()

    separator = "=" * 60
    logger.info(separator)
    logger.info(f"fetch_new.py — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Channels : {args.channels}")
    logger.info(f"Transcripts: {'yes' if args.transcripts else 'no'}")
    logger.info(separator)

    total_written = 0
    today_str     = date.today().isoformat()

    for channel in args.channels:
        slug = re.sub(r"[^\w]", "_", channel.strip("@").lower())
        try:
            from_date = args.force_from or get_last_run(state, slug, args.days_back)
            written, _ = fetch_new_for_channel(
                channel=channel,
                from_date=from_date,
                output_dir=args.output_dir,
                fetch_transcripts=args.transcripts,
            )
            total_written += written
            state[f"last_run_{slug}"] = today_str
            save_state(state)
        except Exception as e:
            logger.error(f"Failed to process {channel}: {e}", exc_info=True)

    logger.info(separator)
    logger.info(f"Done. Total new files written: {total_written}")
    logger.info(separator)


if __name__ == "__main__":
    main()
