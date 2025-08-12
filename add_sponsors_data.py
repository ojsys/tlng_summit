import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tlng_summit_project.settings')
django.setup()

from summit.models import SponsorshipLevel, Sponsor

def create_sample_sponsors():
    # Get existing sponsorship levels
    platinum = SponsorshipLevel.objects.filter(name='platinum').first()
    gold = SponsorshipLevel.objects.filter(name='gold').first()
    silver = SponsorshipLevel.objects.filter(name='silver').first()
    bronze = SponsorshipLevel.objects.filter(name='bronze').first()
    
    sample_sponsors = [
        {
            'name': 'Nigerian National Petroleum Corporation',
            'level': platinum,
            'website': 'https://nnpc.gov.ng',
            'description': 'Nigeria\'s leading oil and gas company',
            'is_active': True,
        },
        {
            'name': 'Access Bank',
            'level': gold,
            'website': 'https://www.accessbankplc.com',
            'description': 'Leading financial institution supporting transport infrastructure',
            'is_active': True,
        },
        {
            'name': 'Dangote Group',
            'level': platinum,
            'website': 'https://www.dangote.com',
            'description': 'Africa\'s largest conglomerate with extensive logistics operations',
            'is_active': True,
        },
        {
            'name': 'MTN Nigeria',
            'level': gold,
            'website': 'https://www.mtnonline.com',
            'description': 'Leading telecommunications company enabling digital logistics',
            'is_active': True,
        },
        {
            'name': 'Nigerian Ports Authority',
            'level': silver,
            'website': 'https://nigerianports.gov.ng',
            'description': 'Managing Nigeria\'s port infrastructure and logistics',
            'is_active': True,
        },
        {
            'name': 'Julius Berger',
            'level': silver,
            'website': 'https://www.julius-berger.com',
            'description': 'Leading construction and infrastructure development company',
            'is_active': True,
        },
        {
            'name': 'Nigerian Railway Corporation',
            'level': bronze,
            'website': 'https://www.nrc.gov.ng',
            'description': 'Nigeria\'s national railway operator',
            'is_active': True,
        },
        {
            'name': 'Lafarge Africa',
            'level': bronze,
            'website': 'https://www.lafarge.com.ng',
            'description': 'Building materials company with extensive logistics network',
            'is_active': True,
        },
    ]
    
    created_count = 0
    for sponsor_data in sample_sponsors:
        if sponsor_data['level']:  # Only create if sponsorship level exists
            sponsor, created = Sponsor.objects.get_or_create(
                name=sponsor_data['name'],
                defaults=sponsor_data
            )
            if created:
                created_count += 1
                print(f"Created sponsor: {sponsor.name}")
            else:
                print(f"Sponsor already exists: {sponsor.name}")
    
    print(f"\nSample sponsors creation completed!")
    print(f"Created: {created_count} new sponsors")
    print(f"Total active sponsors: {Sponsor.objects.filter(is_active=True).count()}")

if __name__ == '__main__':
    create_sample_sponsors()