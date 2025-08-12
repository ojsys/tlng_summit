from django.core.management.base import BaseCommand
from summit.models import SponsorshipLevel, Sponsor


class Command(BaseCommand):
    help = 'Add sample sponsor data to the summit application'

    def handle(self, *args, **options):
        self.stdout.write('Adding sample sponsors data...')

        # Sample sponsors data organized by level
        sponsors_data = {
            'platinum': [
                {
                    'name': 'Nigerian National Petroleum Corporation (NNPC)',
                    'website': 'https://www.nnpcgroup.com',
                    'description': 'Nigeria\'s premier oil and gas company, playing a pivotal role in the nation\'s energy and transportation infrastructure development.'
                },
                {
                    'name': 'Dangote Group',
                    'website': 'https://www.dangote.com',
                    'description': 'Africa\'s leading industrial conglomerate with significant investments in logistics, transportation, and infrastructure development.'
                }
            ],
            'gold': [
                {
                    'name': 'Access Bank Plc',
                    'website': 'https://www.accessbankplc.com',
                    'description': 'Leading financial institution supporting transport and logistics businesses across Nigeria and Africa.'
                },
                {
                    'name': 'MTN Nigeria',
                    'website': 'https://www.mtnonline.com',
                    'description': 'Telecommunications giant enabling digital transformation in transport and logistics through innovative solutions.'
                },
                {
                    'name': 'Zenith Bank Plc',
                    'website': 'https://www.zenithbank.com',
                    'description': 'Premier banking institution providing financial solutions to transport and logistics companies.'
                },
                {
                    'name': 'First Bank of Nigeria',
                    'website': 'https://www.firstbanknigeria.com',
                    'description': 'Nigeria\'s oldest banking institution with a strong commitment to supporting infrastructure development.'
                },
                {
                    'name': 'Nigerian Breweries Plc',
                    'website': 'https://www.nbplc.com',
                    'description': 'Leading beverage company with extensive distribution and logistics networks across Nigeria.'
                }
            ],
            'silver': [
                {
                    'name': 'Coscharis Group',
                    'website': 'https://www.coscharis.com',
                    'description': 'Automotive and technology company contributing to Nigeria\'s transport sector development.'
                },
                {
                    'name': 'Julius Berger Nigeria Plc',
                    'website': 'https://www.juliusberger.com',
                    'description': 'Premier construction and engineering company building Nigeria\'s transport infrastructure.'
                },
                {
                    'name': 'Nestle Nigeria Plc',
                    'website': 'https://www.nestle-cwa.com',
                    'description': 'Multinational food and beverage company with sophisticated supply chain and logistics operations.'
                },
                {
                    'name': 'Total Energies Nigeria',
                    'website': 'https://www.totalenergies.ng',
                    'description': 'Energy company supporting Nigeria\'s transport sector through fuel distribution and logistics.'
                },
                {
                    'name': 'Lafarge Africa Plc',
                    'website': 'https://www.lafarge.com.ng',
                    'description': 'Leading cement manufacturer with extensive distribution and logistics networks.'
                },
                {
                    'name': 'Unilever Nigeria Plc',
                    'website': 'https://www.unilever.com.ng',
                    'description': 'Consumer goods company with advanced supply chain and distribution systems.'
                },
                {
                    'name': 'Flour Mills of Nigeria Plc',
                    'website': 'https://www.fmnplc.com',
                    'description': 'Agribusiness and food manufacturing company with extensive logistics operations.'
                },
                {
                    'name': 'Honeywell Group',
                    'website': 'https://www.honeywellgroup.com',
                    'description': 'Diversified conglomerate with interests in infrastructure and transportation.'
                },
                {
                    'name': 'WAPCO (Lafarge WAPCO)',
                    'website': 'https://www.lafarge.com.ng',
                    'description': 'Cement manufacturing company with robust distribution and logistics network.'
                },
                {
                    'name': 'Guinness Nigeria Plc',
                    'website': 'https://www.guinness-nigeria.com',
                    'description': 'Premium beverage company with sophisticated distribution and logistics systems.'
                }
            ],
            'bronze': [
                {
                    'name': 'Airtel Nigeria',
                    'website': 'https://www.airtel.com.ng',
                    'description': 'Telecommunications company enabling digital solutions for transport and logistics.'
                },
                {
                    'name': 'Nigerian Aviation Handling Company (NAHCo)',
                    'website': 'https://www.nahco.com.ng',
                    'description': 'Leading ground handling and cargo services company in Nigeria\'s aviation sector.'
                },
                {
                    'name': 'SIFAX Group',
                    'website': 'https://www.sifaxgroup.com',
                    'description': 'Integrated logistics and maritime services company with operations across West Africa.'
                },
                {
                    'name': 'BUA Group',
                    'website': 'https://www.buagroup.com',
                    'description': 'Diversified conglomerate with significant investments in logistics and infrastructure.'
                },
                {
                    'name': 'Nigeria LNG Limited',
                    'website': 'https://www.nlng.com',
                    'description': 'Leading liquefied natural gas company with specialized transport and logistics operations.'
                },
                {
                    'name': 'Oando Plc',
                    'website': 'https://www.oandoplc.com',
                    'description': 'Energy solutions provider supporting Nigeria\'s transport and logistics sector.'
                },
                {
                    'name': 'Caverton Helicopters',
                    'website': 'https://www.cavertonhelicopters.com',
                    'description': 'Leading helicopter transportation company providing specialized logistics services.'
                },
                {
                    'name': 'Red Star Express',
                    'website': 'https://www.redstarexpress.com.ng',
                    'description': 'Premier courier and logistics company with nationwide coverage.'
                },
                {
                    'name': 'DHL Express Nigeria',
                    'website': 'https://www.dhl.com/ng-en',
                    'description': 'International express delivery and logistics company serving Nigeria.'
                },
                {
                    'name': 'FedEx Nigeria',
                    'website': 'https://www.fedex.com/ng',
                    'description': 'Global courier and logistics services company with operations in Nigeria.'
                },
                {
                    'name': 'UPS Nigeria',
                    'website': 'https://www.ups.com/ng',
                    'description': 'International package delivery and supply chain management company.'
                },
                {
                    'name': 'Agility Logistics',
                    'website': 'https://www.agility.com',
                    'description': 'Global logistics company providing integrated supply chain solutions in Nigeria.'
                },
                {
                    'name': 'Bollore Logistics Nigeria',
                    'website': 'https://www.bollore-logistics.com',
                    'description': 'International logistics company specializing in Africa operations.'
                },
                {
                    'name': 'Maersk Nigeria',
                    'website': 'https://www.maersk.com/ng',
                    'description': 'Global shipping and logistics company with significant presence in Nigeria.'
                },
                {
                    'name': 'CMA CGM Nigeria',
                    'website': 'https://www.cma-cgm.com',
                    'description': 'International shipping and logistics company serving Nigerian ports.'
                },
                {
                    'name': 'Hapag-Lloyd Nigeria',
                    'website': 'https://www.hapag-lloyd.com',
                    'description': 'Global container shipping company with operations in Nigerian ports.'
                },
                {
                    'name': 'Nigerian Railway Corporation',
                    'website': 'https://www.nrc.gov.ng',
                    'description': 'National railway operator driving rail transport development across Nigeria.'
                },
                {
                    'name': 'Lagos State Resident Registration Agency (LASRRA)',
                    'website': 'https://www.lagosresidents.gov.ng',
                    'description': 'State agency supporting citizen services and transport documentation.'
                },
                {
                    'name': 'Nigerian Ports Authority',
                    'website': 'https://www.nigerianports.gov.ng',
                    'description': 'Federal agency managing Nigeria\'s seaports and maritime logistics.'
                },
                {
                    'name': 'Federal Road Safety Corps (FRSC)',
                    'website': 'https://www.frsc.gov.ng',
                    'description': 'Federal agency ensuring road safety and transport regulation across Nigeria.'
                }
            ],
            'supporting': [
                {
                    'name': 'Transport Workers Union of Nigeria',
                    'website': 'https://www.transportworkersunion.org.ng',
                    'description': 'Labor union representing transport workers and advocating for industry development.'
                },
                {
                    'name': 'Nigerian Institute of Transport Technology',
                    'website': 'https://www.nitt.edu.ng',
                    'description': 'Premier institute for transport education and technology development in Nigeria.'
                },
                {
                    'name': 'Chartered Institute of Logistics and Transport (CILT) Nigeria',
                    'website': 'https://www.ciltnigeria.org',
                    'description': 'Professional body promoting excellence in logistics and transport in Nigeria.'
                },
                {
                    'name': 'Nigerian Shippers\' Council',
                    'website': 'https://www.shipperscouncil.gov.ng',
                    'description': 'Federal agency representing shippers\' interests and promoting efficient cargo movement.'
                },
                {
                    'name': 'Association of Maritime Truck Owners (AMATO)',
                    'website': 'https://www.amato-ng.org',
                    'description': 'Association representing truck owners in Nigeria\'s maritime logistics sector.'
                },
                {
                    'name': 'National Association of Road Transport Owners (NARTO)',
                    'website': 'https://www.narto.org.ng',
                    'description': 'Association of road transport operators promoting industry standards and development.'
                },
                {
                    'name': 'Lagos State Ministry of Transportation',
                    'website': 'https://www.lagosstate.gov.ng',
                    'description': 'State ministry overseeing transportation development and policy in Lagos State.'
                },
                {
                    'name': 'Nigerian Civil Aviation Authority (NCAA)',
                    'website': 'https://www.ncaa.gov.ng',
                    'description': 'Regulatory authority overseeing civil aviation and air transport in Nigeria.'
                },
                {
                    'name': 'Nigerian Maritime Administration and Safety Agency (NIMASA)',
                    'website': 'https://www.nimasa.gov.ng',
                    'description': 'Federal agency regulating maritime transport and ensuring safety standards.'
                },
                {
                    'name': 'Federal Ministry of Transportation',
                    'website': 'https://www.transportation.gov.ng',
                    'description': 'Federal ministry responsible for transportation policy and development in Nigeria.'
                }
            ]
        }

        # Create sponsors for each level
        total_created = 0
        total_existing = 0

        for level_name, sponsors_list in sponsors_data.items():
            try:
                sponsorship_level = SponsorshipLevel.objects.get(name=level_name)
                self.stdout.write(f'\nProcessing {level_name.title()} sponsors...')
                
                for sponsor_data in sponsors_list:
                    sponsor, created = Sponsor.objects.get_or_create(
                        name=sponsor_data['name'],
                        defaults={
                            'level': sponsorship_level,
                            'website': sponsor_data['website'],
                            'description': sponsor_data['description'],
                            'is_active': True
                        }
                    )
                    
                    if created:
                        self.stdout.write(f'  ✓ Created: {sponsor.name}')
                        total_created += 1
                    else:
                        self.stdout.write(f'  - Already exists: {sponsor.name}')
                        total_existing += 1
                        
            except SponsorshipLevel.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Sponsorship level "{level_name}" does not exist. Please run create_sample_data first.')
                )
                continue

        # Summary
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Sponsors data processing completed!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Summary:'))
        self.stdout.write(self.style.SUCCESS(f'   • New sponsors created: {total_created}'))
        self.stdout.write(self.style.SUCCESS(f'   • Existing sponsors: {total_existing}'))
        self.stdout.write(self.style.SUCCESS(f'   • Total sponsors: {total_created + total_existing}'))
        
        if total_created > 0:
            self.stdout.write(self.style.SUCCESS('\n💡 Note: You can upload sponsor logos through the Django admin panel.'))
            self.stdout.write(self.style.SUCCESS('   Admin URL: /admin/summit/sponsor/'))