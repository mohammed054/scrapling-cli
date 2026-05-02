# scrapling-cli

Typed YouTube channel analysis and incremental fetch tooling built around Scrapling, layered transcript recovery, and deterministic markdown/CSV outputs.

## What Changed

- Runtime moved into a real package under `src/scrapling_cli/`.
- `scrapling_cli.py` and `fetch_new.py` remain as thin compatibility wrappers.
- Transcript resolution now runs in a fixed fallback order:
  1. `youtube-transcript-api`
  2. `yt-dlp` subtitle extraction
  3. Optional hosted ASR when `OPENAI_API_KEY` or `OPENROUTER_API_KEY` is available
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
--workers 1
--transcript-delay 4.0
--transcript-retries 4
--transcript-rate-limit-cooldown 300
--transcript-rate-limit-cap 3600
--allow-missing-transcripts
--allow-hosted-asr
--no-hosted-asr
--asr-model gpt-4o-mini-transcribe
--openrouter-asr-model openai/whisper-large-v3
--cookies-from-browser chrome
--cookies path/to/cookies.txt
```

The interactive CLI prints a large `SCRAPPING` startup banner plus run/result panels. Add `--no-banner` for scheduled jobs or plain log output.

Transcript fetching now keeps only one transcript network fetch in flight at a time by default, spaces requests more conservatively, shares cooldown state across YouTube-backed transcript fallbacks after `429` or bot-block responses, treats YouTube bot/IP blocks as retryable cooldown events, stops retrying the same backend once a real rate limit is detected, and avoids stacking yt-dlp's internal retries on top of the service retry loop.

For a transcript-first run where waiting is acceptable, use a slower command:

```bash
python scrapling_cli.py \
  --channel "https://www.youtube.com/@aiDotEngineer" \
  --top-percent 15 \
  --rank-by weighted \
  --recency-decay \
  --clamp-outliers \
  --transcripts \
  --workers 1 \
  --transcript-delay 12 \
  --transcript-retries 8 \
  --transcript-rate-limit-cooldown 600 \
  --transcript-rate-limit-cap 7200 \
  --export-csv \
  --output-dir output
```

## API Keys And `.env`

This repo loads local API keys from a repo-root `.env` file before it builds transcript options. The real `.env` file is ignored by git, so your key stays local.

Create a new file named `.env` in the repo root and paste these secrets into it:

```env
OPENROUTER_API_KEY=your-rotated-openrouter-key
# Optional: direct OpenAI ASR fallback
OPENAI_API_KEY=
# Browser where YouTube works while signed in
YTDLP_COOKIES_FROM_BROWSER=chrome
```

Replace `your-rotated-openrouter-key` with the new key from OpenRouter, then save the file. Set `YTDLP_COOKIES_FROM_BROWSER` to the browser where YouTube works while signed in, such as `chrome`, `edge`, `brave`, or `firefox`. You can also copy `.env.example` to `.env` and edit it.

When the CLI starts, existing shell environment variables win, so a value already set in PowerShell will not be overwritten by `.env`.

Then run the scraper with hosted ASR enabled:

```powershell
python scrapling_cli.py `
  --channel "https://www.youtube.com/@aiDotEngineer" `
  --top-percent 15 `
  --rank-by weighted `
  --recency-decay `
  --clamp-outliers `
  --no-enrich `
  --transcripts `
  --allow-hosted-asr `
  --openrouter-asr-model openai/whisper-large-v3 `
  --cookies-from-browser chrome `
  --export-csv `
  --output-dir output
```

The startup panel should show `Hosted ASR  openrouter`. If it shows `off`, the `.env` file is missing, still blank, or the shell environment is overriding it.

OpenRouter STT defaults to `openai/whisper-large-v3`; override with `--openrouter-asr-model` if your OpenRouter account has access to a different transcription model.

Hosted ASR still needs the video audio first. If `yt-dlp` says `Sign in to confirm you're not a bot`, use `.env` with `YTDLP_COOKIES_FROM_BROWSER=chrome` or pass browser cookies from a browser where YouTube already works:

```powershell
--cookies-from-browser chrome
```

Use `edge`, `chrome`, `brave`, or `firefox` depending on where you are signed in. If browser-cookie loading fails, export a Netscape-format cookies file and pass it with `--cookies path\to\cookies.txt`.

If Windows reports `Could not copy Chrome cookie database`, close every Chrome window and background process, then retry. If Chrome still fails, set `YTDLP_COOKIES_FROM_BROWSER=edge` or `firefox` in `.env` after signing into YouTube there. The most reliable fallback is exporting a Netscape-format `cookies.txt` file and setting `YTDLP_COOKIES=path\to\cookies.txt`.

If Windows reports `Failed to decrypt with DPAPI`, use the same fallback: run PowerShell as your normal Windows user, try Firefox, or export a Netscape-format `cookies.txt`. DPAPI failures usually mean `yt-dlp` can see the browser profile but Windows will not decrypt the saved cookies for this process.

When `--transcripts` is enabled, the CLI now treats missing transcripts as a blocking condition by default: retryable failures keep getting retried in rounds, and the run exits non-zero if any item still has a permanent transcript failure. Use `--allow-missing-transcripts` to restore the looser behavior.

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
- On heavily rate-limited or bot-protected IPs, YouTube watch-page fetches, subtitle providers, and ASR audio downloads may require cookies. The CLI now records those provider failures explicitly in output files and CSV exports.
