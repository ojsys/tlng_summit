# Production Deployment Guide

## For Award Categories Update

### Method 1: Django Management Command (Recommended)
```bash
# SSH into your production server
cd /path/to/your/project
source venv/bin/activate

# Run the management command
python manage.py update_award_categories
```

### Method 2: Django Migration (Safest)
```bash
# Upload the migration file to production
# Then run:
python manage.py migrate
```

### Method 3: Manual through Admin
1. Login to Django Admin: `https://yourdomain.com/admin/`
2. Go to **Summit > Award Categories**
3. Delete existing categories
4. Add the 39 new categories manually

## For Logo Updates

### Step 1: Deploy Code Changes
```bash
# Upload the updated files to production:
# - summit/models.py (updated SiteSettings model)
# - summit/admin.py (updated admin interface)
# - templates/summit/base.html (updated navigation template)
```

### Step 2: Run Migrations
```bash
cd /path/to/your/project
source venv/bin/activate
python manage.py migrate
```

### Step 3: Add Logos via Admin
1. Login to Django Admin: `https://yourdomain.com/admin/`
2. Go to **Site Settings**
3. Upload:
   - **Primary Organizer Logo** (appears first)
   - **Site Logo** (summit logo, appears second)

## Files Changed
- `summit/models.py` - Added primary_organizer_logo field
- `summit/admin.py` - Updated admin interface
- `templates/summit/base.html` - Updated navigation and footer
- `summit/management/commands/update_award_categories.py` - New command

## Backup Recommendations
```bash
# Backup database before making changes
mysqldump -u username -p database_name > backup_$(date +%Y%m%d).sql

# Backup media files
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

## Verification Steps
1. Check navigation displays both logos correctly
2. Verify admin interface shows new logo fields
3. Test responsive design on mobile devices
4. Confirm award categories are updated (39 total)
5. Test nomination form displays new categories