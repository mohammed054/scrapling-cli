"""
reporter.py — Channel-level summary report + CSV export.
Generates a master channel_report.md and scored_videos.csv.
"""

import csv
import logging
import os
from datetime import date, datetime
from typing import Optional

logger = logging.getLogger(__name__)


def _fmt(n) -> str:
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)


def _dur(seconds: int) -> str:
    try:
        s = int(seconds)
        h, rem = divmod(s, 3600)
        m, sec = divmod(rem, 60)
        return f"{h}:{m:02d}:{sec:02d}" if h else f"{m}:{sec:02d}"
    except Exception:
        return "?"


def generate_channel_report(
    channel_name: str,
    all_videos: list[dict],
    all_shorts: list[dict],
    top_videos: list[dict],
    top_shorts: list[dict],
    top_percent: float,
    rank_by: str,
    from_date: Optional[date],
    to_date: Optional[date],
    output_dir: str,
) -> str:
    """Write a comprehensive channel_report.md to output_dir."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "channel_report.md")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_items = len(all_videos) + len(all_shorts)

    # ── aggregate stats ──
    def stats(items: list[dict]) -> dict:
        if not items:
            return {"count": 0, "total_views": 0, "total_likes": 0,
                    "total_comments": 0, "avg_views": 0, "avg_likes": 0,
                    "avg_engagement": 0, "top_video": None}
        total_v = sum(i.get("views", 0) for i in items)
        total_l = sum(i.get("likes", 0) for i in items)
        total_c = sum(i.get("comments", 0) for i in items)
        avg_eng = (
            sum(
                (i.get("likes", 0) + i.get("comments", 0)) / max(i.get("views", 1), 1)
                for i in items
            ) / len(items) * 100
        )
        top = max(items, key=lambda x: x.get("views", 0))
        return {
            "count": len(items),
            "total_views": total_v,
            "total_likes": total_l,
            "total_comments": total_c,
            "avg_views": total_v // len(items),
            "avg_likes": total_l // len(items),
            "avg_engagement": avg_eng,
            "top_video": top,
        }

    vs = stats(all_videos)
    ss = stats(all_shorts)
    ts_v = stats(top_videos)
    ts_s = stats(top_shorts)

    def top_table(items: list[dict], limit: int = 20) -> str:
        if not items:
            return "_No items._\n"
        rows = ["| # | Title | Date | Views | Likes | Comments | Duration | Score |",
                "|---|-------|------|-------|-------|----------|----------|-------|"]
        for i, item in enumerate(items[:limit], 1):
            d = item.get("date")
            date_str = d.strftime("%Y-%m-%d") if d else "?"
            rows.append(
                f"| {i} | [{item.get('title','')[:55]}]({item.get('url','')}) "
                f"| {date_str} | {_fmt(item.get('views',0))} "
                f"| {_fmt(item.get('likes',0))} | {_fmt(item.get('comments',0))} "
                f"| {_dur(item.get('duration',0))} | `{item.get('score',0):.4f}` |"
            )
        return "\n".join(rows) + "\n"

    def tags_section(items: list[dict]) -> str:
        """Aggregate top tags across all top items."""
        from collections import Counter
        tag_counter: Counter = Counter()
        for item in items:
            for tag in item.get("tags", []):
                tag_counter[tag.lower()] += 1
        if not tag_counter:
            return "_No tag data available._"
        top_tags = tag_counter.most_common(30)
        return ", ".join(f"`{tag}` ({count})" for tag, count in top_tags)

    date_range = f"{from_date or 'any'} → {to_date or 'any'}"

    report = f"""# 📊 Channel Performance Report: {channel_name}

> Generated: {now}  
> Ranking method: **{rank_by}**  
> Top percent selected: **{top_percent}%**  
> Date range: **{date_range}**

---

## 📈 Channel Overview

| Metric | Videos | Shorts |
|--------|--------|--------|
| Total analyzed | {_fmt(vs['count'])} | {_fmt(ss['count'])} |
| Total views | {_fmt(vs['total_views'])} | {_fmt(ss['total_views'])} |
| Total likes | {_fmt(vs['total_likes'])} | {_fmt(ss['total_likes'])} |
| Total comments | {_fmt(vs['total_comments'])} | {_fmt(ss['total_comments'])} |
| Avg views/video | {_fmt(vs['avg_views'])} | {_fmt(ss['avg_views'])} |
| Avg likes/video | {_fmt(vs['avg_likes'])} | {_fmt(ss['avg_likes'])} |
| Avg engagement rate | {vs['avg_engagement']:.2f}% | {ss['avg_engagement']:.2f}% |
| **Top {top_percent}% selected** | **{_fmt(len(top_videos))}** | **{_fmt(len(top_shorts))}** |

---

## 🏆 Top {top_percent}% Videos

{top_table(top_videos)}

---

## ⚡ Top {top_percent}% Shorts

{top_table(top_shorts)}

---

## 🏷️ Top Tags (Videos)

{tags_section(top_videos)}

## 🏷️ Top Tags (Shorts)

{tags_section(top_shorts)}

---

## 📂 Output Structure

```
output/{channel_name}/
  channel_report.md        ← this file
  scored_videos.csv        ← full scored dataset (videos)
  scored_shorts.csv        ← full scored dataset (shorts)
  videos/                  ← top {top_percent}% video markdown files
  shorts/                  ← top {top_percent}% shorts markdown files
```

---

*Report generated by scrapling-cli*
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report)

    logger.info(f"Channel report written: {filepath}")
    return filepath


def export_csv(items: list[dict], filepath: str) -> str:
    """Export full scored dataset to CSV."""
    if not items:
        return filepath

    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

    fields = [
        "rank", "title", "type", "date", "views", "likes", "comments",
        "duration", "score", "engagement_rate", "norm_views", "norm_likes",
        "norm_comments", "norm_engagement", "tags", "category", "url",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for rank, item in enumerate(items, 1):
            comp = item.get("_score_components", {})
            d = item.get("date")
            writer.writerow({
                "rank": rank,
                "title": item.get("title", ""),
                "type": item.get("type", ""),
                "date": d.strftime("%Y-%m-%d") if d else "",
                "views": item.get("views", 0),
                "likes": item.get("likes", 0),
                "comments": item.get("comments", 0),
                "duration": item.get("duration", 0),
                "score": item.get("score", 0),
                "engagement_rate": comp.get("engagement_rate", 0),
                "norm_views": comp.get("norm_views", 0),
                "norm_likes": comp.get("norm_likes", 0),
                "norm_comments": comp.get("norm_comments", 0),
                "norm_engagement": comp.get("norm_engagement", 0),
                "tags": "|".join(item.get("tags", [])),
                "category": item.get("category", ""),
                "url": item.get("url", ""),
            })

    logger.info(f"CSV exported: {filepath} ({len(items)} rows)")
    return filepath
