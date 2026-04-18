"""
writer.py — Markdown file generator.

Handles:
  - Clean filename normalization (lowercase, no special chars, max 100 chars)
  - Directory creation
  - Duplicate filename detection
  - Full markdown template from blueprint spec
"""

import logging
import re
from pathlib import Path
from typing import List

log = logging.getLogger(__name__)

# Maximum filename length (excluding .md extension)
MAX_FILENAME_LEN = 100


class MarkdownWriter:
    """
    Writes top-scoring videos/shorts to .md files in organized directories.

    Output structure:
        {output_root}/{channel_name}/videos/
        {output_root}/{channel_name}/shorts/
    """

    def __init__(self, output_root: str, channel_name: str):
        self.root = Path(output_root) / channel_name
        self._used_filenames: set = set()

    def write_batch(self, items: List[dict], content_type: str) -> List[Path]:
        """
        Write all items for a given content type.
        Returns list of written paths.
        """
        if not items:
            return []

        out_dir = self.root / content_type
        out_dir.mkdir(parents=True, exist_ok=True)
        log.info(f"Writing {len(items)} {content_type} to {out_dir}")

        paths = []
        for item in items:
            try:
                path = self._write_item(item, out_dir)
                paths.append(path)
            except Exception as e:
                log.warning(f"Failed to write '{item.get('title', '?')}': {e}")

        return paths

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _write_item(self, item: dict, out_dir: Path) -> Path:
        filename = self._make_filename(item)
        path = out_dir / filename

        content = self._render(item)
        path.write_text(content, encoding="utf-8")
        log.debug(f"Wrote: {path}")
        return path

    def _render(self, item: dict) -> str:
        """Render item dict into the blueprint markdown template."""
        date_str  = self._fmt_date(item.get("date"))
        views     = self._fmt_number(item.get("views", 0))
        likes     = self._fmt_number(item.get("likes", 0))
        comments  = self._fmt_number(item.get("comments", 0))
        score     = f"{item.get('score', 0.0):.4f}"
        url       = item.get("url", "")
        title     = item.get("title", "Untitled")
        desc      = item.get("description") or "_No description provided._"
        transcript= item.get("transcript") or "Transcript not available"
        duration  = self._fmt_duration(item.get("duration", 0))
        ctype     = item.get("type", "video").capitalize()

        return f"""# {title}

- **Type:** {ctype}
- **Date:** {date_str}
- **Duration:** {duration}
- **Views:** {views}
- **Likes:** {likes}
- **Comments:** {comments}
- **Score:** {score}
- **URL:** {url}

---

## Description

{desc}

---

## Transcript

{transcript}
"""

    def _make_filename(self, item: dict) -> str:
        """
        Generate a safe, unique filename from title + date.
        Example: what-is-erp-software-here-is-everything-you-need-to-know-2020-08-03.md
        """
        title = item.get("title", "untitled")
        date  = self._fmt_date(item.get("date"))

        slug = self._slugify(title)
        base = f"{slug}-{date}"

        # Ensure uniqueness
        candidate = base
        counter = 2
        while candidate in self._used_filenames:
            candidate = f"{base}-{counter}"
            counter += 1

        self._used_filenames.add(candidate)
        return candidate + ".md"

    @staticmethod
    def _slugify(text: str) -> str:
        """Convert title to lowercase kebab-case, max MAX_FILENAME_LEN chars."""
        text = text.lower()
        text = re.sub(r"[^\w\s-]", "", text)        # remove special chars
        text = re.sub(r"[\s_]+", "-", text)          # spaces → dashes
        text = re.sub(r"-{2,}", "-", text)            # collapse multiple dashes
        text = text.strip("-")
        return text[:MAX_FILENAME_LEN]

    @staticmethod
    def _fmt_date(date_obj) -> str:
        if not date_obj:
            return "unknown"
        try:
            return date_obj.strftime("%Y-%m-%d")
        except Exception:
            return str(date_obj)[:10]

    @staticmethod
    def _fmt_number(n) -> str:
        try:
            return f"{int(n):,}"
        except (TypeError, ValueError):
            return "0"

    @staticmethod
    def _fmt_duration(seconds: int) -> str:
        if not seconds:
            return "Unknown"
        m, s = divmod(int(seconds), 60)
        h, m = divmod(m, 60)
        if h:
            return f"{h}h {m}m {s}s"
        return f"{m}m {s}s"
