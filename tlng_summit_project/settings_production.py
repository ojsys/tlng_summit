"""
Production settings for Nigeria Transport and Logistics Summit
"""

from .settings import *
import os
from dotenv import load_dotenv
import pymysql

# Use PyMySQL as MySQLdb replacement
pymysql.install_as_MySQLdb()

# Load environment variables from .env file
load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update this with your actual domain
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'transportandlogisticssummit.ng,www.transportandlogisticssummit.ng').split(',')

# Database for production (MySQL/MariaDB)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'your_database_name'),
        'USER': os.environ.get('DB_USER', 'your_database_user'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'your_database_password'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Use HTTPS in production
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files settings for production
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public_html/static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

# Media files settings for production
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'public_html/media')

# Email settings (update with your email provider)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'mail.yourdomain.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'noreply@yourdomain.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'your_email_password')
DEFAULT_FROM_EMAIL = 'Nigeria Transport and Logistics Summit <noreply@yourdomain.com>'

# Logging configuration - disabled for cPanel deployment
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'logs/django_errors.log'),
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     },
# }

# Cache configuration (optional - for better performance)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache'),
    }
}

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # 2 weeks

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB

# Generate a new secret key for production
# You can generate one at: https://djecrety.ir/
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-CHANGE-THIS-IN-PRODUCTION')

# Ensure the secret key is set
if SECRET_KEY == 'django-insecure-CHANGE-THIS-IN-PRODUCTION':
    raise ValueError("You must set a SECRET_KEY environment variable for production")

# Optional: Django Admin URL (change for security)
# Add this to your main urls.py: path('admin-secure-url/', admin.site.urls),