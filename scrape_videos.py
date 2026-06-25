#!/usr/bin/env python3
"""
Scrape transcripts for individual YouTube videos from a URL list file.
Outputs markdown files with video metadata and transcripts.
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
import time
from pathlib import Path
from typing import Optional

from src.scrapling_cli.fetcher import enrich_content_item
from src.scrapling_cli.models import ContentItem, TranscriptOptions
from src.scrapling_cli.rendering import write_item
from src.scrapling_cli.transcripts import TranscriptService
from src.scrapling_cli.utils import build_filename, parse_date, repair_text, slugify

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def extract_video_id(url: str) -> Optional[str]:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/|/embed/|/shorts/)([^&\n?#/]+)",
        r"youtube\.com/watch\?v=([^&\n?#]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def create_content_item(url: str) -> Optional[ContentItem]:
    """Create a ContentItem from a video URL with minimal initial data."""
    video_id = extract_video_id(url)
    if not video_id:
        logger.warning("Could not extract video ID from: %s", url)
        return None

    return ContentItem(
        id=video_id,
        title=video_id,  # Will be updated during enrichment
        url=url,
        type="video",
    )


def load_urls(file_path: Path) -> list[str]:
    """Load and deduplicate URLs from file."""
    if not file_path.exists():
        logger.error("URL file not found: %s", file_path)
        return []

    urls = []
    seen_ids = set()
    with file_path.open("r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            video_id = extract_video_id(line)
            if video_id and video_id not in seen_ids:
                seen_ids.add(video_id)
                urls.append(line)
            elif video_id:
                logger.info(
                    "Skipping duplicate video ID: %s (line %d)", video_id, line_num
                )
            else:
                logger.warning("Invalid URL format on line %d: %s", line_num, line)

    logger.info("Loaded %d unique video URLs from %s", len(urls), file_path)
    return urls


def enrich_item(item: ContentItem) -> ContentItem:
    """Enrich a single item with watch page data."""
    try:
        enrich_content_item(item, retries=2)
    except Exception as exc:  # noqa: BLE001
        logger.warning("Enrichment failed for %s: %s", item.id, exc)
    return item


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Scrape transcripts for individual YouTube videos",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--urls-file",
        "-u",
        type=Path,
        default=Path("videos.txt"),
        help="Path to file containing YouTube URLs (one per line)",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        default=Path("output/videos"),
        help="Output directory for markdown files",
    )
    parser.add_argument(
        "--cookies-from-browser",
        default="chrome:Default",
        help="Browser and profile for yt-dlp cookies (e.g., chrome:Default)",
    )
    parser.add_argument(
        "--cookies-file",
        type=Path,
        default=None,
        help="Path to Netscape format cookies.txt file (alternative to --cookies-from-browser)",
    )
    parser.add_argument(
        "--transcript-language",
        default="en",
        help="Preferred transcript language code",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Transcript worker count",
    )
    parser.add_argument(
        "--transcript-delay",
        type=float,
        default=12.0,
        help="Minimum delay between transcript requests (seconds)",
    )
    parser.add_argument(
        "--transcript-retries",
        type=int,
        default=8,
        help="Retry attempts per transcript backend",
    )
    parser.add_argument(
        "--transcript-rate-limit-cooldown",
        type=float,
        default=600.0,
        help="Base cooldown after YouTube 429/bot-block (seconds)",
    )
    parser.add_argument(
        "--allow-missing-transcripts",
        action="store_true",
        default=True,
        help="Continue even when some transcripts are unavailable",
    )
    parser.add_argument(
        "--no-enrich",
        action="store_true",
        help="Skip watch page enrichment (faster, less metadata)",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--include-score",
        action="store_true",
        help="Include scoring details in markdown (requires channel context, mostly placeholder)",
    )
    parser.add_argument(
        "--no-yt-dlp",
        action="store_true",
        help="Disable yt-dlp backend (use only youtube_transcript_api)",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load URLs
    urls = load_urls(args.urls_file)
    if not urls:
        logger.error("No valid URLs to process")
        return 1

    # Build transcript options
    transcript_options = TranscriptOptions(
        enabled=True,
        language=args.transcript_language,
        cache_dir=Path(".cache/scrapling-cli"),
        workers=max(1, args.workers),
        request_delay_seconds=max(0.0, args.transcript_delay),
        retry_attempts=max(1, args.transcript_retries),
        rate_limit_cooldown_seconds=max(1.0, args.transcript_rate_limit_cooldown),
        rate_limit_cooldown_cap_seconds=max(
            1.0, args.transcript_rate_limit_cooldown * 6
        ),
        require_success=not args.allow_missing_transcripts,
        allow_hosted_asr=False,  # Disable OpenAI/OpenRouter ASR per user request
        cookies_from_browser=args.cookies_from_browser,
        cookies_file=args.cookies_file,
    )

    # Initialize transcript service
    if args.no_yt_dlp:
        from src.scrapling_cli.transcripts.backends import YouTubeTranscriptApiBackend

        transcript_service = TranscriptService(
            transcript_options, backends=[YouTubeTranscriptApiBackend()]
        )
    else:
        transcript_service = TranscriptService(transcript_options)

    # Ensure output directory exists
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Process each video
    success_count = 0
    failed_count = 0
    transcript_available = 0
    transcript_unavailable = 0

    for index, url in enumerate(urls, 1):
        logger.info("[%d/%d] Processing: %s", index, len(urls), url)

        item = create_content_item(url)
        if not item:
            failed_count += 1
            continue

        # Enrich with watch page data (title, views, description, etc.)
        if not args.no_enrich:
            logger.debug("Enriching %s...", item.id)
            enrich_item(item)

        # Fetch transcript
        logger.debug("Fetching transcript for %s...", item.id)
        transcript_service.resolve_item(item)

        # Write markdown
        try:
            write_item(
                item,
                args.output_dir,
                dedup=set(),
                include_score_details=args.include_score,
            )
            success_count += 1
            if item.transcript.status == "available":
                transcript_available += 1
            else:
                transcript_unavailable += 1
                logger.warning(
                    "Transcript unavailable for %s (%s): %s",
                    item.id,
                    item.title,
                    item.transcript.error or item.transcript.status,
                )
        except Exception as exc:  # noqa: BLE001
            logger.error("Failed to write markdown for %s: %s", item.id, exc)
            failed_count += 1

        # Small delay between videos to be polite
        if index < len(urls):
            time.sleep(1.0)

    # Summary
    logger.info("=" * 50)
    logger.info("SCRAPING COMPLETE")
    logger.info("=" * 50)
    logger.info("Total videos:      %d", len(urls))
    logger.info("Successfully wrote: %d", success_count)
    logger.info("Failed:            %d", failed_count)
    logger.info("Transcripts found:  %d", transcript_available)
    logger.info("Transcripts missing: %d", transcript_unavailable)
    logger.info("Output directory:  %s", args.output_dir.resolve())

    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
