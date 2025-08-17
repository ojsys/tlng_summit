from django.core.management.base import BaseCommand
from summit.models import Sponsor, SponsorshipLevel


class Command(BaseCommand):
    help = 'Check sponsor data and logo availability'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== SPONSOR CHECK REPORT ==='))
        
        # Check sponsorship levels
        levels = SponsorshipLevel.objects.all()
        self.stdout.write(f'\nSponsorship Levels ({levels.count()}):')
        for level in levels:
            self.stdout.write(f'  - {level.name} ({level.get_name_display()})')
        
        # Check sponsors
        sponsors = Sponsor.objects.all()
        self.stdout.write(f'\nAll Sponsors ({sponsors.count()}):')
        for sponsor in sponsors:
            logo_status = "✓ Has logo" if sponsor.logo else "✗ No logo"
            active_status = "Active" if sponsor.is_active else "Inactive"
            self.stdout.write(f'  - {sponsor.name}')
            self.stdout.write(f'    Level: {sponsor.level.name} ({sponsor.level.get_name_display()})')
            self.stdout.write(f'    Logo: {logo_status}')
            self.stdout.write(f'    Status: {active_status}')
            if sponsor.logo:
                self.stdout.write(f'    Logo path: {sponsor.logo.url}')
            self.stdout.write('')
        
        # Check by level
        platinum_gold = sponsors.filter(level__name__in=['platinum', 'gold'], is_active=True)
        silver_bronze = sponsors.filter(level__name__in=['silver', 'bronze'], is_active=True)
        
        self.stdout.write(f'Principal Sponsors (Platinum/Gold): {platinum_gold.count()}')
        for sponsor in platinum_gold:
            self.stdout.write(f'  - {sponsor.name} ({sponsor.level.name})')
        
        self.stdout.write(f'\nSupporting Partners (Silver/Bronze): {silver_bronze.count()}')
        for sponsor in silver_bronze:
            self.stdout.write(f'  - {sponsor.name} ({sponsor.level.name})')
        
        # Check for sponsors without logos
        no_logo_sponsors = sponsors.filter(logo__isnull=True, is_active=True)
        if no_logo_sponsors.exists():
            self.stdout.write(self.style.WARNING(f'\nSponsors without logos ({no_logo_sponsors.count()}):'))
            for sponsor in no_logo_sponsors:
                self.stdout.write(f'  - {sponsor.name}')
        else:
            self.stdout.write(self.style.SUCCESS('\n✓ All active sponsors have logos!'))