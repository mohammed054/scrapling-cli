"""
reporter.py — Channel-level summary report (Markdown) + CSV export.
"""

import csv
import logging
import os
from collections import Counter
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


def _stats(items: list[dict]) -> dict:
    if not items:
        return {"count": 0, "total_views": 0, "total_likes": 0,
                "total_comments": 0, "avg_views": 0, "avg_likes": 0,
                "avg_engagement": 0.0, "top": None}
    tv = sum(i.get("views", 0)    for i in items)
    tl = sum(i.get("likes", 0)    for i in items)
    tc = sum(i.get("comments", 0) for i in items)
    ae = sum(
        (i.get("likes", 0) + i.get("comments", 0)) / max(i.get("views", 1), 1)
        for i in items
    ) / len(items) * 100
    return {
        "count": len(items),
        "total_views":    tv,
        "total_likes":    tl,
        "total_comments": tc,
        "avg_views":      tv // len(items),
        "avg_likes":      tl // len(items),
        "avg_engagement": ae,
        "top":            max(items, key=lambda x: x.get("views", 0)),
    }


def _top_table(items: list[dict], limit: int = 25) -> str:
    if not items:
        return "_No items._\n"
    rows = [
        "| # | Title | Date | Views | Likes | Duration | Score |",
        "|---|-------|------|-------|-------|----------|-------|",
    ]
    for i, item in enumerate(items[:limit], 1):
        d = item.get("date")
        ds = d.strftime("%Y-%m-%d") if d else "?"
        rows.append(
            f"| {i} | [{item.get('title','')[:55]}]({item.get('url','')}) "
            f"| {ds} | {_fmt(item.get('views',0))} "
            f"| {_fmt(item.get('likes',0))} "
            f"| {_dur(item.get('duration',0))} | `{item.get('score',0):.4f}` |"
        )
    return "\n".join(rows) + "\n"


def _tags_section(items: list[dict]) -> str:
    counter: Counter = Counter()
    for item in items:
        for tag in item.get("tags", []):
            counter[tag.lower()] += 1
    if not counter:
        return "_No tag data._"
    return ", ".join(f"`{t}` ({n})" for t, n in counter.most_common(30))


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
    os.makedirs(output_dir, exist_ok=True)
    fp = os.path.join(output_dir, "channel_report.md")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    vs  = _stats(all_videos)
    ss  = _stats(all_shorts)
    dr  = f"{from_date or 'any'} → {to_date or 'any'}"

    report = f"""# 📊 Channel Performance Report: {channel_name}

> Generated: {now}
> Ranking method: **{rank_by}**
> Top percent selected: **{top_percent}%**
> Date range: **{dr}**

---

## 📈 Channel Overview

| Metric | Videos | Shorts |
|--------|--------|--------|
| Total analysed | {_fmt(vs['count'])} | {_fmt(ss['count'])} |
| Total views | {_fmt(vs['total_views'])} | {_fmt(ss['total_views'])} |
| Total likes | {_fmt(vs['total_likes'])} | {_fmt(ss['total_likes'])} |
| Total comments | {_fmt(vs['total_comments'])} | {_fmt(ss['total_comments'])} |
| Avg views/item | {_fmt(vs['avg_views'])} | {_fmt(ss['avg_views'])} |
| Avg likes/item | {_fmt(vs['avg_likes'])} | {_fmt(ss['avg_likes'])} |
| Avg engagement | {vs['avg_engagement']:.2f}% | {ss['avg_engagement']:.2f}% |
| **Top {top_percent}% selected** | **{_fmt(len(top_videos))}** | **{_fmt(len(top_shorts))}** |

---

## 🏆 Top {top_percent}% Videos

{_top_table(top_videos)}

---

## ⚡ Top {top_percent}% Shorts

{_top_table(top_shorts)}

---

## 🏷️ Top Tags — Videos

{_tags_section(top_videos)}

## 🏷️ Top Tags — Shorts

{_tags_section(top_shorts)}

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

*Powered by [Scrapling](https://github.com/D4Vinci/Scrapling)*
"""

    with open(fp, "w", encoding="utf-8") as f:
        f.write(report)
    logger.info(f"Channel report → {fp}")
    return fp


def export_csv(items: list[dict], filepath: str) -> str:
    if not items:
        return filepath
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

    fields = [
        "rank", "title", "type", "date", "views", "likes", "comments",
        "duration", "score", "engagement_rate",
        "norm_views", "norm_likes", "norm_comments", "norm_engagement",
        "tags", "category", "url",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for rank, item in enumerate(items, 1):
            comp = item.get("_score_components", {})
            d = item.get("date")
            w.writerow({
                "rank":            rank,
                "title":           item.get("title", ""),
                "type":            item.get("type", ""),
                "date":            d.strftime("%Y-%m-%d") if d else "",
                "views":           item.get("views", 0),
                "likes":           item.get("likes", 0),
                "comments":        item.get("comments", 0),
                "duration":        item.get("duration", 0),
                "score":           item.get("score", 0),
                "engagement_rate": comp.get("engagement_rate", 0),
                "norm_views":      comp.get("norm_views", 0),
                "norm_likes":      comp.get("norm_likes", 0),
                "norm_comments":   comp.get("norm_comments", 0),
                "norm_engagement": comp.get("norm_engagement", 0),
                "tags":            "|".join(item.get("tags", [])),
                "category":        item.get("category", ""),
                "url":             item.get("url", ""),
            })

    logger.info(f"CSV → {filepath} ({len(items)} rows)")
    return filepath
