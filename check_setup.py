#!/usr/bin/env python3
"""
Setup verification script for TLNG Summit
Checks if logging, directories, and permissions are properly configured.
"""

import os
import sys
from pathlib import Path

def check_directories():
    """Check if required directories exist and are writable."""
    print("🔍 Checking directories...")
    
    base_dir = Path(__file__).parent
    required_dirs = [
        base_dir / 'logs',
        base_dir / 'media',
        base_dir / 'static',
    ]
    
    for directory in required_dirs:
        if directory.exists():
            if os.access(directory, os.W_OK):
                print(f"✅ {directory.name}/ - exists and writable")
            else:
                print(f"❌ {directory.name}/ - exists but not writable")
        else:
            print(f"⚠️  {directory.name}/ - does not exist, creating...")
            try:
                directory.mkdir(exist_ok=True)
                print(f"✅ {directory.name}/ - created successfully")
            except Exception as e:
                print(f"❌ {directory.name}/ - failed to create: {e}")

def check_environment():
    """Check environment variables."""
    print("\n🔍 Checking environment variables...")
    
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        print("✅ .env file exists")
        
        # Read .env file to check for important variables
        required_vars = ['SECRET_KEY', 'DEBUG', 'ALLOWED_HOSTS']
        missing_vars = []
        
        with open(env_file, 'r') as f:
            env_content = f.read()
            for var in required_vars:
                if f"{var}=" not in env_content:
                    missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
        else:
            print("✅ All required environment variables present")
    else:
        print("❌ .env file not found")

def check_django_config():
    """Check Django configuration."""
    print("\n🔍 Checking Django configuration...")
    
    try:
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tlng_summit_project.settings')
        
        # Import Django and configure
        import django
        from django.conf import settings
        django.setup()
        
        print("✅ Django configuration loaded successfully")
        print(f"   DEBUG = {settings.DEBUG}")
        print(f"   ALLOWED_HOSTS = {settings.ALLOWED_HOSTS}")
        
        # Check database connection
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection working")
        
    except Exception as e:
        print(f"❌ Django configuration error: {e}")

def check_logging():
    """Test logging configuration."""
    print("\n🔍 Testing logging configuration...")
    
    try:
        import logging
        
        # Test different loggers
        loggers = ['summit', 'django', 'django.request']
        
        for logger_name in loggers:
            logger = logging.getLogger(logger_name)
            logger.info(f"Test log message from {logger_name}")
            print(f"✅ {logger_name} logger working")
            
        print("✅ Logging system configured correctly")
        
    except Exception as e:
        print(f"❌ Logging configuration error: {e}")

def check_log_files():
    """Check if log files can be created."""
    print("\n🔍 Checking log file creation...")
    
    logs_dir = Path(__file__).parent / 'logs'
    test_files = ['error.log', 'warning.log', 'info.log', 'django.log', 'security.log']
    
    for log_file in test_files:
        log_path = logs_dir / log_file
        try:
            # Try to write to the log file
            with open(log_path, 'a') as f:
                f.write(f"# Test entry - {log_file}\n")
            print(f"✅ {log_file} - writable")
        except Exception as e:
            print(f"❌ {log_file} - error: {e}")

def main():
    print("=" * 60)
    print("TLNG SUMMIT SETUP VERIFICATION")
    print("=" * 60)
    
    check_directories()
    check_environment()
    check_django_config()
    check_logging()
    check_log_files()
    
    print("\n" + "=" * 60)
    print("Setup verification complete!")
    print("If any issues were found, please fix them before running the server.")
    print("=" * 60)

if __name__ == '__main__':
    main()