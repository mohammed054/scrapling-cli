# scrapling-cli 🕷️🎬

A production-grade YouTube channel performance scraper powered entirely by **[Scrapling](https://github.com/D4Vinci/Scrapling)**.

No yt-dlp. No Selenium. No heavy headless-browser pipeline.  
Scrapling does the fetching. We do the scoring, ranking, and reporting.

---

## Table of Contents

1. [How It Works](#how-it-works)
2. [Setup](#setup)
3. [IBM Technology — Master Command](#ibm-technology--master-command)
4. [All CLI Options](#all-cli-options)
5. [Automated Daily Runs (Cron)](#automated-daily-runs-cron)
6. [Incremental Fetch (fetch_new.py)](#incremental-fetch-fetch_newpy)
7. [Output Structure](#output-structure)
8. [Scoring Formula](#scoring-formula)
9. [Architecture](#architecture)
10. [Notes & Troubleshooting](#notes--troubleshooting)

---

## How It Works

```
Channel URL
    │
    ├─► Scrapling Fetcher ──► /videos tab  ──┐
    │   (stealthy HTTP)                       ├─► ytInitialData JSON extraction
    └─► Scrapling Fetcher ──► /shorts tab ──┘
                │
                ▼
         InnerTube API (Scrapling POST)
         Paginate through ALL videos
                │
                ▼
         Pre-filter top candidates by view count
                │
                ▼
         Per-video page enrichment
         (exact date · likes · description
          chapters · tags — via Scrapling)
                │
                ▼
         Score → Select top % → Write Markdown + CSV + Report
```

**Phase 1 — Channel tab scraping** (`Fetcher.get`)
Scrapling fetches `/videos` and `/shorts` tabs with stealthy headers.
The `ytInitialData` JSON blob embedded in each page's `<script>` tags is
extracted via brace-counting (not regex) — no JS engine required.

**Phase 2 — Pagination** (`Fetcher.post` → InnerTube)
Continuation tokens from `ytInitialData` are POSTed to YouTube's internal
`youtubei/v1/browse` endpoint, paginating through all videos.

**Phase 3 — Per-video enrichment** (`Fetcher.get` per candidate)
Top candidates are individually fetched for richer metadata: exact upload
dates, like counts, full descriptions, chapters, tags, and subscriber counts.

**Phase 4 — Transcripts** (`youtube-transcript-api`)
Fetched via the lightweight `youtube-transcript-api` library, which calls
YouTube's caption endpoint directly with no browser required.

---

## Setup

### One-command install

```bash
bash setup.sh
```

### Manual install

```bash
# 1. Create and activate a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Install Scrapling browser binaries (StealthyFetcher fallback)
scrapling install
```

---

## IBM Technology — Master Command

> **Channel:** https://www.youtube.com/ibmtechnology

### 🏆 Full Analysis — Everything, Maximum Depth

This is the one command that does it all: scrapes every video and short,
scores them, selects the top 15%, fetches transcripts, exports CSVs,
and generates a full channel report.

```bash
python scrapling_cli.py \
  --channel "https://www.youtube.com/ibmtechnology" \
  --top-percent 15 \
  --rank-by weighted \
  --recency-decay \
  --clamp-outliers \
  --transcripts \
  --export-csv \
  --output-dir output \
  --log-file logs/ibmtechnology.log \
  --verbose
```

### ⚡ Fast Analysis — No Transcripts (3–5× faster)

```bash
python scrapling_cli.py \
  --channel "https://www.youtube.com/ibmtechnology" \
  --top-percent 15 \
  --rank-by weighted \
  --recency-decay \
  --clamp-outliers \
  --export-csv \
  --output-dir output \
  --log-file logs/ibmtechnology.log
```

### 🗓️ Recent Content Only — Last 6 Months

```bash
python scrapling_cli.py \
  --channel "https://www.youtube.com/ibmtechnology" \
  --top-percent 20 \
  --from-date 2024-10-01 \
  --rank-by weighted \
  --recency-decay \
  --clamp-outliers \
  --transcripts \
  --export-csv \
  --output-dir output
```

### 🔍 Quick Preview — Dry Run (no files written)

```bash
python scrapling_cli.py \
  --channel "https://www.youtube.com/ibmtechnology" \
  --top-percent 10 \
  --rank-by views \
  --no-enrich \
  --dry-run \
  --verbose
```

### 📹 Videos Only (skip Shorts)

```bash
python scrapling_cli.py \
  --channel "https://www.youtube.com/ibmtechnology" \
  --top-percent 15 \
  --no-shorts \
  --rank-by engagement \
  --recency-decay \
  --clamp-outliers \
  --transcripts \
  --export-csv \
  --output-dir output
```

---

## All CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--channel` / `-c` | **required** | `@handle`, full URL, or `UC...` channel ID |
| `--top-percent` / `-p` | `15` | Top X% to select (separately for videos & shorts) |
| `--rank-by` | `weighted` | `weighted` · `views` · `engagement` · `likes` |
| `--from-date` | none | Only include content uploaded on/after (`YYYY-MM-DD`) |
| `--to-date` | none | Only include content uploaded on/before (`YYYY-MM-DD`) |
| `--recency-decay` | off | Apply `exp(-days/365)` recency boost to scores |
| `--clamp-outliers` | off | Cap viral outliers at 95th percentile before scoring |
| `--transcripts` | off | Fetch full transcripts via `youtube-transcript-api` |
| `--no-enrich` | off | Skip per-video page fetches (faster, less metadata) |
| `--no-shorts` | off | Skip Shorts entirely |
| `--no-videos` | off | Skip long-form videos entirely |
| `--output-dir` / `-o` | `output` | Base output directory |
| `--export-csv` | off | Export full scored dataset as CSV |
| `--no-report` | off | Skip `channel_report.md` |
| `--log-file` | none | Write logs to a file |
| `--dry-run` | off | Score & print preview, write nothing |
| `--verbose` / `-v` | off | Debug-level logging |

---

## Automated Daily Runs (Cron)

There are two strategies. Choose the one that fits your workflow:

---

### Strategy A — Full Analysis Every Day

Runs the complete pipeline (score + rank + report) fresh each day.
Good for weekly or deep audits. Can take 10–40 minutes depending on channel size.

#### Step 1 — Get your Python path

```bash
which python3
# example: /usr/bin/python3
# with venv: /home/you/scrapling_cli/venv/bin/python
```

#### Step 2 — Get your project path

```bash
cd scrapling_cli && pwd
# example: /home/you/scrapling_cli
```

#### Step 3 — Open crontab

```bash
crontab -e
```

#### Step 4 — Add the line (runs at 07:00 every day)

```cron
# scrapling-cli — full IBM Technology analysis, daily at 07:00
0 7 * * * cd /home/you/scrapling_cli && /usr/bin/python3 scrapling_cli.py --channel "https://www.youtube.com/ibmtechnology" --top-percent 15 --rank-by weighted --recency-decay --clamp-outliers --transcripts --export-csv --output-dir output --log-file logs/daily.log >> logs/cron.log 2>&1
```

#### Alternative — Use auto_run.sh (cleaner, with error handling)

```bash
# Make it executable once:
chmod +x /home/you/scrapling_cli/auto_run.sh
```

Crontab line:

```cron
# scrapling-cli via auto_run.sh — daily at 07:00
0 7 * * * /home/you/scrapling_cli/auto_run.sh >> /home/you/scrapling_cli/logs/cron.log 2>&1
```

---

### Strategy B — Incremental Daily Fetch (Recommended for ongoing monitoring)

`fetch_new.py` uses `state.json` to track the last run date.
On each execution it fetches **only new content** since the previous run.
Much faster (seconds to minutes). Perfect for daily cron jobs.

```cron
# scrapling fetch_new — incremental IBM Technology watch, daily at 07:00
0 7 * * * cd /home/you/scrapling_cli && /usr/bin/python3 fetch_new.py >> logs/fetch_new_cron.log 2>&1
```

With transcripts:

```cron
0 7 * * * cd /home/you/scrapling_cli && /usr/bin/python3 fetch_new.py --transcripts >> logs/fetch_new_cron.log 2>&1
```

---

### Cron Time Reference

```
┌───────── minute  (0–59)
│ ┌─────── hour    (0–23)
│ │ ┌───── day of month (1–31)
│ │ │ ┌─── month   (1–12)
│ │ │ │ ┌─ day of week (0–7, 0 and 7 = Sunday)
│ │ │ │ │
0 7 * * *   →  every day at 07:00
0 7 * * 1   →  every Monday at 07:00
0 7 1 * *   →  1st of every month at 07:00
0 */6 * * * →  every 6 hours
```

---

### Verify Cron Is Working

```bash
# Check scheduled jobs
crontab -l

# Watch logs in real time
tail -f /home/you/scrapling_cli/logs/cron.log
tail -f /home/you/scrapling_cli/logs/fetch_new_cron.log

# Check last run state (fetch_new.py)
cat /home/you/scrapling_cli/state.json
```

---

### Virtual Environment with Cron

If you installed into a venv, cron must use the venv Python explicitly:

```cron
0 7 * * * cd /home/you/scrapling_cli && /home/you/scrapling_cli/venv/bin/python fetch_new.py --transcripts >> logs/fetch_new_cron.log 2>&1
```

Or for auto_run.sh:

```cron
0 7 * * * PYTHON=/home/you/scrapling_cli/venv/bin/python /home/you/scrapling_cli/auto_run.sh >> /home/you/scrapling_cli/logs/cron.log 2>&1
```

---

## Incremental Fetch (fetch_new.py)

`fetch_new.py` is the cron companion. It tracks the last run in `state.json`
and on each execution only fetches content published since then.

```bash
# Default — IBM Technology, last 7 days on first run
python fetch_new.py

# With full transcripts
python fetch_new.py --transcripts

# Specific channel
python fetch_new.py --channels "https://www.youtube.com/ibmtechnology"

# Multiple channels at once
python fetch_new.py --channels "@IBMTechnology" "@mkbhd"

# Force a specific start date (ignores state.json)
python fetch_new.py --force-from 2025-01-01 --transcripts

# Wider fallback window on first run
python fetch_new.py --days-back 30

# Verbose output
python fetch_new.py --verbose
```

State file `state.json` tracks per-channel last-run dates:

```json
{
  "last_run_ibmtechnology": "2026-04-21",
  "last_run_mkbhd": "2026-04-21"
}
```

---

## Output Structure

### scrapling_cli.py output

```
output/
  ibm_technology/
    channel_report.md        ← full summary: stats, top tables, tag clouds
    scored_videos.csv        ← complete ranked video dataset (with --export-csv)
    scored_shorts.csv        ← complete ranked shorts dataset (with --export-csv)
    videos/
      what-is-quantum-computing-2024-03-15.md
      ibm-watsonx-explained-2023-11-02.md
      ...
    shorts/
      ai-in-60-seconds-2024-01-10.md
      ...
```

### fetch_new.py output

```
output_new/
  ibm_technology/
    videos/
      new-video-title-2026-04-21.md
    shorts/
      new-short-2026-04-21.md
```

### What each Markdown file contains

**scrapling_cli.py output files:**
- Thumbnail image
- Title, date, type, duration
- Views, likes, comments, like ratio, comment ratio
- Weighted performance score + full normalised breakdown
- Score components (norm_views, norm_likes, norm_engagement)
- Tags, category, language, channel info, subscriber count
- Full description
- Chapter markers (if available)
- Top comments (if available)
- Transcript (if `--transcripts` was set)

**fetch_new.py output files:**
- Thumbnail image
- Title, date, type, duration, views, channel
- Tags
- Full description
- Transcript (if `--transcripts` was set)

---

## Scoring Formula

```
score = 0.5 × norm_views
      + 0.2 × norm_likes
      + 0.1 × norm_comments
      + 0.2 × norm_engagement_rate

where  engagement_rate = (likes + comments) / views
```

All values are min-max normalised across the full candidate set for that run.

**Optional modifiers:**

| Flag | Effect |
|------|--------|
| `--recency-decay` | Multiplies score by `exp(-days_since_upload / 365)` — newer content scores higher |
| `--clamp-outliers` | Caps view/like/comment counts at 95th percentile before normalisation — prevents one viral video from dominating |

**`--rank-by` options:**

| Value | What it ranks by |
|-------|-----------------|
| `weighted` | Full formula above (default — most balanced) |
| `views` | Raw view count only |
| `engagement` | `(likes + comments) / views` only |
| `likes` | Like count only |

---

## Architecture

```
scrapling_cli.py        ← main CLI entrypoint (7-step pipeline)
fetch_new.py            ← incremental cron fetcher (state.json based)
auto_run.sh             ← shell wrapper for cron (logging + error codes)
setup.sh                ← one-command install

modules/
  fetcher.py            ← Scrapling-based YouTube scraper
                           · Fetcher.get()       — channel pages + video pages
                           · Fetcher.post()      — InnerTube pagination API
                           · StealthyFetcher     — headless Chromium fallback
                           · brace-counting JSON — robust ytInitialData extraction
  classifier.py         ← raw dict → VideoRecord + videos/shorts split
                           · relative date parsing  ("2 years ago" → date)
  filter.py             ← date-range filtering
  scorer.py             ← weighted scoring engine (numpy)
  transcript.py         ← youtube-transcript-api integration
  writer.py             ← Markdown file generation (full scoring detail)
  reporter.py           ← channel_report.md + CSV export
```

---

## Notes & Troubleshooting

**YouTube bot detection**
Scrapling uses stealthy HTTP headers for initial requests. If a page is blocked,
`StealthyFetcher` (headless Chromium) activates automatically.
Run `scrapling install` once to ensure the browser binaries are available.

**Likes are approximate for large counts**
YouTube only surfaces like counts via accessibility labels (`"42K likes"`).
These are parsed and converted to integers — very high counts are approximations.

**Relative dates**
Channel listing pages show relative dates (`"2 years ago"`).
These are converted to approximate calendar dates.
Per-video enrichment fetches the exact date (skip with `--no-enrich`).

**Nothing found / zero videos**
- Verify the channel handle: use the full URL `https://www.youtube.com/ibmtechnology`
- Also try `@IBMTechnology`
- Add `--verbose` to see detailed scraping logs
- YouTube occasionally changes its `ytInitialData` schema

**Cron job not running**
- Use absolute paths everywhere in crontab
- Confirm with `crontab -l`
- Check `logs/cron.log` for errors
- Suppress email: add `MAILTO=""` at the top of your crontab

**Speed optimisation**

| Scenario | Flags to add |
|----------|-------------|
| Skip metadata enrichment | `--no-enrich` |
| Skip transcripts | omit `--transcripts` |
| Shorter candidate list | lower `--top-percent` |
| One content type only | `--no-shorts` or `--no-videos` |

---

*Powered by [Scrapling](https://github.com/D4Vinci/Scrapling) 🕷️*
