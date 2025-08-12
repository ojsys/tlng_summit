# Nigeria Transport and Logistics Summit - cPanel Deployment Guide

## Prerequisites

Before deploying to cPanel, ensure you have:
- Access to your cPanel hosting account
- MySQL database access
- Python 3.11 support (verify with your hosting provider)
- SSH access (optional but recommended)

## Step 1: Prepare Your cPanel Environment

### 1.1 Create MySQL Database
1. Login to your cPanel
2. Navigate to "MySQL Databases"
3. Create a new database (e.g., `your_database_name`)
4. Create a database user with full privileges
5. Note down the database credentials:
   - Database name
   - Username
   - Password
   - Host (usually localhost)

### 1.2 Set Up Domain/Subdomain
1. In cPanel, go to "Subdomains" or use your main domain
2. Point the document root to `public_html` (this will be created)

## Step 2: Upload Application Files

### 2.1 Upload via File Manager or FTP
1. Upload all project files to your domain's root directory
2. Ensure these key files are in the root:
   - `passenger_wsgi.py`
   - `requirements.txt`
   - `manage.py`
   - All Django project files

### 2.2 Directory Structure
Your hosting directory should look like:
```
/
├── passenger_wsgi.py
├── requirements.txt
├── manage.py
├── tlng_summit_project/
│   ├── settings.py
│   ├── settings_production.py
│   └── ...
├── summit/
├── templates/
├── static/
└── public_html/ (will be created)
```

## Step 3: Install Python Dependencies

### 3.1 Via SSH (Recommended)
```bash
# Navigate to your project directory
cd ~/your-domain.com

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies (PyMySQL is used instead of mysqlclient for better cPanel compatibility)
pip install -r requirements.txt
```

### 3.2 Via cPanel Python App (Alternative)
1. Go to "Python App" in cPanel
2. Create new Python application
3. Set Python version to 3.11
4. Set application root to your project directory
5. Install packages from requirements.txt

## Step 4: Configure Environment Variables

### 4.1 Create Environment File
Create a `.env` file in your project root:
```bash
# Database Configuration
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306

# Django Secret Key (Generate new one at https://djecrety.ir/)
SECRET_KEY=your-super-secret-key-here

# Email Configuration (Optional)
EMAIL_HOST=mail.yourdomain.com
EMAIL_HOST_USER=noreply@yourdomain.com
EMAIL_HOST_PASSWORD=your_email_password
```

### 4.2 Update Production Settings
Edit `tlng_summit_project/settings_production.py`:
```python
# Update ALLOWED_HOSTS with your domain
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Ensure environment variables are loaded
import os
from dotenv import load_dotenv
load_dotenv()
```

## Step 5: Database Setup

### 5.1 Run Migrations
```bash
# Activate virtual environment
source venv/bin/activate

# Set production settings
export DJANGO_SETTINGS_MODULE=tlng_summit_project.settings_production

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (optional)
python manage.py loaddata initial_data.json
```

## Step 6: Static Files Configuration

### 6.1 Collect Static Files
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Collect static files
python manage.py collectstatic --noinput
```

### 6.2 Verify Static Files Structure
Ensure the following structure exists:
```
public_html/
├── static/
│   ├── css/
│   ├── js/
│   └── admin/
└── media/ (for uploaded files)
```

## Step 7: Configure Web Server

### 7.1 Update .htaccess
Ensure `.htaccess` is in your domain root with proper paths:
```apache
RewriteEngine On

# Handle static files
RewriteRule ^static/(.*)$ /public_html/static/$1 [L]
RewriteRule ^media/(.*)$ /public_html/media/$1 [L]

# Handle Django application
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ passenger_wsgi.py/$1 [L]
```

### 7.2 Update passenger_wsgi.py
Ensure the Python path is correct:
```python
#!/usr/bin/python3.11

import sys
import os

# Add your project directory to sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tlng_summit_project.settings_production')

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Step 8: Test Your Deployment

### 8.1 Basic Functionality Test
1. Visit your domain to see the homepage
2. Try navigating to different pages
3. Test admin panel at `/admin`
4. Upload test images to verify media handling

### 8.2 Admin Configuration
1. Login to admin panel
2. Configure Site Settings:
   - Site name and logo
   - Hero background image
   - Contact information
3. Add Event Content
4. Add sample speakers and sponsors

## Step 9: Security Considerations

### 9.1 File Permissions
Set appropriate permissions:
```bash
chmod 755 passenger_wsgi.py
chmod -R 755 static/
chmod -R 755 public_html/
chmod 600 .env
```

### 9.2 Hide Sensitive Files
Add to `.htaccess`:
```apache
# Hide sensitive files
<Files ".env">
    Order allow,deny
    Deny from all
</Files>

<Files "*.pyc">
    Order allow,deny
    Deny from all
</Files>
```

## Step 10: Maintenance

### 10.1 Regular Updates
- Keep Django and dependencies updated
- Regular database backups
- Monitor error logs

### 10.2 Backup Strategy
1. Database: Use cPanel's backup tools
2. Files: Regular file backups
3. Media: Backup uploaded images

## Troubleshooting

### Common Issues

**1. Internal Server Error (500)**
- Check error logs in cPanel
- Verify Python version and dependencies
- Ensure all environment variables are set

**2. Static Files Not Loading**
- Verify `collectstatic` was run
- Check file permissions
- Ensure correct paths in `.htaccess`

**3. Database Connection Issues**
- Verify database credentials
- Check database user permissions
- Ensure database exists
- Note: We use PyMySQL instead of mysqlclient for better cPanel compatibility

**4. Admin Panel Styling Issues**
- Run `python manage.py collectstatic`
- Check static files configuration
- Verify admin static files are collected

### Log Files
Check these log locations:
- cPanel Error Logs
- Django logs: `logs/django_errors.log`
- Access logs in cPanel

## Support

If you encounter issues:
1. Check cPanel error logs first
2. Verify all configuration files
3. Contact your hosting provider for Python/Django support
4. Ensure all dependencies are properly installed

## Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [cPanel Python Documentation](https://docs.cpanel.net/cpanel/software/python-apps/)
- [Generate Secret Key](https://djecrety.ir/)

---

**Note**: This guide assumes a standard cPanel setup. Some hosting providers may have specific requirements or configurations. Always consult your hosting provider's documentation for Python/Django specific instructions.