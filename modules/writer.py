"""
writer.py — Production-grade markdown file generation.
Includes: thumbnail, tags, chapters, top comments, full score breakdown,
          engagement metrics, like ratio, comment ratio.
"""

import logging
import os
import re
import unicodedata
from datetime import date

logger = logging.getLogger(__name__)

MAX_FILENAME_LENGTH = 100


def _slugify(text: str, max_len: int = MAX_FILENAME_LENGTH) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-]", " ", text)
    text = re.sub(r"[\s\-]+", "-", text)
    text = text.strip("-")
    return text[:max_len]


def _build_filename(item: dict) -> str:
    slug = _slugify(item.get("title", "untitled"))
    d = item.get("date")
    date_str = d.strftime("%Y-%m-%d") if isinstance(d, date) else "no-date"
    return f"{slug}-{date_str}.md"


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
    lines = []
    for ch in chapters:
        start = _dur(ch.get("start", 0))
        lines.append(f"- `{start}` — {ch.get('title', '')}")
    return "\n".join(lines)


def _render_top_comments(comments: list[dict]) -> str:
    if not comments:
        return "_No comment data available._"
    lines = []
    for i, c in enumerate(comments, 1):
        pinned = " 📌 **Pinned**" if c.get("is_pinned") else ""
        likes = c.get("likes", 0)
        like_str = f" · 👍 {_fmt(likes)}" if likes else ""
        author = c.get("author", "Unknown")
        text = (c.get("text") or "").replace("\n", " ").strip()
        if len(text) > 300:
            text = text[:297] + "…"
        lines.append(f"**{i}. {author}**{pinned}{like_str}  \n> {text}\n")
    return "\n".join(lines)


def _render_tags(tags: list[str]) -> str:
    if not tags:
        return "_No tags._"
    return " ".join(f"`{t}`" for t in tags[:40])


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
    description   = item.get("description", "").strip() or "_No description provided._"
    transcript    = item.get("transcript", "Transcript not available").strip()
    chapters      = item.get("chapters", [])
    top_comments  = item.get("top_comments", [])
    tags          = item.get("tags", [])

    comp = item.get("_score_components", {})
    rank_by = comp.get("rank_by", "weighted")

    thumbnail_block = f"![Thumbnail]({thumbnail})\n\n" if thumbnail else ""

    breakdown = f"""| Component | Raw | Normalized |
|-----------|-----|------------|
| Views | {_fmt(item.get('views',0))} | `{comp.get('norm_views', 0):.4f}` |
| Likes | {_fmt(item.get('likes',0))} | `{comp.get('norm_likes', 0):.4f}` |
| Comments | {_fmt(item.get('comments',0))} | `{comp.get('norm_comments', 0):.4f}` |
| Engagement rate | `{comp.get('engagement_rate', 0):.6f}` | `{comp.get('norm_engagement', 0):.4f}` |
| **Final score** | | **`{score:.6f}`** |

> Ranked by: **{rank_by}**  
> Formula: `0.5×views + 0.2×likes + 0.1×comments + 0.2×engagement`"""

    return f"""{thumbnail_block}# {title}

---

## 📊 Performance Metrics

| Field | Value |
|-------|-------|
| **Score** | `{score:.6f}` |
| **Date** | {date_str} |
| **Type** | {video_type} |
| **Duration** | {duration} |
| **Views** | {views} |
| **Likes** | {likes} |
| **Comments** | {comments} |
| **Like ratio** | {like_ratio} |
| **Comment ratio** | {comment_ratio} |
| **Category** | {category} |
| **Language** | {language} |
| **Channel** | [{channel}]({channel_url}) |
| **Subscribers** | {subscribers} |
| **URL** | [Watch on YouTube]({url}) |

---

## 🧮 Score Breakdown

{breakdown}

---

## 🏷️ Tags

{_render_tags(tags)}

---

## 📖 Description

{description}

---

## 🎬 Chapters

{_render_chapters(chapters)}

---

## 💬 Top Comments

{_render_top_comments(top_comments)}

---

## 📝 Transcript

{transcript}
"""


def write_item(item: dict, output_dir: str, dedup_tracker: set = None) -> str:
    os.makedirs(output_dir, exist_ok=True)
    if dedup_tracker is None:
        dedup_tracker = set()
    base_name = _build_filename(item)
    final_name = base_name
    counter = 1
    while final_name in dedup_tracker:
        stem = base_name[:-3]
        final_name = f"{stem}-{counter}.md"
        counter += 1
    dedup_tracker.add(final_name)
    filepath = os.path.join(output_dir, final_name)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(_render_markdown(item))
    logger.debug(f"Wrote: {filepath}")
    return filepath


def write_all(items: list[dict], output_dir: str, progress_callback=None) -> list[str]:
    os.makedirs(output_dir, exist_ok=True)
    dedup_tracker = set()
    written = []
    total = len(items)
    for idx, item in enumerate(items, 1):
        if progress_callback:
            progress_callback(idx, total, item.get("title", ""))
        written.append(write_item(item, output_dir, dedup_tracker))
    logger.info(f"Wrote {len(written)} files → {output_dir}")
    return written
