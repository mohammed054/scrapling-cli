from __future__ import annotations

import logging
import time
from datetime import date
from pathlib import Path

from .classification import classify_all
from .fetcher import ChannelFetchResult, enrich_content_item, fetch_channel_entries
from .filtering import filter_by_date
from .models import (
    ChannelRunConfig,
    ChannelRunResult,
    FetchNewRunConfig,
    FetchNewRunResult,
    IncrementalChannelResult,
)
from .rendering import write_items
from .reporting import export_csv, generate_channel_report
from .scoring import score_items, select_top_percent
from .state import get_last_run, load_state, save_state
from .transcripts import TranscriptService
from .utils import slugify_channel_name, stable_sort

logger = logging.getLogger(__name__)


class TranscriptResolutionError(RuntimeError):
    """Raised when a run requires transcripts but some items remain unresolved."""


def _build_transcript_service(config) -> TranscriptService:
    return TranscriptService(config.transcript_options)


def _enrich_items(items, progress_callback=None) -> None:
    for index, item in enumerate(items, 1):
        enrich_content_item(item)
        if progress_callback:
            progress_callback(index, len(items), item.title)


def _format_transcript_failures(items) -> str:
    sample = []
    for item in items[:5]:
        sample.append(f"{item.id} ({item.title}): {item.transcript.error or item.transcript.status}")
    suffix = "" if len(items) <= 5 else f" ... and {len(items) - 5} more"
    return "; ".join(sample) + suffix


def _resolve_transcripts_or_raise(transcript_service: TranscriptService, items, options) -> None:
    if not options.enabled or not items:
        return

    transcript_service.resolve_many(items)
    if not options.require_success:
        return

    retry_round = 0
    while True:
        unresolved = [item for item in items if item.transcript.status != "available"]
        if not unresolved:
            return
        retryable = [item for item in unresolved if transcript_service.is_retryable_failure(item.transcript)]
        if not retryable:
            raise TranscriptResolutionError(
                f"Could not resolve all transcripts: {_format_transcript_failures(unresolved)}"
            )

        retry_round += 1
        sleep_seconds = max(30.0, max(1.0, options.request_delay_seconds) * 4)
        logger.warning(
            "transcript.retry_round round=%s unresolved=%s retryable=%s sleep_seconds=%.2f",
            retry_round,
            len(unresolved),
            len(retryable),
            sleep_seconds,
        )
        time.sleep(sleep_seconds)
        transcript_service.resolve_many(retryable)


