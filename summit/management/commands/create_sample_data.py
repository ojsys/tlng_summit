from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from summit.models import (
    SiteSettings, EventContent, Speaker, SponsorshipLevel, 
    AwardCategory, ExhibitionPackage
)


class Command(BaseCommand):
    help = 'Create sample data for the summit application'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create Site Settings
        if not SiteSettings.objects.exists():
            site_settings = SiteSettings.objects.create(
                site_name="Nigeria Transport and Logistics Summit and Awards",
                contact_email="info@transportandlogisticssummit.ng",
                contact_phone="+234 801 234 5678",
                social_facebook="https://facebook.com/tlngsummit",
                social_twitter="https://twitter.com/tlngsummit",
                social_linkedin="https://linkedin.com/company/tlngsummit",
                social_instagram="https://instagram.com/tlngsummit"
            )
            self.stdout.write(self.style.SUCCESS('✓ Site settings created'))
        else:
            self.stdout.write(self.style.WARNING('Site settings already exist'))

        # Create Event Content
        if not EventContent.objects.exists():
            event_date = timezone.now() + timedelta(days=90)  # 3 months from now
            event_content = EventContent.objects.create(
                title="Nigeria Transport and Logistics Summit and Awards 2024",
                subtitle="Join industry leaders, innovators, and stakeholders as we shape the future of Nigeria's transport and logistics sector.",
                event_date=event_date,
                venue="Eko Hotels & Suites, Lagos",
                about_title="Nigeria's Premier Transport & Logistics Event",
                about_text="The Nigeria Transport and Logistics Summit and Awards brings together industry leaders, innovators, and decision-makers to shape the future of the transport and logistics sector. This premier event features cutting-edge insights, networking opportunities, and recognition of excellence in the industry.",
                hero_badge_text="Registration Open",
                stat_1_number="500+",
                stat_1_label="Expected Attendees",
                stat_2_number="50+",
                stat_2_label="Industry Speakers",
                stat_3_number="100+",
                stat_3_label="Companies",
                stat_4_number="2",
                stat_4_label="Days",
                feature_1_title="Networking Opportunities",
                feature_1_description="Connect with 500+ industry professionals and decision-makers",
                feature_2_title="Innovation Showcase",
                feature_2_description="Discover the latest technologies and solutions transforming the industry",
                feature_3_title="Awards Ceremony",
                feature_3_description="Celebrate excellence and recognize outstanding achievements in transport and logistics"
            )
            self.stdout.write(self.style.SUCCESS('✓ Event content created'))
        else:
            self.stdout.write(self.style.WARNING('Event content already exists'))

        # Create Sample Speakers
        speakers_data = [
            {
                'name': 'Dr. Amina Mohammed',
                'title': 'Deputy Secretary-General, United Nations',
                'company': 'United Nations',
                'bio': 'Dr. Amina Mohammed is the Deputy Secretary-General of the United Nations and a leading advocate for sustainable development and infrastructure investment in Africa.',
                'is_featured': True,
                'order': 1
            },
            {
                'name': 'Engr. Mu\'azu Sambo',
                'title': 'Minister of Transportation',
                'company': 'Federal Ministry of Transportation',
                'bio': 'Engineer Mu\'azu Sambo serves as Nigeria\'s Minister of Transportation, overseeing the development and implementation of transportation policies across the country.',
                'is_featured': True,
                'order': 2
            },
            {
                'name': 'Mrs. Hadiza Bala Usman',
                'title': 'Former Managing Director',
                'company': 'Nigerian Ports Authority',
                'bio': 'Mrs. Hadiza Bala Usman is a distinguished leader in Nigeria\'s maritime sector, having served as Managing Director of the Nigerian Ports Authority.',
                'is_featured': True,
                'order': 3
            },
            {
                'name': 'Dr. Allen Onyema',
                'title': 'Chairman/CEO',
                'company': 'Air Peace Limited',
                'bio': 'Dr. Allen Onyema is the Chairman and CEO of Air Peace Limited, one of Nigeria\'s leading airlines, and a prominent figure in the aviation industry.',
                'is_featured': False,
                'order': 4
            },
            {
                'name': 'Capt. Niyi Adebayo',
                'title': 'Former Minister of Industry, Trade and Investment',
                'company': 'Federal Government of Nigeria',
                'bio': 'Captain Niyi Adebayo brings extensive experience in trade, investment, and economic development to discussions on transport and logistics.',
                'is_featured': False,
                'order': 5
            },
            {
                'name': 'Mrs. Funmi Ogbue',
                'title': 'Managing Director',
                'company': 'DHL Express Nigeria',
                'bio': 'Mrs. Funmi Ogbue leads DHL Express Nigeria, bringing international logistics expertise and best practices to the Nigerian market.',
                'is_featured': False,
                'order': 6
            }
        ]

        for speaker_data in speakers_data:
            speaker, created = Speaker.objects.get_or_create(
                name=speaker_data['name'],
                defaults=speaker_data
            )
            if created:
                self.stdout.write(f'✓ Speaker created: {speaker.name}')
            else:
                self.stdout.write(f'Speaker already exists: {speaker.name}')

        # Create Sponsorship Levels
        sponsorship_levels = [
            {
                'name': 'platinum',
                'price': 5000000.00,
                'benefits': 'Premium booth space (6m x 6m)\nLogo on all marketing materials\nKeynote speaking opportunity\n10 complimentary tickets\nExclusive networking session\nPremium branding throughout venue',
                'max_sponsors': 2,
                'order': 1
            },
            {
                'name': 'gold',
                'price': 3000000.00,
                'benefits': 'Standard booth space (4m x 4m)\nLogo on select marketing materials\nPanel discussion opportunity\n6 complimentary tickets\nNetworking session access\nBranding in common areas',
                'max_sponsors': 5,
                'order': 2
            },
            {
                'name': 'silver',
                'price': 1500000.00,
                'benefits': 'Booth space (3m x 3m)\nLogo on event materials\n4 complimentary tickets\nNetworking session access\nBranding opportunities',
                'max_sponsors': 10,
                'order': 3
            },
            {
                'name': 'bronze',
                'price': 750000.00,
                'benefits': 'Exhibition space (2m x 2m)\nLogo recognition\n2 complimentary tickets\nNetworking access',
                'max_sponsors': 20,
                'order': 4
            },
            {
                'name': 'supporting',
                'price': 300000.00,
                'benefits': 'Logo recognition\n1 complimentary ticket\nNetworking access',
                'max_sponsors': 50,
                'order': 5
            }
        ]

        for level_data in sponsorship_levels:
            level, created = SponsorshipLevel.objects.get_or_create(
                name=level_data['name'],
                defaults=level_data
            )
            if created:
                self.stdout.write(f'✓ Sponsorship level created: {level.get_name_display()}')
            else:
                self.stdout.write(f'Sponsorship level already exists: {level.get_name_display()}')

        # Create Award Categories
        award_categories = [
            {
                'name': 'Transport Company of the Year',
                'description': 'Recognizing the most outstanding transport company that has demonstrated excellence in service delivery, innovation, and customer satisfaction.',
                'criteria': 'Service quality\nInnovation in operations\nCustomer satisfaction\nSafety record\nContribution to industry development',
                'order': 1
            },
            {
                'name': 'Logistics Provider of the Year',
                'description': 'Honoring the logistics company that has excelled in supply chain management, warehousing, and distribution services.',
                'criteria': 'Operational efficiency\nTechnology adoption\nCustomer service\nNetwork coverage\nSustainability practices',
                'order': 2
            },
            {
                'name': 'Innovation in Transport Technology',
                'description': 'Celebrating groundbreaking technological solutions that have transformed transport and logistics operations.',
                'criteria': 'Technological innovation\nImpact on industry\nScalability\nUser adoption\nProblem-solving capability',
                'order': 3
            },
            {
                'name': 'Outstanding Leadership in Transport',
                'description': 'Recognizing individual leaders who have made significant contributions to the development of Nigeria\'s transport sector.',
                'criteria': 'Leadership qualities\nIndustry impact\nVision and strategy\nMentorship\nCommunity contribution',
                'order': 4
            },
            {
                'name': 'Best Safety Initiative',
                'description': 'Acknowledging organizations that have implemented exceptional safety measures and protocols.',
                'criteria': 'Safety record\nInnovative safety measures\nEmployee training\nCompliance standards\nIncident reduction',
                'order': 5
            },
            {
                'name': 'Sustainability Excellence',
                'description': 'Honoring companies that have demonstrated outstanding commitment to environmental sustainability.',
                'criteria': 'Environmental impact reduction\nSustainable practices\nGreen technology adoption\nCarbon footprint reduction\nCommunity engagement',
                'order': 6
            },
            {
                'name': 'Young Professional of the Year',
                'description': 'Celebrating young professionals under 35 who have made remarkable contributions to the transport and logistics industry.',
                'criteria': 'Professional achievements\nInnovation and creativity\nLeadership potential\nIndustry contribution\nPeer recognition',
                'order': 7
            },
            {
                'name': 'Customer Service Excellence',
                'description': 'Recognizing organizations that have set exceptional standards in customer service and satisfaction.',
                'criteria': 'Customer satisfaction scores\nService innovation\nComplaint resolution\nCustomer retention\nService accessibility',
                'order': 8
            }
        ]

        for category_data in award_categories:
            category, created = AwardCategory.objects.get_or_create(
                name=category_data['name'],
                defaults=category_data
            )
            if created:
                self.stdout.write(f'✓ Award category created: {category.name}')
            else:
                self.stdout.write(f'Award category already exists: {category.name}')

        # Create Exhibition Packages
        exhibition_packages = [
            {
                'name': 'standard',
                'price': 500000.00,
                'space_size': '3m x 3m',
                'features': 'Basic booth setup\nElectricity connection\nCarpeting\nCompany name board\n2 chairs and 1 table',
                'max_exhibitors': 50,
                'order': 1
            },
            {
                'name': 'premium',
                'price': 750000.00,
                'space_size': '4m x 4m',
                'features': 'Enhanced booth setup\nElectricity and lighting\nCarpeting and walls\nCompany name board\n4 chairs and 2 tables\nStorage space',
                'max_exhibitors': 30,
                'order': 2
            },
            {
                'name': 'corner',
                'price': 900000.00,
                'space_size': '4m x 4m',
                'features': 'Corner location\nEnhanced visibility\nElectricity and lighting\nCustom booth design\n4 chairs and 2 tables\nStorage space',
                'max_exhibitors': 20,
                'order': 3
            },
            {
                'name': 'island',
                'price': 1500000.00,
                'space_size': '6m x 6m',
                'features': 'Island booth with 360° access\nPremium location\nFull electricity and lighting\nCustom design and setup\n6 chairs and 3 tables\nStorage and meeting space\nDedicated networking area',
                'max_exhibitors': 10,
                'order': 4
            }
        ]

        for package_data in exhibition_packages:
            package, created = ExhibitionPackage.objects.get_or_create(
                name=package_data['name'],
                defaults=package_data
            )
            if created:
                self.stdout.write(f'✓ Exhibition package created: {package.get_name_display()}')
            else:
                self.stdout.write(f'Exhibition package already exists: {package.get_name_display()}')

        self.stdout.write(self.style.SUCCESS('\n🎉 Sample data creation completed successfully!'))
        self.stdout.write(self.style.SUCCESS('You can now visit the admin panel to add sponsors and customize the content.'))