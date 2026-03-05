#!/bin/bash
# Setup cron job for watchlist research
# Runs Tuesdays and Fridays at 8:00 AM

SCRIPT="/data/.openclaw/workspace/scripts/run_watchlist.sh"
CRON_JOB="0 8 * * 2,5 $SCRIPT >> /data/.openclaw/workspace/logs/cron.log 2>&1"

# Create log directory
mkdir -p /data/.openclaw/workspace/logs

# Make scripts executable
chmod +x "$SCRIPT"
chmod +x /data/.openclaw/workspace/skills/watchlist-research/scripts/*.py

# Check if cron job already exists
if crontab -l 2>/dev/null | grep -q "run_watchlist.sh"; then
    echo "Cron job already exists. Updating..."
    crontab -l 2>/dev/null | grep -v "run_watchlist.sh" > /tmp/crontab.tmp
    echo "$CRON_JOB" >> /tmp/crontab.tmp
    crontab /tmp/crontab.tmp
    rm /tmp/crontab.tmp
else
    echo "Adding new cron job..."
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
fi

echo "Cron job installed:"
echo "  Time: Tuesday, Friday at 8:00 AM"
echo "  Command: $SCRIPT"
echo ""
crontab -l | grep "run_watchlist"
