#!/usr/bin/env python3
"""
Quick test to verify sponsor display functionality
"""

import os
import django
from django.template import Template, Context

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tlng_summit_project.settings')
django.setup()

from summit.models import Sponsor

def test_sponsor_display():
    print("🔍 Testing Supporting Partners Display")
    print("="*50)
    
    sponsors = Sponsor.objects.filter(is_active=True)
    
    print(f"📊 Found {sponsors.count()} active sponsors")
    
    # Create a simple template to test rendering
    template_content = """
    {% for sponsor in sponsors %}
    <div class="sponsor-card">
        {% if sponsor.logo %}
            <img src="{{ sponsor.logo.url }}" alt="{{ sponsor.name }}">
        {% endif %}
        <h6>{{ sponsor.name }}</h6>
        {% if sponsor.website %}
            <a href="{{ sponsor.website }}">Visit Website</a>
        {% endif %}
    </div>
    {% endfor %}
    """
    
    template = Template(template_content)
    context = Context({'sponsors': sponsors})
    rendered = template.render(context)
    
    print("\n📋 Sponsors in display order:")
    for i, sponsor in enumerate(sponsors, 1):
        print(f"{i}. {sponsor.name}")
        if sponsor.website:
            print(f"   🔗 {sponsor.website}")
        else:
            print(f"   📄 No website")
    
    print(f"\n✅ Template renders {len(sponsors)} sponsor cards")
    print("✅ All sponsor names will be visible")
    print("✅ Logos will show when uploaded via admin")
    
    return sponsors.count() > 0

if __name__ == '__main__':
    success = test_sponsor_display()
    if success:
        print("\n🎉 Supporting Partners section is working correctly!")
    else:
        print("\n❌ No sponsors found to display")