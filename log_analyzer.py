#!/usr/bin/env python3
"""
Log analysis script for the TLNG Summit application.
Provides insights into errors, warnings, and application usage.
"""

import os
import re
from datetime import datetime, timedelta
from collections import Counter, defaultdict
from pathlib import Path

def parse_log_line(line):
    """Parse a log line and extract timestamp, level, and message."""
    # Pattern for our log format: LEVEL TIMESTAMP MESSAGE
    pattern = r'(\w+)\s+(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2},\d{3})\s+(.+)'
    match = re.match(pattern, line)
    if match:
        level, timestamp, message = match.groups()
        try:
            dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S,%f')
            return level, dt, message
        except ValueError:
            return None, None, None
    return None, None, None

def analyze_error_log():
    """Analyze error log for common issues."""
    log_file = Path(__file__).parent / 'logs' / 'error.log'
    if not log_file.exists():
        print("No error log found.")
        return
    
    errors = []
    error_counts = Counter()
    
    with open(log_file, 'r') as f:
        for line in f:
            level, timestamp, message = parse_log_line(line)
            if level and timestamp:
                errors.append((timestamp, message))
                # Extract error type
                error_type = message.split()[0] if message else 'Unknown'
                error_counts[error_type] += 1
    
    print(f"\n=== ERROR ANALYSIS (Total: {len(errors)}) ===")
    
    if not errors:
        print("No errors found!")
        return
    
    # Recent errors (last 24 hours)
    recent_cutoff = datetime.now() - timedelta(hours=24)
    recent_errors = [e for e in errors if e[0] > recent_cutoff]
    
    print(f"Recent errors (last 24h): {len(recent_errors)}")
    print(f"Most recent error: {errors[-1][0] if errors else 'None'}")
    
    # Top error types
    print("\nTop error types:")
    for error_type, count in error_counts.most_common(5):
        print(f"  {error_type}: {count}")
    
    # Recent error details
    if recent_errors:
        print(f"\nLast 5 errors:")
        for timestamp, message in recent_errors[-5:]:
            print(f"  {timestamp}: {message[:100]}...")

def analyze_django_log():
    """Analyze Django log for request patterns."""
    log_file = Path(__file__).parent / 'logs' / 'django.log'
    if not log_file.exists():
        print("No Django log found.")
        return
    
    requests = []
    status_codes = Counter()
    paths = Counter()
    
    with open(log_file, 'r') as f:
        for line in f:
            level, timestamp, message = parse_log_line(line)
            if level and timestamp and 'HTTP' in message:
                requests.append((timestamp, message))
                
                # Extract status code and path
                if '"' in message:
                    parts = message.split('"')
                    if len(parts) >= 3:
                        request_line = parts[1]
                        status_part = parts[2].strip()
                        
                        if ' ' in request_line:
                            method, path = request_line.split(' ')[:2]
                            paths[path] += 1
                        
                        if status_part:
                            status_code = status_part.split()[0]
                            status_codes[status_code] += 1
    
    print(f"\n=== DJANGO REQUEST ANALYSIS (Total: {len(requests)}) ===")
    
    if not requests:
        print("No requests logged!")
        return
    
    # Recent requests (last hour)
    recent_cutoff = datetime.now() - timedelta(hours=1)
    recent_requests = [r for r in requests if r[0] > recent_cutoff]
    
    print(f"Recent requests (last hour): {len(recent_requests)}")
    
    # Top status codes
    print("\nTop status codes:")
    for code, count in status_codes.most_common(10):
        print(f"  {code}: {count}")
    
    # Top requested paths
    print("\nTop requested paths:")
    for path, count in paths.most_common(10):
        print(f"  {path}: {count}")

def analyze_security_log():
    """Analyze security log for suspicious activity."""
    log_file = Path(__file__).parent / 'logs' / 'security.log'
    if not log_file.exists():
        print("No security log found.")
        return
    
    security_events = []
    
    with open(log_file, 'r') as f:
        for line in f:
            level, timestamp, message = parse_log_line(line)
            if level and timestamp:
                security_events.append((timestamp, message))
    
    print(f"\n=== SECURITY ANALYSIS (Total: {len(security_events)}) ===")
    
    if not security_events:
        print("No security events logged!")
        return
    
    # Recent security events (last 24 hours)
    recent_cutoff = datetime.now() - timedelta(hours=24)
    recent_events = [e for e in security_events if e[0] > recent_cutoff]
    
    print(f"Recent security events (last 24h): {len(recent_events)}")
    
    # Show recent events
    if recent_events:
        print("\nRecent security events:")
        for timestamp, message in recent_events[-10:]:
            print(f"  {timestamp}: {message[:100]}...")

def generate_report():
    """Generate a comprehensive log report."""
    print("=" * 60)
    print("TLNG SUMMIT LOG ANALYSIS REPORT")
    print(f"Generated: {datetime.now()}")
    print("=" * 60)
    
    analyze_error_log()
    analyze_django_log()
    analyze_security_log()
    
    # Log file sizes
    print(f"\n=== LOG FILE SIZES ===")
    logs_dir = Path(__file__).parent / 'logs'
    if logs_dir.exists():
        for log_file in logs_dir.glob('*.log'):
            size_mb = log_file.stat().st_size / (1024 * 1024)
            print(f"  {log_file.name}: {size_mb:.2f} MB")

def main():
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'errors':
            analyze_error_log()
        elif command == 'requests':
            analyze_django_log()
        elif command == 'security':
            analyze_security_log()
        else:
            print("Invalid command. Use: errors, requests, security, or no argument for full report")
    else:
        generate_report()

if __name__ == '__main__':
    main()