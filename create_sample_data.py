import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tlng_summit_project.settings')
django.setup()

from summit.models import (
    EventContent, Speaker, SponsorshipLevel, Sponsor,
    AwardCategory, ExhibitionPackage
)

def create_sample_data():
    # Create Event Content
    event_date = datetime.now() + timedelta(days=90)
    event_content, created = EventContent.objects.get_or_create(
        title="Nigeria Transport and Logistics Summit and Awards 2024",
        defaults={
            'description': 'Join Nigeria\'s premier transport and logistics industry event, bringing together leaders, innovators, and decision-makers to shape the future of the sector.',
            'event_date': event_date,
            'venue': 'Eko Hotels & Suites, Lagos, Nigeria',
            'about_text': '''The Nigeria Transport and Logistics Summit and Awards is the country's most significant gathering of transport and logistics professionals. This annual event serves as a platform for industry leaders to share insights, explore innovations, and recognize excellence within the sector.

Our summit features keynote presentations from industry titans, panel discussions on current challenges and opportunities, networking sessions for business development, and an awards ceremony celebrating outstanding achievements in the transport and logistics industry.

Whether you're a logistics provider, transport operator, technology innovator, or industry stakeholder, this event offers unparalleled opportunities to learn, network, and grow your business in Nigeria's dynamic transport sector.'''
        }
    )

    # Create Award Categories
    award_categories = [
        {
            'name': 'Logistics Company of the Year',
            'description': 'Recognizing the logistics company that has demonstrated exceptional service delivery, innovation, and growth.',
            'criteria': 'Judged on service quality, innovation, customer satisfaction, growth metrics, and industry impact.',
            'order': 1
        },
        {
            'name': 'Transport Innovation Award',
            'description': 'Honoring companies or individuals who have introduced groundbreaking innovations in transport technology.',
            'criteria': 'Evaluated based on innovation uniqueness, implementation success, industry adoption, and impact on efficiency.',
            'order': 2
        },
        {
            'name': 'Logistics Professional of the Year',
            'description': 'Celebrating an individual who has made outstanding contributions to the logistics industry.',
            'criteria': 'Professional achievements, industry leadership, mentorship, and contribution to sector development.',
            'order': 3
        },
        {
            'name': 'Best Supply Chain Solution',
            'description': 'Recognizing companies providing the most effective and innovative supply chain solutions.',
            'criteria': 'Solution effectiveness, client results, innovation level, scalability, and industry impact.',
            'order': 4
        },
        {
            'name': 'Sustainability in Transport Award',
            'description': 'Honoring organizations leading in environmentally sustainable transport practices.',
            'criteria': 'Environmental impact reduction, sustainability initiatives, green technology adoption, and industry leadership.',
            'order': 5
        },
        {
            'name': 'Young Logistics Professional',
            'description': 'Celebrating promising young professionals (under 35) making their mark in the industry.',
            'criteria': 'Career achievements, innovation, leadership potential, and contribution to industry growth.',
            'order': 6
        }
    ]

    for category_data in award_categories:
        AwardCategory.objects.get_or_create(
            name=category_data['name'],
            defaults=category_data
        )

    # Create Sponsorship Levels
    sponsorship_levels = [
        {
            'name': 'platinum',
            'price': 5000000.00,
            'benefits': '''Premium booth space (6m x 6m)
Speaking opportunity at main session
Logo on all event materials
Full-page advertisement in event magazine
VIP networking access
8 complimentary delegate passes
Dedicated social media mentions
Press release inclusion
Exhibition priority placement''',
            'max_sponsors': 2,
            'order': 1
        },
        {
            'name': 'gold',
            'price': 3000000.00,
            'benefits': '''Premium booth space (4m x 4m)
Panel discussion participation
Logo on main event materials
Half-page advertisement in event magazine
VIP networking access
6 complimentary delegate passes
Social media mentions
Exhibition premium placement''',
            'max_sponsors': 4,
            'order': 2
        },
        {
            'name': 'silver',
            'price': 1500000.00,
            'benefits': '''Standard booth space (3m x 3m)
Logo on event materials
Quarter-page advertisement in magazine
Networking access
4 complimentary delegate passes
Social media mentions
Standard exhibition placement''',
            'max_sponsors': 6,
            'order': 3
        },
        {
            'name': 'bronze',
            'price': 800000.00,
            'benefits': '''Logo on event materials
Networking access
2 complimentary delegate passes
Social media mention
Exhibition opportunity''',
            'max_sponsors': 10,
            'order': 4
        }
    ]

    for level_data in sponsorship_levels:
        SponsorshipLevel.objects.get_or_create(
            name=level_data['name'],
            defaults=level_data
        )

    # Create Exhibition Packages
    exhibition_packages = [
        {
            'name': 'island',
            'price': 2000000.00,
            'space_size': '6m x 6m',
            'features': '''Island booth (accessible from all sides)
Premium location
Power supply included
Basic furniture package
Carpet flooring
Company signage
Lighting package
Networking access''',
            'max_exhibitors': 10,
            'order': 1
        },
        {
            'name': 'premium',
            'price': 1200000.00,
            'space_size': '4m x 4m',
            'features': '''Corner location
Power supply included
Basic furniture package
Carpet flooring
Company signage
Lighting
Networking access''',
            'max_exhibitors': 20,
            'order': 2
        },
        {
            'name': 'standard',
            'price': 600000.00,
            'space_size': '3m x 3m',
            'features': '''Standard booth space
Power supply included
Basic furniture
Company signage
Networking access''',
            'max_exhibitors': 40,
            'order': 3
        }
    ]

    for package_data in exhibition_packages:
        ExhibitionPackage.objects.get_or_create(
            name=package_data['name'],
            defaults=package_data
        )

    # Create Sample Speakers
    sample_speakers = [
        {
            'name': 'Dr. Amina Hassan',
            'title': 'CEO & Managing Director',
            'company': 'Nigerian Logistics Excellence Ltd',
            'bio': '''Dr. Amina Hassan is a visionary leader in Nigeria's logistics industry with over 20 years of experience. She founded Nigerian Logistics Excellence Ltd, which has become one of the country's leading logistics companies, serving major corporations across West Africa.

Dr. Hassan holds a Ph.D. in Supply Chain Management from the University of Lagos and an MBA from London Business School. She has been instrumental in implementing digital transformation initiatives that have revolutionized last-mile delivery in Nigeria.

Under her leadership, the company has expanded operations to 15 African countries and has been recognized for its innovative use of technology in logistics operations. She is a frequent speaker at international logistics conferences and serves on the board of the African Logistics Association.''',
            'linkedin_url': 'https://linkedin.com/in/amina-hassan',
            'is_featured': True,
            'order': 1
        },
        {
            'name': 'Engr. Tunde Bakare',
            'title': 'Director of Transport Innovation',
            'company': 'Federal Ministry of Transportation',
            'bio': '''Engr. Tunde Bakare is a seasoned transport infrastructure expert with extensive experience in railway systems and urban transport development. He has been instrumental in Nigeria's railway modernization projects and the development of integrated transport systems.

With a background in Civil Engineering from the University of Ibadan and a Master's in Transportation Engineering from Imperial College London, Engr. Bakare has overseen major transport infrastructure projects worth over $2 billion.

He has worked on the Lagos-Ibadan railway project, the Abuja Light Rail system, and is currently leading the development of Nigeria's National Transport Master Plan. His expertise spans railway systems, urban planning, and sustainable transport solutions.''',
            'twitter_url': 'https://twitter.com/tunde_bakare',
            'is_featured': True,
            'order': 2
        },
        {
            'name': 'Mrs. Funmi Ogbonna',
            'title': 'Chief Operations Officer',
            'company': 'West African Shipping Lines',
            'bio': '''Mrs. Funmi Ogbonna is a maritime logistics expert with over 18 years of experience in shipping and port operations. She currently serves as the Chief Operations Officer at West African Shipping Lines, where she oversees operations across 12 ports in West Africa.

She holds an MBA in International Business from the Lagos Business School and is a certified member of the Chartered Institute of Logistics and Transport. Mrs. Ogbonna has been a pioneer in implementing digital solutions for port operations and cargo tracking.

Her leadership has resulted in a 40% improvement in port efficiency and reduced cargo dwell time across the company's operations. She is actively involved in mentoring young professionals in the maritime industry.''',
            'linkedin_url': 'https://linkedin.com/in/funmi-ogbonna',
            'is_featured': True,
            'order': 3
        },
        {
            'name': 'Mr. Kelechi Okonkwo',
            'title': 'Founder & CTO',
            'company': 'LogiTech Solutions Nigeria',
            'bio': '''Mr. Kelechi Okonkwo is a technology entrepreneur who has revolutionized logistics through innovative digital solutions. As the Founder and CTO of LogiTech Solutions Nigeria, he has developed cutting-edge software platforms that optimize supply chain operations for businesses across Africa.

He graduated with a degree in Computer Science from the University of Nigeria, Nsukka, and later obtained a Master's in Artificial Intelligence from Carnegie Mellon University. His company's AI-powered logistics platform serves over 500 companies across Nigeria.

Kelechi's innovations have been recognized internationally, and he was named in Forbes' "30 Under 30" list for Technology in Africa. His solutions have helped reduce logistics costs by up to 30% for client companies.''',
            'twitter_url': 'https://twitter.com/kelechi_tech',
            'linkedin_url': 'https://linkedin.com/in/kelechi-okonkwo',
            'is_featured': True,
            'order': 4
        }
    ]

    for speaker_data in sample_speakers:
        Speaker.objects.get_or_create(
            name=speaker_data['name'],
            defaults=speaker_data
        )

    print("Sample data created successfully!")
    print(f"Created/Updated:")
    print(f"- Event Content: {EventContent.objects.count()}")
    print(f"- Award Categories: {AwardCategory.objects.count()}")
    print(f"- Sponsorship Levels: {SponsorshipLevel.objects.count()}")
    print(f"- Exhibition Packages: {ExhibitionPackage.objects.count()}")
    print(f"- Speakers: {Speaker.objects.count()}")

if __name__ == '__main__':
    create_sample_data()