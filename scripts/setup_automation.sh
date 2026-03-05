#!/bin/bash
# Setup automation for watchlist research
# Tries cron first, falls back to background scheduler

SCRIPT_DIR="/data/.openclaw/workspace/projects/watchlist-research/scripts"

echo "Setting up watchlist research automation..."
echo "Schedule: Tuesday & Friday at 8:00 AM (America/Phoenix)"
echo ""

# Make scripts executable
chmod +x "$SCRIPT_DIR"/*.sh
chmod +x "$SCRIPT_DIR"/*.py

# Try cron first
if command -v crontab &> /dev/null; then
    echo "✓ Cron available, installing cron job..."
    
    # Remove existing job if present
    crontab -l 2>/dev/null | grep -v "cron_runner.sh" > /tmp/crontab.tmp || true
    
    # Add new job (8:00 AM Tue/Fri)
    echo "0 8 * * 2,5 $SCRIPT_DIR/cron_runner.sh >> /data/.openclaw/workspace/logs/cron.log 2>&1" >> /tmp/crontab.tmp
    crontab /tmp/crontab.tmp
    rm /tmp/crontab.tmp
    
    echo "✓ Cron job installed:"
    crontab -l | grep "cron_runner" || echo "  (No cron job found)"
    echo ""
    echo "To verify: crontab -l"
    
else
    echo "⚠ Cron not available, using background scheduler..."
    echo ""
    echo "To start scheduler:"
    echo "  nohup $SCRIPT_DIR/scheduler.sh > /dev/null 2>&1 &"
    echo ""
    echo "To check if running:"
    echo "  ps aux | grep scheduler.sh"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Manual run command:"
echo "  $SCRIPT_DIR/cron_runner.sh"
