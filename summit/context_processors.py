from .models import SiteSettings


def site_settings(request):
    """Make site settings available globally in templates"""
    return {'site_settings': SiteSettings.get_solo()}
