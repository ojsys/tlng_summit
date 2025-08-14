#!/usr/bin/env python3
"""
Log monitoring script for the TLNG Summit application.
Usage: python monitor_logs.py [log_type]
Log types: error, warning, info, django, security, all
"""

import os
import sys
import time
from pathlib import Path

def get_log_file(log_type):
    """Get the log file path for the given log type."""
    logs_dir = Path(__file__).parent / 'logs'
    log_files = {
        'error': logs_dir / 'error.log',
        'warning': logs_dir / 'warning.log',
        'info': logs_dir / 'info.log',
        'django': logs_dir / 'django.log',
        'security': logs_dir / 'security.log'
    }
    return log_files.get(log_type)

def tail_log(log_file, lines=50):
    """Display the last N lines of a log file."""
    if not log_file.exists():
        print(f"Log file {log_file} does not exist yet.")
        return
    
    print(f"\n=== Last {lines} lines of {log_file.name} ===")
    with open(log_file, 'r') as f:
        file_lines = f.readlines()
        for line in file_lines[-lines:]:
            print(line.rstrip())

def monitor_log(log_file):
    """Monitor a log file in real-time."""
    if not log_file.exists():
        print(f"Waiting for log file {log_file} to be created...")
        while not log_file.exists():
            time.sleep(1)
    
    print(f"\n=== Monitoring {log_file.name} (Press Ctrl+C to stop) ===")
    
    with open(log_file, 'r') as f:
        # Go to end of file
        f.seek(0, 2)
        
        try:
            while True:
                line = f.readline()
                if line:
                    print(line.rstrip())
                else:
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print(f"\nStopped monitoring {log_file.name}")

def show_all_logs():
    """Show recent entries from all log files."""
    logs_dir = Path(__file__).parent / 'logs'
    log_types = ['error', 'warning', 'info', 'django', 'security']
    
    for log_type in log_types:
        log_file = logs_dir / f'{log_type}.log'
        if log_file.exists():
            tail_log(log_file, 20)
        else:
            print(f"\n=== {log_type.upper()} LOG ===")
            print("No log file found.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python monitor_logs.py [command] [log_type]")
        print("Commands:")
        print("  tail [log_type] - Show last 50 lines")
        print("  watch [log_type] - Monitor in real-time")
        print("  all - Show recent entries from all logs")
        print("\nLog types: error, warning, info, django, security")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'all':
        show_all_logs()
    elif command in ['tail', 'watch'] and len(sys.argv) >= 3:
        log_type = sys.argv[2]
        log_file = get_log_file(log_type)
        
        if not log_file:
            print(f"Invalid log type: {log_type}")
            print("Available types: error, warning, info, django, security")
            sys.exit(1)
        
        if command == 'tail':
            tail_log(log_file)
        elif command == 'watch':
            monitor_log(log_file)
    else:
        print("Invalid command or missing log type.")
        print("Use: python monitor_logs.py [tail|watch|all] [log_type]")

if __name__ == '__main__':
    main()