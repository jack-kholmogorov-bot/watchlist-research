#!/bin/bash
# Alternative scheduler for systems without cron
# Run this script in background or via systemd timer

SCRIPT_DIR="/data/.openclaw/workspace/projects/watchlist-research/scripts"
LOG_FILE="/data/.openclaw/workspace/logs/scheduler.log"

mkdir -p /data/.openclaw/workspace/logs

echo "$(date): Scheduler started" >> "$LOG_FILE"

while true; do
    # Get current time in America/Phoenix
    CURRENT_HOUR=$(TZ='America/Phoenix' date +%H)
    CURRENT_MINUTE=$(TZ='America/Phoenix' date +%M)
    CURRENT_DAY=$(TZ='America/Phoenix' date +%u)  # 2=Tuesday, 5=Friday
    
    # Check if it's Tuesday (2) or Friday (5) at 8:00 AM
    if [ "$CURRENT_HOUR" = "08" ] && [ "$CURRENT_MINUTE" = "00" ]; then
        if [ "$CURRENT_DAY" = "2" ] || [ "$CURRENT_DAY" = "5" ]; then
            echo "$(date): Triggering watchlist research (day $CURRENT_DAY at $CURRENT_HOUR:$CURRENT_MINUTE)" >> "$LOG_FILE"
            "$SCRIPT_DIR/cron_runner.sh"
        fi
    fi
    
    # Sleep for 60 seconds
    sleep 60
done
