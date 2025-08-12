from .models import SiteSettings

def site_settings(request):
    """Make site settings available globally in templates"""
    settings = SiteSettings.objects.first()
    return {
        'site_settings': settings
    }