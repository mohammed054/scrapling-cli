"""
writer.py — Markdown file generation for top-performing videos.
Includes: thumbnail, tags, chapters, comments, score breakdown, engagement metrics.
"""

import logging
import os
import re
import unicodedata
from datetime import date

logger = logging.getLogger(__name__)

MAX_FILENAME_LEN = 100


# ─────────────────────────────────────────────────────────────────────────────
# Formatting helpers
# ─────────────────────────────────────────────────────────────────────────────

def _slugify(text: str, max_len: int = MAX_FILENAME_LEN) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    text = re.sub(r"[\s\-]+", "-", text).strip("-")
    return text[:max_len]


def _build_filename(item: dict) -> str:
    slug = _slugify(item.get("title", "untitled"))
    d = item.get("date")
    ds = d.strftime("%Y-%m-%d") if isinstance(d, date) else "no-date"
    return f"{slug}-{ds}.md"


def _fmt(n) -> str:
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)


def _dur(seconds) -> str:
    try:
        s = int(seconds)
        h, rem = divmod(s, 3600)
        m, sec = divmod(rem, 60)
        return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"
    except Exception:
        return "unknown"


def _render_chapters(chapters: list[dict]) -> str:
    if not chapters:
        return "_No chapter markers._"
    return "\n".join(
        f"- `{_dur(ch.get('start', 0))}` — {ch.get('title', '')}"
        for ch in chapters
    )


def _render_comments(comments: list[dict]) -> str:
    if not comments:
        return "_No comment data available._"
    lines = []
    for i, c in enumerate(comments, 1):
        pinned  = " 📌 **Pinned**" if c.get("is_pinned") else ""
        likes   = c.get("likes", 0)
        lstr    = f" · 👍 {_fmt(likes)}" if likes else ""
        author  = c.get("author", "Unknown")
        text    = (c.get("text") or "").replace("\n", " ").strip()[:300]
        lines.append(f"**{i}. {author}**{pinned}{lstr}  \n> {text}\n")
    return "\n".join(lines)


def _render_tags(tags: list[str]) -> str:
    if not tags:
        return "_No tags._"
    return " ".join(f"`{t}`" for t in tags[:40])


# ─────────────────────────────────────────────────────────────────────────────
# Markdown renderer
# ─────────────────────────────────────────────────────────────────────────────

def _render_markdown(item: dict) -> str:
    title         = item.get("title", "Untitled")
    d             = item.get("date")
    date_str      = d.strftime("%Y-%m-%d") if isinstance(d, date) else "Unknown"
    video_type    = item.get("type", "video").capitalize()
    duration      = _dur(item.get("duration", 0))
    views         = _fmt(item.get("views", 0))
    likes         = _fmt(item.get("likes", 0))
    comments      = _fmt(item.get("comments", 0))
    like_ratio    = f"{item.get('like_ratio', 0):.3f}%"
    comment_ratio = f"{item.get('comment_ratio', 0):.4f}%"
    score         = item.get("score", 0.0)
    url           = item.get("url", "")
    channel       = item.get("channel", "")
    channel_url   = item.get("channel_url", "")
    subscribers   = _fmt(item.get("subscribers", 0))
    category      = item.get("category", "") or "—"
    language      = item.get("language", "") or "—"
    thumbnail     = item.get("thumbnail", "")
    description   = (item.get("description") or "").strip() or "_No description provided._"
    transcript    = (item.get("transcript") or "Transcript not available").strip()

    comp    = item.get("_score_components", {})
    rank_by = comp.get("rank_by", "weighted")

    thumb_block = f"![Thumbnail]({thumbnail})\n\n" if thumbnail else ""

    breakdown = (
        f"| Component | Raw | Normalised |\n"
        f"|-----------|-----|------------|\n"
        f"| Views | {_fmt(item.get('views',0))} | `{comp.get('norm_views',0):.4f}` |\n"
        f"| Likes | {_fmt(item.get('likes',0))} | `{comp.get('norm_likes',0):.4f}` |\n"
        f"| Comments | {_fmt(item.get('comments',0))} | `{comp.get('norm_comments',0):.4f}` |\n"
        f"| Engagement rate | `{comp.get('engagement_rate',0):.6f}` | `{comp.get('norm_engagement',0):.4f}` |\n"
        f"| **Final score** | | **`{score:.6f}`** |\n\n"
        f"> Ranked by: **{rank_by}**  \n"
        f"> Formula: `0.5×views + 0.2×likes + 0.1×comments + 0.2×engagement`"
    )

    return (
        f"{thumb_block}"
        f"# {title}\n\n"
        f"---\n\n"
        f"## 📊 Performance Metrics\n\n"
        f"| Field | Value |\n"
        f"|-------|-------|\n"
        f"| **Score** | `{score:.6f}` |\n"
        f"| **Date** | {date_str} |\n"
        f"| **Type** | {video_type} |\n"
        f"| **Duration** | {duration} |\n"
        f"| **Views** | {views} |\n"
        f"| **Likes** | {likes} |\n"
        f"| **Comments** | {comments} |\n"
        f"| **Like ratio** | {like_ratio} |\n"
        f"| **Comment ratio** | {comment_ratio} |\n"
        f"| **Category** | {category} |\n"
        f"| **Language** | {language} |\n"
        f"| **Channel** | [{channel}]({channel_url}) |\n"
        f"| **Subscribers** | {subscribers} |\n"
        f"| **URL** | [Watch on YouTube]({url}) |\n\n"
        f"---\n\n"
        f"## 🧮 Score Breakdown\n\n"
        f"{breakdown}\n\n"
        f"---\n\n"
        f"## 🏷️ Tags\n\n"
        f"{_render_tags(item.get('tags', []))}\n\n"
        f"---\n\n"
        f"## 📖 Description\n\n"
        f"{description}\n\n"
        f"---\n\n"
        f"## 🎬 Chapters\n\n"
        f"{_render_chapters(item.get('chapters', []))}\n\n"
        f"---\n\n"
        f"## 💬 Top Comments\n\n"
        f"{_render_comments(item.get('top_comments', []))}\n\n"
        f"---\n\n"
        f"## 📝 Transcript\n\n"
        f"{transcript}\n"
    )


# ─────────────────────────────────────────────────────────────────────────────
# File I/O
# ─────────────────────────────────────────────────────────────────────────────

def write_item(item: dict, output_dir: str, dedup: set = None) -> str:
    os.makedirs(output_dir, exist_ok=True)
    if dedup is None:
        dedup = set()

    base = _build_filename(item)
    final = base
    counter = 1
    while final in dedup:
        final = f"{base[:-3]}-{counter}.md"
        counter += 1
    dedup.add(final)

    path = os.path.join(output_dir, final)
    with open(path, "w", encoding="utf-8") as f:
        f.write(_render_markdown(item))
    logger.debug(f"Wrote: {path}")
    return path


def write_all(
    items: list[dict],
    output_dir: str,
    progress_callback=None,
) -> list[str]:
    os.makedirs(output_dir, exist_ok=True)
    dedup: set[str] = set()
    written: list[str] = []
    for idx, item in enumerate(items, 1):
        if progress_callback:
            progress_callback(idx, len(items), item.get("title", ""))
        written.append(write_item(item, output_dir, dedup))
    logger.info(f"Wrote {len(written)} files → {output_dir}")
    return written
