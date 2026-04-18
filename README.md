# scrapling-cli

**YouTube Channel Intelligence Tool** — scrapes all videos & shorts, scores them with a weighted performance formula, and exports top performers as structured Markdown files.

---

## Installation

```bash
# 1. Clone / download the project folder
cd scrapling_cli

# 2. Install dependencies
pip install -r requirements.txt
```

---

## Usage

```bash
python main.py --channel @channel_handle --top-percent 15
```

### All options

| Flag | Description | Default |
|---|---|---|
| `--channel` / `-c` | Channel handle (`@name`) or full URL | **required** |
| `--top-percent` / `-p` | % of top videos/shorts to keep | `10` |
| `--from-date` | Start date filter `YYYY-MM-DD` | none |
| `--to-date` | End date filter `YYYY-MM-DD` | today |
| `--output-dir` | Root output directory | `./output` |
| `--no-transcript` | Skip transcript fetching (faster) | off |
| `--decay` | Apply time-decay recency boost | off |
| `--max-videos` | Cap videos fetched (for testing) | none |
| `--verbose` / `-v` | Enable debug logging | off |

### Examples

```bash
# Top 10% of all time
python main.py --channel @mkbhd

# Top 20% from 2022 onward
python main.py --channel @lexfridman --top-percent 20 --from-date 2022-01-01

# Date range, no transcripts (fast mode), with recency boost
python main.py --channel @someChannel -p 15 \
  --from-date 2021-01-01 --to-date 2024-01-01 \
  --no-transcript --decay

# Test run — only fetch first 30 videos
python main.py --channel @veritasium --max-videos 30 --top-percent 30
```

---

## Output Structure

```
output/
└── channel_name/
    ├── videos/
    │   ├── my-best-video-title-2023-04-12.md
    │   └── another-great-video-2022-11-05.md
    └── shorts/
        └── quick-tip-about-something-2023-07-01.md
```

### Each `.md` file contains

```markdown
# Video Title Here

- **Type:** Video
- **Date:** 2023-04-12
- **Duration:** 12m 34s
- **Views:** 1,245,000
- **Likes:** 48,200
- **Comments:** 3,100
- **Score:** 0.8421
- **URL:** https://www.youtube.com/watch?v=...

---

## Description

Full description text...

---

## Transcript

Full transcript, chunked into readable paragraphs...
```

---

## Scoring Formula

```
score = 0.5 × norm_views
      + 0.2 × norm_likes
      + 0.1 × norm_comments
      + 0.2 × norm_engagement_rate
```

Where:
- All values are min-max normalized across the scoring group
- `engagement_rate = (likes + comments) / views`
- Outliers are clamped at the 95th percentile before normalization
- Optional time decay: `score *= exp(−days_since_upload / 365)`

Videos and Shorts are scored **independently** (no cross-contamination).

---

## Content Classification

| Duration | Type |
|---|---|
| < 60 seconds | Short |
| ≥ 60 seconds | Video |

---

## Transcript Priority

1. Manual captions (official)
2. Auto-generated captions
3. Any available language (auto-translated to English)
4. `"Transcript not available"` if nothing found

---

## Edge Cases Handled

- Missing likes / comments → treated as 0
- Zero views → engagement rate = 0 (no division error)
- Private / deleted videos → skipped with warning
- Duplicate titles → deduplicated with numeric suffix
- No transcript → graceful fallback message
- Empty date fields → epoch date (excluded by date filter)
