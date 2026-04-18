# scrapling-cli 🕷️🎬

A production-grade YouTube channel performance scraper — **powered entirely by [Scrapling](https://github.com/D4Vinci/Scrapling)**.

No yt-dlp. No Selenium. No heavy dependencies.  
Scrapling does the fetching. We do the rest.

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
         Pre-filter top candidates by views
                │
                ▼
         Per-video page enrichment
         (exact date, likes, description,
          chapters, tags — via Scrapling)
                │
                ▼
         Score → Select → Write Markdown
```

**Phase 1 — Channel tab scraping** (`Fetcher.get`)  
Scrapling fetches `/videos` and `/shorts` tabs with stealthy headers. The `ytInitialData` JSON blob embedded in each page's `<script>` tags is extracted and parsed — no JavaScript engine required for this step.

**Phase 2 — Pagination** (`Fetcher.post` → InnerTube API)  
Continuation tokens from `ytInitialData` are used to POST to YouTube's internal `youtubei/v1/browse` endpoint, paginating through all videos efficiently.

**Phase 3 — Per-video enrichment** (`Fetcher.get` per candidate)  
Top candidates are individually fetched for richer metadata: exact upload dates, like counts, full descriptions, chapters, tags, and subscriber counts — all parsed from `ytInitialData` and `ytInitialPlayerResponse`.

**Phase 4 — Transcripts** (`youtube-transcript-api`)  
Transcripts are fetched via the lightweight `youtube-transcript-api` library, which calls YouTube's caption endpoint directly.

---

## Setup

```bash
pip install -r requirements.txt

# Install Scrapling browser binaries (needed for StealthyFetcher fallback)
scrapling install
```

---

## Quick Start

```bash
python scrapling_cli.py --channel "@mkbhd" --top-percent 15
```

## Full-Feature Command

```bash
python scrapling_cli.py \
  --channel "@mkbhd" \
  --top-percent 15 \
  --from-date 2021-01-01 \
  --to-date 2025-01-01 \
  --rank-by weighted \
  --recency-decay \
  --clamp-outliers \
  --transcripts \
  --export-csv \
  --output-dir output \
  --log-file output/run.log \
  --verbose
```

---

## All Options

| Flag | Default | Description |
|------|---------|-------------|
| `--channel` | **required** | `@handle`, full URL, or `UC...` channel ID |
| `--top-percent` | `15` | Top X% to select (separately for videos & shorts) |
| `--rank-by` | `weighted` | `weighted` · `views` · `engagement` · `likes` |
| `--from-date` | none | Only include content uploaded on/after (`YYYY-MM-DD`) |
| `--to-date` | none | Only include content uploaded on/before (`YYYY-MM-DD`) |
| `--recency-decay` | off | Apply `exp(-days/365)` recency boost |
| `--clamp-outliers` | off | Cap viral outliers at 95th percentile |
| `--transcripts` | off | Fetch transcripts via `youtube-transcript-api` |
| `--no-enrich` | off | Skip per-video page fetches (faster, less metadata) |
| `--no-shorts` | off | Skip Shorts entirely |
| `--no-videos` | off | Skip long-form videos entirely |
| `--output-dir` | `output` | Base output directory |
| `--export-csv` | off | Export full scored dataset as CSV |
| `--no-report` | off | Skip `channel_report.md` |
| `--log-file` | none | Write logs to file |
| `--dry-run` | off | Score & preview without writing files |
| `--verbose` | off | Debug-level logging |

---

## Output Structure

```
output/
  {channel_name}/
    channel_report.md        ← summary with stats, top tables, tag clouds
    scored_videos.csv        ← full scored video dataset (if --export-csv)
    scored_shorts.csv        ← full scored shorts dataset (if --export-csv)
    videos/
      top-video-title-2024-03-15.md
      another-great-video-2023-11-02.md
    shorts/
      viral-short-2024-01-10.md
```

### Each Markdown File Contains

- Thumbnail image
- Title, date, type, duration
- Views, likes, comments, like ratio, comment ratio
- Weighted performance score + full breakdown
- Tags, category, language, channel info
- Full description
- Chapter markers
- Top comments (if available)
- Transcript (if `--transcripts` enabled)

---

## Scoring Formula

```
score = 0.5 × norm_views
      + 0.2 × norm_likes
      + 0.1 × norm_comments
      + 0.2 × norm_engagement_rate
```

Where `engagement_rate = (likes + comments) / views`.  
All values are min-max normalised across the candidate set.

**Optional modifiers:**
- `--recency-decay` → `score × exp(-days_since_upload / 365)`
- `--clamp-outliers` → values capped at 95th percentile before normalisation

---

## Architecture

```
scrapling_cli.py          ← CLI entrypoint
modules/
  fetcher.py              ← Scrapling-based YouTube scraper
                             · Fetcher.get()  — channel pages + video pages
                             · Fetcher.post() — InnerTube pagination API
                             · StealthyFetcher — fallback for blocked requests
  classifier.py           ← Raw dict → VideoRecord + videos/shorts split
  filter.py               ← Date-range filtering
  scorer.py               ← Weighted scoring engine (numpy)
  transcript.py           ← youtube-transcript-api integration
  writer.py               ← Markdown file generation
  reporter.py             ← channel_report.md + CSV export
```

---

## Notes

- YouTube's `ytInitialData` is server-rendered and available in plain HTTP responses — no JavaScript execution needed for the listing pages
- `StealthyFetcher` (headless browser) is used automatically as a fallback if a plain HTTP request is blocked
- Per-video enrichment (`--no-enrich` to skip) makes one additional Scrapling request per candidate to get exact dates, like counts, descriptions, and chapters
- Likes are parsed from YouTube's accessibility labels (e.g. "42K likes") — approximations for large counts
- Relative dates ("2 years ago") are converted to approximate calendar dates
- Private/deleted videos are automatically skipped
- Duplicate filenames get a counter suffix

---

*Powered by [Scrapling](https://github.com/D4Vinci/Scrapling) 🕷️*
