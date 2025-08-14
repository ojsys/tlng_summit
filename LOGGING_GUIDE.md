# TLNG Summit Logging Guide

## Overview
This project includes a comprehensive logging system designed for production use when `DEBUG=False`. The logging system captures errors, warnings, security events, and general application information.

## Log Files

All log files are stored in the `logs/` directory:

- **`error.log`** - Critical errors and exceptions
- **`warning.log`** - Warning messages and potential issues
- **`info.log`** - General application information
- **`django.log`** - Django framework logs and HTTP requests
- **`security.log`** - Security-related events

## Log Monitoring

### Real-time Monitoring
```bash
# Monitor error log in real-time
python monitor_logs.py watch error

# Monitor all recent logs
python monitor_logs.py all

# Show last 50 lines of a specific log
python monitor_logs.py tail django
```

### Log Analysis
```bash
# Generate comprehensive report
python log_analyzer.py

# Analyze specific log types
python log_analyzer.py errors
python log_analyzer.py requests
python log_analyzer.py security
```

## Production Setup

### 1. Environment Configuration
Copy `.env.production` to `.env` and update the values:
```bash
cp .env.production .env
```

**Important:** Update these values in production:
- `SECRET_KEY` - Generate a new secret key
- `EMAIL_HOST_*` - Configure SMTP settings
- `ADMIN_EMAIL` - Set admin email for error notifications
- `ALLOWED_HOSTS` - Set your domain names
- `DEBUG=False` - Ensure debug is disabled

### 2. Email Notifications
When `DEBUG=False`, critical errors are automatically emailed to administrators. Configure SMTP settings in your `.env` file:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@domain.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
ADMIN_EMAIL=admin@transportandlogisticssummit.ng
```

### 3. Log Rotation
Set up daily log rotation with cron:
```bash
# Add to crontab (crontab -e)
0 2 * * * /path/to/tlng_summit/rotate_logs.sh
```

## Log Levels

- **ERROR** - Critical errors requiring immediate attention
- **WARNING** - Issues that should be monitored
- **INFO** - General application events
- **DEBUG** - Detailed diagnostic information (development only)

## Common Log Patterns

### Error Examples
```
ERROR 2024-08-14 10:30:15,123 summit.views 12345 67890 Error in registration view: ValidationError
```

### Request Examples
```
INFO 2024-08-14 10:30:15,123 django.request 12345 67890 "GET /register/ HTTP/1.1" 200 1234
```

### Security Examples
```
WARNING 2024-08-14 10:30:15,123 django.security 12345 67890 Suspicious operation: Invalid form submission
```

## Best Practices

1. **Regular Monitoring**: Check logs daily, especially error.log
2. **Set Up Alerts**: Configure email notifications for critical errors
3. **Archive Old Logs**: Use the rotation script to manage disk space
4. **Security Review**: Regularly check security.log for suspicious activity
5. **Performance Monitoring**: Monitor django.log for slow requests

## Troubleshooting

### Log Files Not Created
- Ensure the `logs/` directory exists and is writable
- Check file permissions on the logs directory
- Verify Django settings are correctly configured

### Email Notifications Not Working
- Test SMTP settings with Django shell
- Check spam folder for error emails
- Verify `ADMIN_EMAIL` and `DEFAULT_FROM_EMAIL` settings

### High Disk Usage
- Run log rotation manually: `./rotate_logs.sh`
- Check for large log files: `du -h logs/`
- Adjust log rotation frequency if needed

## Custom Logging in Views

Add logging to your custom views:

```python
import logging

logger = logging.getLogger('summit')

def my_view(request):
    try:
        logger.info(f"View accessed from {request.META.get('REMOTE_ADDR')}")
        # Your view logic here
        logger.info("View completed successfully")
    except Exception as e:
        logger.error(f"Error in my_view: {str(e)}", exc_info=True)
        raise
```

## Monitoring Dashboard

For production, consider setting up:
- **Grafana** + **Loki** for log visualization
- **Sentry** for error tracking
- **New Relic** or **DataDog** for application monitoring

## Security Notes

- Never log sensitive information (passwords, API keys, personal data)
- Regularly review and archive old logs
- Protect log files with appropriate file permissions
- Monitor for log injection attempts in user inputs