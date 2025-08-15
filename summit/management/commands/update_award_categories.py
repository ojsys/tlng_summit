from django.core.management.base import BaseCommand
from summit.models import AwardCategory


class Command(BaseCommand):
    help = 'Update award categories with the new list'

    def handle(self, *args, **options):
        # Clear existing categories
        self.stdout.write(self.style.WARNING('Clearing existing award categories...'))
        AwardCategory.objects.all().delete()
        
        # Define new categories
        categories = [
            {
                'name': 'Governor of the Year in Transport Infrastructure Development (Six Geo-Political Zones)',
                'description': 'Recognizing governors who have demonstrated exceptional leadership in developing transport infrastructure within their geo-political zones.',
                'criteria': 'Projects completed, impact on transport network, innovation in infrastructure development, cross-state collaboration'
            },
            {
                'name': 'Governor of the Year in Road Infrastructure Development',
                'description': 'Honoring the governor who has made outstanding contributions to road infrastructure development.',
                'criteria': 'Quality of road projects, coverage area, completion rate, sustainability measures'
            },
            {
                'name': 'Distinguished Public Servant of the Year in Transport and Road Infrastructure Development',
                'description': 'Celebrating public servants who have shown exemplary service in transport and road infrastructure.',
                'criteria': 'Leadership, innovation, project delivery, policy implementation, public service impact'
            },
            {
                'name': 'Distinguished Transport and Logistics Legislator of the Year',
                'description': 'Recognizing legislators who have championed transport and logistics through effective legislation.',
                'criteria': 'Legislative contributions, policy advocacy, sector development support, stakeholder engagement'
            },
            {
                'name': 'Distinguished Trailblazers Award',
                'description': 'Honoring individuals or organizations that have pioneered innovative solutions in transport and logistics.',
                'criteria': 'Innovation, market disruption, industry leadership, measurable impact, sustainability'
            },
            {
                'name': 'Leadership Award in Transport Logistics in Governance',
                'description': 'Recognizing outstanding leadership in transport logistics governance and administration.',
                'criteria': 'Governance excellence, policy implementation, stakeholder management, results delivery'
            },
            {
                'name': 'Local Govt. Chairman of the Year in Road Infrastructure Development',
                'description': 'Celebrating local government leaders who have excelled in road infrastructure development.',
                'criteria': 'Local road projects, community impact, resource management, accessibility improvement'
            },
            {
                'name': 'Leadership Award in Transport & Logistics Infrastructure Financing',
                'description': 'Honoring leaders who have demonstrated excellence in financing transport and logistics infrastructure.',
                'criteria': 'Financing innovation, project funding success, financial sustainability, partnership development'
            },
            {
                'name': 'State Transport Ministry of the Year',
                'description': 'Recognizing the state transport ministry that has shown outstanding performance and service delivery.',
                'criteria': 'Policy implementation, service delivery, stakeholder satisfaction, innovation in operations'
            },
            {
                'name': 'State Transport Parastatal of the Year',
                'description': 'Celebrating the state transport parastatal with the best performance in service delivery.',
                'criteria': 'Operational efficiency, service quality, customer satisfaction, financial performance'
            },
            {
                'name': 'State Traffic Management Agency of the Year',
                'description': 'Honoring the traffic management agency that has excelled in traffic control and road safety.',
                'criteria': 'Traffic flow improvement, road safety records, technology adoption, public compliance'
            },
            {
                'name': 'Rural Transport & Logistics Project of the Year',
                'description': 'Recognizing outstanding projects that have improved rural transport and logistics connectivity.',
                'criteria': 'Rural connectivity impact, community benefit, sustainability, innovation in rural transport'
            },
            {
                'name': 'State Owned Road Transport Company of the Year',
                'description': 'Celebrating the state-owned road transport company with exceptional service delivery.',
                'criteria': 'Service reliability, fleet management, passenger satisfaction, operational efficiency'
            },
            {
                'name': 'Road Transport Company of the Year',
                'description': 'Honoring the private road transport company that has demonstrated excellence in operations.',
                'criteria': 'Service quality, safety records, customer satisfaction, operational efficiency, route coverage'
            },
            {
                'name': 'Company of the Year in CNG Infrastructure Development',
                'description': 'Recognizing the company leading in compressed natural gas infrastructure development.',
                'criteria': 'CNG infrastructure rollout, environmental impact, technology adoption, market penetration'
            },
            {
                'name': 'Electric Vehicle Brand of the Year',
                'description': 'Celebrating the electric vehicle brand making the most significant impact in the Nigerian market.',
                'criteria': 'Market adoption, technology innovation, charging infrastructure, environmental impact'
            },
            {
                'name': 'Auto Company of the Year',
                'description': 'Honoring the automotive company with outstanding performance and market presence.',
                'criteria': 'Sales performance, customer satisfaction, innovation, after-sales service, market share'
            },
            {
                'name': 'Automobile Maker of the Year',
                'description': 'Recognizing the automobile manufacturer with the best production and quality standards.',
                'criteria': 'Production quality, innovation, local content, export performance, technology transfer'
            },
            {
                'name': 'Airline of the Year',
                'description': 'Celebrating the airline that has demonstrated excellence in aviation services.',
                'criteria': 'Safety records, on-time performance, customer service, route network, operational efficiency'
            },
            {
                'name': 'Helicopter Aviation Service Provider of the Year',
                'description': 'Honoring the helicopter service provider with outstanding performance in aviation.',
                'criteria': 'Safety standards, service reliability, fleet maintenance, customer satisfaction, operational coverage'
            },
            {
                'name': 'Logistics Company of the Year',
                'description': 'Recognizing the logistics company that has excelled in comprehensive logistics services.',
                'criteria': 'Service delivery, technology adoption, customer satisfaction, operational efficiency, market reach'
            },
            {
                'name': 'Logistics Startup of the Year',
                'description': 'Celebrating the most promising logistics startup with innovative solutions.',
                'criteria': 'Innovation, growth potential, market disruption, technology adoption, scalability'
            },
            {
                'name': 'Haulage Company of the Year',
                'description': 'Honoring the haulage company with exceptional freight transportation services.',
                'criteria': 'Fleet efficiency, safety records, delivery reliability, customer satisfaction, route optimization'
            },
            {
                'name': 'Supply Chain Excellence Company of the Year',
                'description': 'Recognizing the company that has demonstrated excellence in supply chain management.',
                'criteria': 'Supply chain optimization, cost efficiency, delivery performance, technology integration, sustainability'
            },
            {
                'name': 'Marine Logistics Company of the Year',
                'description': 'Celebrating excellence in marine logistics and water transportation services.',
                'criteria': 'Maritime operations efficiency, safety standards, cargo handling, environmental compliance'
            },
            {
                'name': 'Fleet Management Company of the Year',
                'description': 'Honoring the company providing outstanding fleet management services.',
                'criteria': 'Fleet optimization, maintenance standards, technology adoption, cost efficiency, client satisfaction'
            },
            {
                'name': 'Freight Forwarding Company of the Year',
                'description': 'Recognizing excellence in freight forwarding and cargo management services.',
                'criteria': 'Cargo handling efficiency, documentation accuracy, customer service, international reach'
            },
            {
                'name': 'Most Innovative Transport Technology Brand of the Year',
                'description': 'Celebrating the brand leading in transport technology innovation.',
                'criteria': 'Technology innovation, market impact, adoption rate, user experience, industry disruption'
            },
            {
                'name': 'Shipping Company of the Year',
                'description': 'Honoring the shipping company with outstanding maritime transportation services.',
                'criteria': 'Fleet performance, cargo capacity, route coverage, safety records, environmental compliance'
            },
            {
                'name': 'Shipping Agent of the Year',
                'description': 'Recognizing the shipping agent providing exceptional vessel and cargo services.',
                'criteria': 'Agency services quality, port operations efficiency, customer relations, regulatory compliance'
            },
            {
                'name': 'Maritime Operator of the Year',
                'description': 'Celebrating excellence in maritime operations and vessel management.',
                'criteria': 'Operational efficiency, safety management, environmental stewardship, crew welfare'
            },
            {
                'name': 'Maritime Security and Safety Provider of the Year',
                'description': 'Honoring the provider of outstanding maritime security and safety services.',
                'criteria': 'Security effectiveness, safety protocols, emergency response, training programs, compliance'
            },
            {
                'name': 'Domestic Gas Distribution Company of the Year',
                'description': 'Recognizing excellence in domestic gas distribution and delivery services.',
                'criteria': 'Distribution network, safety standards, customer service, market penetration, infrastructure development'
            },
            {
                'name': 'Energy Transport & Logistics Brand of the Year',
                'description': 'Celebrating the brand leading in energy transport and logistics solutions.',
                'criteria': 'Energy logistics efficiency, safety protocols, environmental compliance, technology adoption'
            },
            {
                'name': 'Transport Support Service Provider of the Year (Upstream)',
                'description': 'Honoring upstream transport support service providers with exceptional performance.',
                'criteria': 'Upstream operations support, safety standards, reliability, technical expertise, client satisfaction'
            },
            {
                'name': 'Transport Support Service Provider of the Year (Downstream)',
                'description': 'Recognizing downstream transport support service providers for outstanding services.',
                'criteria': 'Downstream operations efficiency, service quality, market reach, customer satisfaction'
            },
            {
                'name': 'Excellence in Local Content in Transport & Logistics',
                'description': 'Celebrating organizations promoting local content in transport and logistics.',
                'criteria': 'Local content percentage, skills transfer, job creation, technology transfer, community impact'
            },
            {
                'name': 'Green and Sustainable Transport Company of the Year',
                'description': 'Honoring the company leading in environmentally sustainable transport solutions.',
                'criteria': 'Environmental impact reduction, sustainable practices, green technology adoption, carbon footprint'
            },
            {
                'name': 'Pipeline Transport & Distribution Excellence',
                'description': 'Recognizing excellence in pipeline transport and distribution operations.',
                'criteria': 'Pipeline safety, operational efficiency, environmental compliance, maintenance standards, technology adoption'
            }
        ]
        
        # Create new categories
        self.stdout.write(self.style.SUCCESS('Creating new award categories...'))
        for i, category_data in enumerate(categories, 1):
            category = AwardCategory.objects.create(
                name=category_data['name'],
                description=category_data['description'],
                criteria=category_data['criteria'],
                order=i,
                is_active=True
            )
            self.stdout.write(f'✓ Created: {category.name}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(categories)} award categories!')
        )