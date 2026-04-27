from __future__ import annotations

import logging
from pathlib import Path

from .models import ContentItem
from .utils import (
    build_filename,
    format_duration,
    format_number,
    output_date,
    prune_markdown_files,
    repair_text,
    write_text,
)

logger = logging.getLogger(__name__)


def _render_tags(tags: list[str]) -> str:
    if not tags:
        return "_No tags._"
    return " ".join(f"`{repair_text(tag)}`" for tag in tags[:40])


def _render_chapters(chapters: list[dict]) -> str:
    if not chapters:
        return "_No chapter markers._"
    return "\n".join(
        f"- `{format_duration(chapter.get('start', 0))}` - {repair_text(chapter.get('title', '').strip())}"
        for chapter in chapters
    )


def _render_comments(comments: list[dict]) -> str:
    if not comments:
        return "_No comment data available._"
    lines: list[str] = []
    for index, comment in enumerate(comments, 1):
        pinned = " (Pinned)" if comment.get("is_pinned") else ""
        likes = comment.get("likes", 0)
        like_text = f" - {format_number(likes)} likes" if likes else ""
        author = repair_text(comment.get("author", "Unknown"))
        text = repair_text((comment.get("text") or "").replace("\n", " ").strip())[:300]
        lines.append(f"**{index}. {author}**{pinned}{like_text}\n> {text}\n")
    return "\n".join(lines)


def _render_transcript_section(item: ContentItem) -> str:
    transcript = item.transcript
    source = repair_text(transcript.source) or "none"
    language = repair_text(transcript.language) or "unknown"
    chars = transcript.characters if transcript.characters else 0
    error = repair_text(transcript.error) or "none"
    header = (
        "| Field | Value |\n"
        "|-------|-------|\n"
        f"| **Status** | `{transcript.status}` |\n"
        f"| **Source** | `{source}` |\n"
        f"| **Language** | `{language}` |\n"
        f"| **Characters** | `{chars}` |\n"
        f"| **Error** | `{error}` |\n"
    )
    if transcript.status == "available" and transcript.text:
        body = repair_text(transcript.text.strip())
    else:
        body = "> No transcript text was recovered for this item."
    return f"{header}\n\n{body}\n"


def render_markdown(item: ContentItem, *, include_score_details: bool) -> str:
    exact_date = output_date(item)
    date_text = exact_date.strftime("%Y-%m-%d") if exact_date else "Unknown"
    description = repair_text(item.description).strip() or "_No description provided._"
    thumbnail_block = f"![Thumbnail]({item.thumbnail})\n\n" if item.thumbnail else ""

    sections = [
        thumbnail_block + f"# {repair_text(item.title)}\n",
        "---\n\n## Info\n\n"
        "| Field | Value |\n"
        "|-------|-------|\n"
        f"| **Date** | {date_text} |\n"
        f"| **Type** | {item.type.capitalize()} |\n"
        f"| **Duration** | {format_duration(item.duration)} |\n"
        f"| **Views** | {format_number(item.views)} |\n"
        f"| **Likes** | {format_number(item.likes)} |\n"
        f"| **Comments** | {format_number(item.comments)} |\n"
        f"| **Like ratio** | {item.like_ratio:.4f}% |\n"
        f"| **Comment ratio** | {item.comment_ratio:.4f}% |\n"
        f"| **Channel** | [{repair_text(item.channel)}]({item.channel_url}) |\n"
        f"| **Subscribers** | {format_number(item.subscribers)} |\n"
        f"| **URL** | [Watch on YouTube]({item.url}) |\n"
        f"| **Category** | {repair_text(item.category) or '-'} |\n"
        f"| **Language** | {repair_text(item.language) or '-'} |\n",
    ]

    if include_score_details:
        components = item.score_components
        sections.append(
            "---\n\n## Score\n\n"
            "| Component | Raw | Normalized |\n"
            "|-----------|-----|------------|\n"
            f"| Views | {format_number(item.views)} | `{components.norm_views:.4f}` |\n"
            f"| Likes | {format_number(item.likes)} | `{components.norm_likes:.4f}` |\n"
            f"| Comments | {format_number(item.comments)} | `{components.norm_comments:.4f}` |\n"
            f"| Engagement rate | `{components.engagement_rate:.6f}` | `{components.norm_engagement:.4f}` |\n"
            f"| **Final score** | | **`{item.score:.6f}`** |\n\n"
            f"> Ranked by: **{components.rank_by}**\n"
        )

    sections.extend(
        [
            f"---\n\n## Tags\n\n{_render_tags(item.tags)}\n",
            f"---\n\n## Description\n\n{description}\n",
            f"---\n\n## Chapters\n\n{_render_chapters(item.chapters)}\n",
            f"---\n\n## Top Comments\n\n{_render_comments(item.top_comments)}\n",
            f"---\n\n## Transcript\n\n{_render_transcript_section(item)}",
        ]
    )

    return "\n".join(section.rstrip() for section in sections if section).rstrip() + "\n"


def write_item(
    item: ContentItem,
    output_dir: Path,
    *,
    dedup: set[str] | None = None,
    include_score_details: bool,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    dedup = dedup or set()
    base_name = build_filename(item)
    final_name = base_name
    counter = 1
    while final_name in dedup:
        final_name = f"{base_name[:-3]}-{counter}.md"
        counter += 1
    dedup.add(final_name)
    destination = output_dir / final_name
    write_text(destination, render_markdown(item, include_score_details=include_score_details))
    logger.debug("markdown.write path=%s", destination)
    return destination


def write_items(
    items: list[ContentItem],
    output_dir: Path,
    *,
    include_score_details: bool,
    progress_callback=None,
    prune_existing: bool = False,
) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if prune_existing:
        prune_markdown_files(output_dir)
    written: list[Path] = []
    dedup: set[str] = set()
    for index, item in enumerate(items, 1):
        if progress_callback:
            progress_callback(index, len(items), item.title)
        written.append(
            write_item(
                item,
                output_dir,
                dedup=dedup,
                include_score_details=include_score_details,
            )
        )
    logger.info("markdown.complete output_dir=%s files=%s", output_dir, len(written))
    return written
