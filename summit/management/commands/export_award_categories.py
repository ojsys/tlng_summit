import json
from django.core.management.base import BaseCommand
from summit.models import AwardCategory


class Command(BaseCommand):
    help = 'Export award categories to JSON file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='award_categories_backup.json',
            help='Output file name (default: award_categories_backup.json)'
        )

    def handle(self, *args, **options):
        categories = AwardCategory.objects.all().order_by('order')
        
        categories_data = []
        for category in categories:
            categories_data.append({
                'name': category.name,
                'description': category.description,
                'criteria': category.criteria,
                'order': category.order,
                'is_active': category.is_active
            })
        
        output_file = options['output']
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(categories_data, f, indent=2, ensure_ascii=False)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully exported {len(categories_data)} categories to {output_file}')
        )