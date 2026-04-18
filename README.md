# scrapling-cli 🎬

A production-grade YouTube channel performance scraper.  
Extracts ALL videos & shorts, scores them by weighted performance, and saves top performers as structured Markdown files.

---

## Setup

```bash
pip install -r requirements.txt
```

---

## Quick Start

```bash
python scrapling_cli.py --channel "@erickimberling" --top-percent 15
```

## Full-Feature Command

```bash
python scrapling_cli.py \
  --channel "@erickimberling" \
  --top-percent 15 \
  --from-date 2020-01-01 \
  --to-date 2025-06-01 \
  --recency-decay \
  --clamp-outliers \
  --transcripts \
  --output-dir output \
  --log-file output/run.log \
  --verbose
```

```bash
python scrapling_cli.py \
  --channel @erickimberling \
  --top-percent 15 \
  --from-date 2020-01-01 \
  --to-date 2025-06-01 \
  --recency-decay \
  --clamp-outliers \
  --transcripts \
  --output-dir output \
  --log-file output/run.log \
  --verbose
```

---

## All Options

| Flag | Default | Description |
|------|---------|-------------|
| `--channel` | **required** | Handle (`@name`), full URL, or channel ID |
| `--top-percent` | `15` | Top X% to select (separately for videos & shorts) |
| `--rank-by` | `weight` | Ranking method: `weight` (weighted performance) or `views` (raw view count) |
| `--from-date` | none | Only include content uploaded on/after date (`YYYY-MM-DD`) |
| `--to-date` | none | Only include content uploaded on/before date (`YYYY-MM-DD`) |
| `--recency-decay` | off | Apply exp(-days/365) recency boost to score |
| `--clamp-outliers` | off | Cap viral outliers at 95th percentile |
| `--transcripts` | off | Fetch transcripts (slower — adds per-video API calls) |
| `--no-shorts` | off | Skip Shorts entirely |
| `--no-videos` | off | Skip long-form videos entirely |
| `--output-dir` | `output` | Base output directory |
| `--log-file` | none | Write logs to file |
| `--cookies` | none | Netscape cookies.txt for age-restricted content |
| `--dry-run` | off | Score & preview without writing any files |
| `--verbose` | off | Debug-level logging |

---

## Output Structure

The tool generates two ranking files in the output directory:

### Ranked by Weight (default)
```
output/
  {channel_name}/
    ranked-by-weight.md
```

### Ranked by Views
```
output/
  {channel_name}/
    ranked-by-views.md
```

### Individual Video Files
```
output/
  {channel_name}/
    videos/
      top-video-title-2024-03-15.md
      another-great-video-2023-11-02.md
    shorts/
      viral-short-title-2024-01-10.md
```

```
output/
  {channel_name}/
    videos/
      top-video-title-2024-03-15.md
      another-great-video-2023-11-02.md
    shorts/
      viral-short-title-2024-01-10.md
```

### Each Markdown File Contains:

- Title, date, type, duration
- Views, likes, comments
- Weighted performance score + breakdown
- Full description
- Transcript (if `--transcripts` enabled)

### Ranking Files Structure

**ranked-by-weight.md** - Videos sorted by weighted performance score
**ranked-by-views.md** - Videos sorted by raw view count

Each ranking file includes:
- Video title and URL
- Upload date
- Duration
- Views, likes, comments
- Weighted performance score
- Individual metric weights
- Overall rank

---

## Scoring Formula

The weighted performance score combines multiple metrics:

```
score = 0.5 × norm_views
      + 0.2 × norm_likes  
      + 0.1 × norm_comments
      + 0.2 × norm_engagement_rate
```

Where `engagement_rate = (likes + comments) / views`

All values min-max normalized across the full channel dataset.

### Weight Breakdown

**Views (50%)** - Raw view count, normalized
**Likes (20%)** - Normalized like count
**Comments (10%)** - Normalized comment count  
**Engagement Rate (20%)** - (Likes + Comments) / Views, normalized

### Optional Modifiers

- **Recency decay**: `score × exp(-days_since_upload / 365)`
- **Outlier clamp**: Values capped at 95th percentile before normalization

```
score = 0.5 × norm_views
      + 0.2 × norm_likes  
      + 0.1 × norm_comments
      + 0.2 × norm_engagement_rate
```

Where `engagement_rate = (likes + comments) / views`

All values min-max normalized across the full channel dataset.

Optional modifiers:
- **Recency decay**: `score × exp(-days_since_upload / 365)`
- **Outlier clamp**: Values capped at 95th percentile before normalization

---

## Notes

- Private/deleted videos are silently skipped
- Videos with 0 views do not cause division errors
- Duplicate filenames get a counter suffix automatically
- Transcripts use `youtube-transcript-api` first, then `yt-dlp` subtitles fallback
- Ranking files are generated in both weight-based and view-based orders
- The `--rank-by` flag controls which ranking method is used for selection

- Private/deleted videos are silently skipped
- Videos with 0 views do not cause division errors
- Duplicate filenames get a counter suffix automatically
- Transcripts use `youtube-transcript-api` first, then `yt-dlp` subtitles fallback