def run_channel_analysis(config: ChannelRunConfig) -> ChannelRunResult:
    fetched = fetch_channel_entries(
        config.channel,
        candidate_percent=config.top_percent,
        enrich_pages=not config.no_enrich,
        include_videos=not config.no_videos,
        include_shorts=not config.no_shorts,
    )
    videos, shorts = classify_all(fetched.items)
    videos = filter_by_date(videos, config.from_date, config.to_date)
    shorts = filter_by_date(shorts, config.from_date, config.to_date)

    scored_videos = score_items(
        videos,
        use_recency_decay=config.recency_decay,
        clamp_outliers=config.clamp_outliers,
        rank_by=config.rank_by,
    )
    scored_shorts = score_items(
        shorts,
        use_recency_decay=config.recency_decay,
        clamp_outliers=config.clamp_outliers,
        rank_by=config.rank_by,
    )
    top_videos = select_top_percent(scored_videos, config.top_percent) if scored_videos else []
    top_shorts = select_top_percent(scored_shorts, config.top_percent) if scored_shorts else []

    transcript_service = _build_transcript_service(config)
    _resolve_transcripts_or_raise(transcript_service, top_videos + top_shorts, config.transcript_options)

    result = ChannelRunResult(
        channel_name=fetched.channel_name,
        channel_slug=fetched.channel_slug,
        videos=scored_videos,
        shorts=scored_shorts,
        top_videos=top_videos,
        top_shorts=top_shorts,
        scraped_item_count=fetched.scraped_item_count,
        candidate_item_count=fetched.candidate_item_count,
        output_root=config.output_dir / fetched.channel_slug,
    )
    if config.dry_run:
        return result

    output_root = config.output_dir / fetched.channel_slug
    videos_dir = output_root / "videos"
    shorts_dir = output_root / "shorts"
    written_files: list[Path] = []

    if top_videos:
        written_files.extend(
            write_items(
                stable_sort(top_videos, score_first=True),
                videos_dir,
                include_score_details=True,
                prune_existing=True,
            )
        )
    else:
        videos_dir.mkdir(parents=True, exist_ok=True)
        for stale in videos_dir.glob("*.md"):
            stale.unlink()

    if top_shorts:
        written_files.extend(
            write_items(
                stable_sort(top_shorts, score_first=True),
                shorts_dir,
                include_score_details=True,
                prune_existing=True,
            )
        )
    else:
        shorts_dir.mkdir(parents=True, exist_ok=True)
        for stale in shorts_dir.glob("*.md"):
            stale.unlink()

    result.written_files = written_files

    if not config.no_report:
        result.report_path = generate_channel_report(
            channel_name=fetched.channel_name,
            all_videos=scored_videos,
            all_shorts=scored_shorts,
            top_videos=top_videos,
            top_shorts=top_shorts,
            top_percent=config.top_percent,
            rank_by=config.rank_by,
            from_date=config.from_date,
            to_date=config.to_date,
            output_dir=output_root,
            scraped_item_count=fetched.scraped_item_count,
            candidate_item_count=fetched.candidate_item_count,
        )

    if config.export_csv:
        result.csv_paths = [
            export_csv(stable_sort(scored_videos, score_first=True), output_root / "scored_videos.csv"),
            export_csv(stable_sort(scored_shorts, score_first=True), output_root / "scored_shorts.csv"),
        ]

    return result


def _filter_new_items(fetched: ChannelFetchResult, from_date: date) -> tuple[list, list]:
    videos, shorts = classify_all(fetched.items)
    filtered_videos = filter_by_date(videos, from_date, None)
    filtered_shorts = filter_by_date(shorts, from_date, None)
    return filtered_videos, filtered_shorts


def run_incremental_fetch(config: FetchNewRunConfig) -> FetchNewRunResult:
    state = load_state(config.state_file)
    transcript_service = _build_transcript_service(config)
    channel_results: list[IncrementalChannelResult] = []
    today = date.today().isoformat()

    for channel in config.channels:
        channel_key = slugify_channel_name(channel.strip("@"))
        from_date = config.force_from or get_last_run(state, channel_key, config.days_back)
        fetched = fetch_channel_entries(
            channel,
            candidate_percent=None,
            enrich_pages=False,
            include_videos=True,
            include_shorts=True,
        )
        videos, shorts = _filter_new_items(fetched, from_date)
        new_videos = stable_sort(videos, score_first=False)
        new_shorts = stable_sort(shorts, score_first=False)
        new_items = new_videos + new_shorts

        _enrich_items(new_items)
        _resolve_transcripts_or_raise(transcript_service, new_items, config.transcript_options)

        output_root = config.output_dir / fetched.channel_slug
        written_files: list[Path] = []
        if new_videos:
            written_files.extend(
                write_items(
                    new_videos,
                    output_root / "videos",
                    include_score_details=False,
                    prune_existing=False,
                )
            )
        if new_shorts:
            written_files.extend(
                write_items(
                    new_shorts,
                    output_root / "shorts",
                    include_score_details=False,
                    prune_existing=False,
                )
            )

        channel_results.append(
            IncrementalChannelResult(
                channel=channel,
                channel_name=fetched.channel_name,
                channel_slug=fetched.channel_slug,
                from_date=from_date,
                items=new_items,
                written_files=written_files,
            )
        )

        state[f"last_run_{channel_key}"] = today
        save_state(config.state_file, state)
        logger.info(
            "fetch_new.channel_complete channel=%s from_date=%s written=%s",
            channel,
            from_date,
            len(written_files),
        )

    return FetchNewRunResult(channel_results=channel_results)
