#!/usr/bin/env bash
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │  auto_run.sh — Daily scrapling-cli runner for IBM Technology               │
# │                                                                             │
# │  Run manually:   bash auto_run.sh                                          │
# │  Run via cron:   see README.md → "Automated Daily Runs"                    │
# └─────────────────────────────────────────────────────────────────────────────┘

set -euo pipefail

# ── Resolve project root (works whether called directly or via cron) ──────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── Configuration ─────────────────────────────────────────────────────────────
CHANNEL="https://www.youtube.com/ibmtechnology"
OUTPUT_DIR="output"
LOG_DIR="logs"
DATE_TAG="$(date +%Y%m%d_%H%M%S)"
RUN_LOG="$LOG_DIR/auto_run_${DATE_TAG}.log"
SCRAPE_LOG="$LOG_DIR/scrapling_${DATE_TAG}.log"
PYTHON="${PYTHON:-python3}"          # override with: PYTHON=/path/to/venv/bin/python bash auto_run.sh

# ── Helpers ───────────────────────────────────────────────────────────────────
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$RUN_LOG"; }
die() { log "ERROR: $*"; exit 1; }

# ── Pre-flight ────────────────────────────────────────────────────────────────
mkdir -p "$LOG_DIR" "$OUTPUT_DIR"

log "======================================================"
log "  scrapling auto_run.sh"
log "  Channel : $CHANNEL"
log "  Output  : $SCRIPT_DIR/$OUTPUT_DIR"
log "======================================================"

# Verify Python is available
command -v "$PYTHON" >/dev/null 2>&1 || die "Python not found at: $PYTHON"
log "Python  : $($PYTHON --version 2>&1)"

# Verify scrapling_cli.py exists
[[ -f "$SCRIPT_DIR/scrapling_cli.py" ]] || die "scrapling_cli.py not found in $SCRIPT_DIR"

# ── Full analysis run ─────────────────────────────────────────────────────────
log "Starting full channel analysis..."

"$PYTHON" scrapling_cli.py \
    --channel "$CHANNEL" \
    --top-percent 15 \
    --rank-by weighted \
    --recency-decay \
    --clamp-outliers \
    --transcripts \
    --export-csv \
    --output-dir "$OUTPUT_DIR" \
    --log-file "$SCRAPE_LOG" \
    2>&1 | tee -a "$RUN_LOG"

EXIT_CODE=${PIPESTATUS[0]}

# ── Post-run ──────────────────────────────────────────────────────────────────
log "======================================================"
if [[ $EXIT_CODE -eq 0 ]]; then
    log "  ✅  Run completed successfully"
else
    log "  ❌  Run exited with code $EXIT_CODE"
fi
log "  Log : $RUN_LOG"
log "  Scrape log : $SCRAPE_LOG"
log "======================================================"

exit $EXIT_CODE
