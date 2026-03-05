#!/bin/bash
# Research watchlist runner
# Runs research on watchlist topics

export PATH="/home/linuxbrew/.linuxbrew/bin:$PATH"

SCRIPT_DIR="$HOME/.openclaw/skills/watchlist-research/scripts"
LOG_DIR="$HOME/.openclaw/workspace/logs"

mkdir -p "$LOG_DIR"

cd "$SCRIPT_DIR"

# Run research on all topics
python3 watchlist.py run all 2>&1 | tee "$LOG_DIR/watchlist-$(date +%Y%m%d-%H%M).log"

# Generate report
python3 watchlist.py report 7 2>&1 | tee -a "$LOG_DIR/watchlist-$(date +%Y%m%d-%H%M).log"

# Print completion message
echo "Watchlist research completed at $(date)"
