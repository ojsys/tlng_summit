from django.core.management.base import BaseCommand
from django.conf import settings
from summit.models import SiteSettings
import os


class Command(BaseCommand):
    help = 'Check favicon configuration and accessibility'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== FAVICON CHECK ==='))
        
        # Check site settings
        site_settings = SiteSettings.objects.first()
        if not site_settings:
            self.stdout.write(self.style.ERROR('No site settings found'))
            return
        
        self.stdout.write(f'Site name: {site_settings.site_name}')
        
        if site_settings.favicon:
            self.stdout.write(f'✅ Favicon configured: {site_settings.favicon.name}')
            self.stdout.write(f'Favicon URL: {site_settings.favicon.url}')
            
            # Check if file exists
            favicon_path = os.path.join(settings.MEDIA_ROOT, site_settings.favicon.name)
            if os.path.exists(favicon_path):
                file_size = os.path.getsize(favicon_path)
                self.stdout.write(f'✅ Favicon file exists: {favicon_path}')
                self.stdout.write(f'File size: {file_size:,} bytes ({file_size/1024:.1f} KB)')
                
                # Check file extension
                ext = os.path.splitext(site_settings.favicon.name)[1].lower()
                if ext in ['.ico', '.png', '.jpg', '.jpeg', '.gif', '.svg']:
                    self.stdout.write(f'✅ Valid favicon format: {ext}')
                else:
                    self.stdout.write(self.style.WARNING(f'⚠️  Unusual favicon format: {ext}'))
                
                # Check if it's accessible via URL
                self.stdout.write('\n--- Template Implementation ---')
                self.stdout.write('The favicon should appear in the browser tab with this HTML:')
                self.stdout.write(f'<link rel="icon" type="image/x-icon" href="{site_settings.favicon.url}">')
                
            else:
                self.stdout.write(self.style.ERROR(f'❌ Favicon file not found: {favicon_path}'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  No favicon uploaded'))
            self.stdout.write('To add a favicon:')
            self.stdout.write('1. Go to Django Admin → Site Settings')
            self.stdout.write('2. Upload a favicon file (preferably .ico or .png)')
            self.stdout.write('3. Save the settings')
        
        # Additional recommendations
        self.stdout.write('\n--- Recommendations ---')
        self.stdout.write('✓ For best results, use a 32x32 or 16x16 pixel .ico file')
        self.stdout.write('✓ Clear browser cache after uploading new favicon')
        self.stdout.write('✓ Test in incognito/private browsing mode')
        
        return site_settings.favicon is not None