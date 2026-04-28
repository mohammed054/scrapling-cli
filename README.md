# scrapling-cli

Typed YouTube channel analysis and incremental fetch tooling built around Scrapling, layered transcript recovery, and deterministic markdown/CSV outputs.

## What Changed

- Runtime moved into a real package under `src/scrapling_cli/`.
- `scrapling_cli.py` and `fetch_new.py` remain as thin compatibility wrappers.
- Transcript resolution now runs in a fixed fallback order:
  1. `youtube-transcript-api`
  2. `yt-dlp` subtitle extraction
  3. Optional OpenAI ASR when `OPENAI_API_KEY` is available
  4. Structured `unavailable` result with provenance and error details
- Transcript metadata is exported everywhere:
  - `transcript_status`
  - `transcript_source`
  - `transcript_language`
  - `transcript_chars`
  - `transcript_error`
- Outputs are deterministic:
  - stable scoring/order
  - exact-date filenames only when an exact upload date was confirmed
  - transcript/cache artifacts stored under a repo-local cache directory

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

`requirements.txt` is a compatibility stub that installs the editable package plus test dependencies from `pyproject.toml`.

## Analyze a Channel

```bash
python scrapling_cli.py \
  --channel "https://www.youtube.com/ibmtechnology" \
  --top-percent 15 \
  --rank-by weighted \
  --recency-decay \
  --clamp-outliers \
  --transcripts \
  --export-csv \
  --output-dir output
```

Useful transcript controls:

```bash
--transcript-language en
--cache-dir .cache/scrapling-cli
--workers 2
--transcript-delay 2.0
--transcript-retries 4
--allow-hosted-asr
--no-hosted-asr
--asr-model gpt-4o-mini-transcribe
```

Transcript fetching now spaces requests by default, retries retryable provider failures with exponential backoff, and avoids caching transient block responses such as `429` or `not a bot` challenges.

If YouTube blocks the current IP, the transcript fields will still record the failure reason instead of collapsing to a generic message.

The full-analysis report now records both:

- `Unique items scraped`
- `Candidate items scored`

This matters because scoring runs against a prefiltered candidate pool for speed, while still making that pool size explicit in the output.

## Incremental Fetch

```bash
python fetch_new.py \
  --channels \
  "https://www.youtube.com/ibmtechnology" \
  "https://www.youtube.com/@Fireship" \
  --days-back 7 \
  --transcripts \
  --output-dir output_new \
  --state-file state.json
```

This flow fetches channel tabs, keeps only items newer than the stored run date, enriches the remaining items, resolves transcripts, and writes markdown under per-channel `videos/` and `shorts/` directories.

For a ready-to-run multi-channel example, this repo ships with [`channels.daily.txt`](channels.daily.txt), which currently includes:

- `https://www.youtube.com/ibmtechnology`
- `https://www.youtube.com/@Fireship`

## Automated Daily Runs

For this Windows repo layout, the default daily runner is:

```powershell
.\auto_run.ps1
```

It reads channel URLs from `channels.daily.txt`, writes incremental output to `output_daily/`, and stores the rolling state in `state.daily.json`.

To register a Task Scheduler job that runs every day at `7:00 AM`:

```powershell
.\register_daily_task.ps1 -Time 07:00
```

Edit `channels.daily.txt` to replace the two example channels with your real watch list.

## Output Layout

Analysis output:

```text
output/<channel_slug>/
  channel_report.md
  scored_videos.csv
  scored_shorts.csv
  videos/*.md
  shorts/*.md
```

`channel_report.md` now includes:

- unique items scraped from the channel
- candidate items that were actually scored after prefiltering
- an engagement note when YouTube does not expose likes/comments for that run

Incremental output:

```text
output_new/<channel_slug>/
  videos/*.md
  shorts/*.md
```

## Daily Automation

Windows PowerShell runner:

```powershell
powershell -ExecutionPolicy Bypass -File .\auto_run.ps1
```

That script reads channel URLs from `channels.daily.txt`, fetches new items with transcripts enabled, writes output under `output_daily/`, updates `state.daily.json`, and stores a timestamped log under `logs/`.

To register a daily Windows Task Scheduler job for `7:00 AM`:

```powershell
powershell -ExecutionPolicy Bypass -File .\register_daily_task.ps1 -Time 07:00
```

You can edit `channels.daily.txt` directly to swap in the delivery channels you actually want monitored.

## Tests

```bash
.venv/bin/python -m pytest tests -q
.venv/bin/python -m compileall src scrapling_cli.py fetch_new.py tests
```

There is also one opt-in live smoke placeholder in the pytest suite, marked `live`.

## Notes

- `imageio-ffmpeg` supplies the bundled ffmpeg path for OpenAI ASR normalization and chunking.
- On heavily rate-limited or bot-protected IPs, YouTube watch-page fetches and subtitle providers may require cookies or proxies. The CLI now records those provider failures explicitly in output files and CSV exports.
