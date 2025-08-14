#!/bin/bash
# Log rotation script for TLNG Summit
# Run this daily via cron: 0 2 * * * /path/to/tlng_summit/rotate_logs.sh

LOGS_DIR="$(dirname "$0")/logs"
ARCHIVE_DIR="$LOGS_DIR/archive"
DATE=$(date +%Y%m%d)

# Create archive directory if it doesn't exist
mkdir -p "$ARCHIVE_DIR"

# Function to rotate a log file
rotate_log() {
    local logfile="$1"
    local basename=$(basename "$logfile" .log)
    
    if [ -f "$logfile" ] && [ -s "$logfile" ]; then
        # Compress and move to archive
        gzip -c "$logfile" > "$ARCHIVE_DIR/${basename}_${DATE}.log.gz"
        
        # Clear the original log file
        > "$logfile"
        
        echo "Rotated $logfile"
    fi
}

# Rotate all log files
for logfile in "$LOGS_DIR"/*.log; do
    if [ -f "$logfile" ]; then
        rotate_log "$logfile"
    fi
done

# Clean up old archives (keep last 30 days)
find "$ARCHIVE_DIR" -name "*.log.gz" -mtime +30 -delete

echo "Log rotation completed on $(date)"