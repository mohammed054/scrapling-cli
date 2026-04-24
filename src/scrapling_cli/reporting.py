from __future__ import annotations

import csv
import logging
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from .models import ContentItem
from .utils import format_duration, format_number, output_date, write_text

logger = logging.getLogger(__name__)


def _stats(items: list[ContentItem]) -> dict:
    if not items:
        return {
            "count": 0,
            "total_views": 0,
            "total_likes": 0,
            "total_comments": 0,
            "avg_views": 0,
            "avg_likes": 0,
            "avg_engagement": 0.0,
        }
    total_views = sum(item.views for item in items)
    total_likes = sum(item.likes for item in items)
    total_comments = sum(item.comments for item in items)
    average_engagement = (
        sum((item.likes + item.comments) / max(item.views, 1) for item in items) / len(items) * 100
    )
    return {
        "count": len(items),
        "total_views": total_views,
        "total_likes": total_likes,
        "total_comments": total_comments,
        "avg_views": total_views // len(items),
        "avg_likes": total_likes // len(items),
        "avg_engagement": average_engagement,
    }


def _top_table(items: list[ContentItem], *, limit: int = 25) -> str:
    if not items:
        return "_No items._\n"
    rows = [
        "| # | Title | Date | Views | Likes | Duration | Score | Transcript |",
        "|---|-------|------|-------|-------|----------|-------|------------|",
    ]
    for index, item in enumerate(items[:limit], 1):
        exact_date = output_date(item)
        date_text = exact_date.strftime("%Y-%m-%d") if exact_date else "?"
        rows.append(
            f"| {index} | [{item.title[:55]}]({item.url}) | {date_text} | "
            f"{format_number(item.views)} | {format_number(item.likes)} | "
            f"{format_duration(item.duration)} | `{item.score:.4f}` | "
            f"`{item.transcript.status}:{item.transcript.source or 'none'}` |"
        )
    return "\n".join(rows) + "\n"


def _tags_section(items: list[ContentItem]) -> str:
    counts: Counter[str] = Counter()
    for item in items:
        for tag in item.tags:
            counts[tag.lower()] += 1
    if not counts:
        return "_No tag data._"
    return ", ".join(f"`{tag}` ({count})" for tag, count in counts.most_common(30))


def _transcript_summary(items: list[ContentItem]) -> str:
    if not items:
        return "_No items._"
    counts: Counter[str] = Counter(
        f"{item.transcript.status}:{item.transcript.source or 'none'}" for item in items
    )
    return ", ".join(f"`{label}` ({count})" for label, count in counts.most_common())


def generate_channel_report(
    *,
    channel_name: str,
    all_videos: list[ContentItem],
    all_shorts: list[ContentItem],
    top_videos: list[ContentItem],
    top_shorts: list[ContentItem],
    top_percent: float,
    rank_by: str,
    from_date: Optional[date],
    to_date: Optional[date],
    output_dir: Path,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "channel_report.md"

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    video_stats = _stats(all_videos)
    short_stats = _stats(all_shorts)
    date_range = f"{from_date or 'any'} -> {to_date or 'any'}"

    body = f"""# Channel Performance Report: {channel_name}

> Generated: {generated_at}
> Ranking method: **{rank_by}**
> Top percent selected: **{top_percent}%**
> Date range: **{date_range}**

---

## Overview

| Metric | Videos | Shorts |
|--------|--------|--------|
| Total analyzed | {format_number(video_stats['count'])} | {format_number(short_stats['count'])} |
| Total views | {format_number(video_stats['total_views'])} | {format_number(short_stats['total_views'])} |
| Total likes | {format_number(video_stats['total_likes'])} | {format_number(short_stats['total_likes'])} |
| Total comments | {format_number(video_stats['total_comments'])} | {format_number(short_stats['total_comments'])} |
| Avg views/item | {format_number(video_stats['avg_views'])} | {format_number(short_stats['avg_views'])} |
| Avg likes/item | {format_number(video_stats['avg_likes'])} | {format_number(short_stats['avg_likes'])} |
| Avg engagement | {video_stats['avg_engagement']:.2f}% | {short_stats['avg_engagement']:.2f}% |
| Selected top items | {format_number(len(top_videos))} | {format_number(len(top_shorts))} |

---

## Transcript Coverage

Videos: {_transcript_summary(top_videos)}

Shorts: {_transcript_summary(top_shorts)}

---

## Top {top_percent}% Videos

{_top_table(top_videos)}

---

## Top {top_percent}% Shorts

{_top_table(top_shorts)}

---

## Top Tags - Videos

{_tags_section(top_videos)}

## Top Tags - Shorts

{_tags_section(top_shorts)}
"""

    write_text(report_path, body)
    logger.info("report.complete path=%s", report_path)
    return report_path


def export_csv(items: list[ContentItem], filepath: Path) -> Path:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "rank",
        "title",
        "type",
        "date",
        "views",
        "likes",
        "comments",
        "duration",
        "score",
        "engagement_rate",
        "norm_views",
        "norm_likes",
        "norm_comments",
        "norm_engagement",
        "transcript_status",
        "transcript_source",
        "transcript_language",
        "transcript_chars",
        "transcript_error",
        "tags",
        "category",
        "url",
    ]
    with filepath.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for rank, item in enumerate(items, 1):
            writer.writerow(
                {
                    "rank": rank,
                    "title": item.title,
                    "type": item.type,
                    "date": output_date(item).strftime("%Y-%m-%d") if output_date(item) else "",
                    "views": item.views,
                    "likes": item.likes,
                    "comments": item.comments,
                    "duration": item.duration,
                    "score": item.score,
                    "engagement_rate": item.score_components.engagement_rate,
                    "norm_views": item.score_components.norm_views,
                    "norm_likes": item.score_components.norm_likes,
                    "norm_comments": item.score_components.norm_comments,
                    "norm_engagement": item.score_components.norm_engagement,
                    "transcript_status": item.transcript.status,
                    "transcript_source": item.transcript.source,
                    "transcript_language": item.transcript.language,
                    "transcript_chars": item.transcript.characters,
                    "transcript_error": item.transcript.error,
                    "tags": "|".join(item.tags),
                    "category": item.category,
                    "url": item.url,
                }
            )
    logger.info("csv.complete path=%s rows=%s", filepath, len(items))
    return filepath
