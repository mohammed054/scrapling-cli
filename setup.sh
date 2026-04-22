#!/usr/bin/env bash
# setup.sh — One-command setup for scrapling-cli
set -euo pipefail

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║       scrapling-cli  setup               ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Create a virtual environment if one doesn't exist
if [[ ! -d "venv" ]]; then
    echo "[1/3] Creating virtual environment..."
    python3 -m venv venv
else
    echo "[1/3] Virtual environment already exists, skipping."
fi

# Activate and install
echo "[2/3] Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt

# Install Scrapling browser binaries (needed for StealthyFetcher fallback)
echo "[3/3] Installing Scrapling browser binaries..."
scrapling install || echo "  ⚠  scrapling install failed — StealthyFetcher fallback may not work."

echo ""
echo "✅  Setup complete!"
echo ""
echo "Quick start:"
echo "  source venv/bin/activate"
echo "  python scrapling_cli.py --channel \"https://www.youtube.com/ibmtechnology\" --top-percent 15"
echo ""
echo "Full IBM Technology analysis:"
echo "  python scrapling_cli.py \\"
echo "    --channel \"https://www.youtube.com/ibmtechnology\" \\"
echo "    --top-percent 15 --rank-by weighted \\"
echo "    --recency-decay --clamp-outliers \\"
echo "    --transcripts --export-csv"
echo ""
echo "Daily incremental fetch:"
echo "  python fetch_new.py"
echo ""
