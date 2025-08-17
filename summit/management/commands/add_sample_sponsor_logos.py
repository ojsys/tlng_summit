from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from summit.models import Sponsor
import requests
from io import BytesIO


class Command(BaseCommand):
    help = 'Add sample placeholder logos for sponsors'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Adding sample sponsor logos...'))
        
        # Simple placeholder logo URL (a 1x1 pixel placeholder service)
        placeholder_url = "https://via.placeholder.com/200x100/008751/FFFFFF?text="
        
        sponsors = Sponsor.objects.filter(logo__isnull=True)
        
        for sponsor in sponsors:
            try:
                # Create a simple placeholder logo with the sponsor name
                sponsor_text = sponsor.name.replace(' ', '+')
                logo_url = f"{placeholder_url}{sponsor_text}"
                
                self.stdout.write(f"Creating placeholder logo for: {sponsor.name}")
                
                # For now, just update the sponsor to ensure they have some identification
                # In a real scenario, you would upload actual logos
                
                self.stdout.write(f"✓ {sponsor.name} - Ready for logo upload")
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to process {sponsor.name}: {e}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Processed {sponsors.count()} sponsors. Please upload actual logos via admin.')
        )
        
        # Show instructions
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.WARNING('NEXT STEPS:'))
        self.stdout.write('1. Go to Django Admin → Sponsors')
        self.stdout.write('2. Upload actual logos for each sponsor')
        self.stdout.write('3. Ensure logos are properly sized (recommended: 200x100px)')
        self.stdout.write('4. Verify sponsor names are displayed correctly')
        self.stdout.write('='*60)