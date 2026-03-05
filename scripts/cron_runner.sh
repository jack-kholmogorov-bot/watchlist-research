#!/bin/bash
# Watchlist Research - Cron Runner
# Runs Tuesdays and Fridays at 8:00 AM America/Phoenix
# Generates full report with all findings

export PATH="/home/linuxbrew/.linuxbrew/bin:/home/linuxbrew/.linuxbrew/sbin:$PATH"
export PYTHONPATH="/home/linuxbrew/.linuxbrew/lib/python3.14/site-packages"

# Load environment variables
export $(grep -v '^#' /data/.openclaw/workspace/projects/watchlist-research/.env | xargs)

SCRIPT_DIR="/data/.openclaw/workspace/projects/watchlist-research/scripts"
LOG_DIR="/data/.openclaw/workspace/logs"
REPORT_DIR="/data/.openclaw/workspace/reports"

mkdir -p "$LOG_DIR" "$REPORT_DIR"

DATE=$(date '+%Y-%m-%d_%H-%M')
LOG_FILE="$LOG_DIR/watchlist-$DATE.log"
REPORT_FILE="$REPORT_DIR/report-$DATE.txt"

echo "========================================" | tee -a "$LOG_FILE"
echo "Watchlist Research - $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

cd "$SCRIPT_DIR"

# Initialize topics if first run
if [ ! -f "$HOME/.openclaw/workspace/watchlist.db" ]; then
    echo "Initializing watchlist database..." | tee -a "$LOG_FILE"
    python3 watchlist.py init 2>&1 | tee -a "$LOG_FILE"
fi

# Run research on all topics with full depth
echo ""
echo "🔍 Running research on all topics..." | tee -a "$LOG_FILE"
python3 watchlist.py run all 30 2>&1 | tee -a "$LOG_FILE"

# Generate comprehensive report
echo ""
echo "📊 Generating report..." | tee -a "$LOG_FILE"
python3 watchlist.py report 7 2>&1 | tee "$REPORT_FILE" | tee -a "$LOG_FILE"

echo ""
echo "✅ Completed at $(date)" | tee -a "$LOG_FILE"
echo "Report saved to: $REPORT_FILE" | tee -a "$LOG_FILE"
echo "Log saved to: $LOG_FILE" | tee -a "$LOG_FILE"

# Optional: Send report via webhook/telegram if configured
if [ -n "$REPORT_WEBHOOK" ]; then
    curl -s -X POST -H "Content-Type: text/plain" --data "@$REPORT_FILE" "$REPORT_WEBHOOK" > /dev/null
fi

echo "========================================" | tee -a "$LOG_FILE"
