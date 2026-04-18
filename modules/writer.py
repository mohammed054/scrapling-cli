"""
writer.py — Markdown file generation for top-performing videos.
Handles filename normalization and directory structure creation.
"""

import logging
import os
import re
import unicodedata
from datetime import date
from typing import Optional

logger = logging.getLogger(__name__)

MAX_FILENAME_LENGTH = 100  # characters (excluding .md)


def _slugify(text: str, max_len: int = MAX_FILENAME_LENGTH) -> str:
    """
    Convert a title to a clean filename-safe slug.
    - Lowercase
    - Replace spaces → hyphens
    - Remove special characters
    - Trim to max_len
    """
    # Normalize unicode (e.g. accents)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    # Replace non-alphanumeric/space/hyphen with space
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    # Collapse whitespace and replace with hyphens
    text = re.sub(r"[\s\-]+", "-", text)
    text = text.strip("-")
    return text[:max_len]


def _build_filename(item: dict) -> str:
    """Build filename: {slug}-{date}.md"""
    slug = _slugify(item.get("title", "untitled"))
    upload_date = item.get("date")
    date_str = upload_date.strftime("%Y-%m-%d") if isinstance(upload_date, date) else "no-date"
    return f"{slug}-{date_str}.md"


def _format_number(n: int) -> str:
    """Format large numbers with commas."""
    try:
        return f"{int(n):,}"
    except (TypeError, ValueError):
        return str(n)


def _duration_str(seconds: int) -> str:
    """Convert seconds to MM:SS or HH:MM:SS."""
    try:
        s = int(seconds)
        h, rem = divmod(s, 3600)
        m, sec = divmod(rem, 60)
        if h:
            return f"{h}:{m:02d}:{sec:02d}"
        return f"{m}:{sec:02d}"
    except Exception:
        return "unknown"


def _render_markdown(item: dict) -> str:
    """Render a full markdown file from a VideoRecord dict."""
    title = item.get("title", "Untitled")
    date_val = item.get("date")
    date_str = date_val.strftime("%Y-%m-%d") if isinstance(date_val, date) else "Unknown"
    views = _format_number(item.get("views", 0))
    likes = _format_number(item.get("likes", 0))
    comments = _format_number(item.get("comments", 0))
    score = item.get("score", 0.0)
    url = item.get("url", "")
    duration = _duration_str(item.get("duration", 0))
    content_type = item.get("type", "video").capitalize()
    description = item.get("description", "").strip() or "_No description provided._"
    transcript = item.get("transcript", "Transcript not available").strip()

    # Score breakdown block
    components = item.get("_score_components", {})
    breakdown_lines = ""
    if components:
        breakdown_lines = (
            "\n"
            f"  - Views (normalized): {components.get('norm_views', 0):.4f}\n"
            f"  - Likes (normalized): {components.get('norm_likes', 0):.4f}\n"
            f"  - Comments (normalized): {components.get('norm_comments', 0):.4f}\n"
            f"  - Engagement rate: {components.get('engagement_rate', 0):.6f}\n"
            f"  - Engagement (normalized): {components.get('norm_engagement', 0):.4f}"
        )

    return f"""# {title}

## Metadata

| Field | Value |
|-------|-------|
| **Date** | {date_str} |
| **Type** | {content_type} |
| **Duration** | {duration} |
| **Views** | {views} |
| **Likes** | {likes} |
| **Comments** | {comments} |
| **Performance Score** | `{score:.6f}` |
| **URL** | {url} |

### Score Breakdown
{breakdown_lines}

---

## Description

{description}

---

## Transcript

{transcript}
"""


def write_item(item: dict, output_dir: str, dedup_tracker: Optional[set] = None) -> str:
    """
    Write a single VideoRecord to a markdown file.

    Returns the path of the written file.
    Handles duplicate filenames by appending a counter.
    """
    os.makedirs(output_dir, exist_ok=True)

    if dedup_tracker is None:
        dedup_tracker = set()

    base_name = _build_filename(item)

    # Deduplicate filenames
    final_name = base_name
    counter = 1
    while final_name in dedup_tracker:
        stem = base_name[:-3]  # remove .md
        final_name = f"{stem}-{counter}.md"
        counter += 1

    dedup_tracker.add(final_name)
    filepath = os.path.join(output_dir, final_name)

    content = _render_markdown(item)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    logger.debug(f"Wrote: {filepath}")
    return filepath


def write_all(
    items: list[dict],
    output_dir: str,
    progress_callback=None,
) -> list[str]:
    """Write all items to markdown files. Returns list of written paths."""
    os.makedirs(output_dir, exist_ok=True)
    dedup_tracker = set()
    written_paths = []
    total = len(items)

    for idx, item in enumerate(items, 1):
        if progress_callback:
            progress_callback(idx, total, item.get("title", ""))
        path = write_item(item, output_dir, dedup_tracker)
        written_paths.append(path)

    logger.info(f"Wrote {len(written_paths)} files to: {output_dir}")
    return written_paths
