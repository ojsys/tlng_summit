"""Custom admin site: groups models into CMS-style sections and adds a dashboard."""
from django.contrib import admin
from django.contrib.admin.apps import AdminConfig
from django.db.models import Count
from django.utils import timezone

# (section title, [model labels in display order])
SECTIONS = [
    ('Website Content', ['summit.sitesettings', 'summit.eventcontent', 'summit.contentblock',
                         'summit.highlight', 'summit.aboutsectioncontent']),
    ('Gallery', ['summit.galleryalbum', 'summit.galleryphoto']),
    ('Registration', ['summit.conferenceregistration', 'summit.tickettype']),
    ('Awards & Nominations', ['summit.nomination', 'summit.awardcategory']),
    ('Speakers & Partners', ['summit.speaker', 'summit.summitorganizer', 'summit.sponsor',
                             'summit.sponsorshiplevel', 'summit.exhibitionpackage', 'summit.exhibitor']),
    ('Users & Permissions', ['auth.user', 'auth.group']),
]


class SummitAdminSite(admin.AdminSite):
    site_header = 'TLNG Summit · Content Manager'
    site_title = 'TLNG Summit CMS'
    index_title = 'Dashboard'

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        if app_label:
            return app_list
        models = {}
        for app in app_list:
            for m in app['models']:
                models[f"{app['app_label']}.{m['object_name'].lower()}"] = m
        grouped = []
        for title, labels in SECTIONS:
            section_models = [models.pop(label) for label in labels if label in models]
            if section_models:
                grouped.append({'name': title, 'app_label': title.lower().replace(' ', '_'),
                                'app_url': '', 'has_module_perms': True, 'models': section_models})
        if models:  # anything not explicitly grouped
            grouped.append({'name': 'Other', 'app_label': 'other', 'app_url': '',
                            'has_module_perms': True, 'models': list(models.values())})
        return grouped

    def index(self, request, extra_context=None):
        from .models import (ConferenceRegistration, GalleryAlbum, GalleryPhoto,
                             Nomination, SiteSettings, TicketType)
        today = timezone.now()
        week_ago = today - timezone.timedelta(days=7)
        regs = ConferenceRegistration.objects
        extra_context = {
            **(extra_context or {}),
            'stats': {
                'registrations': regs.count(),
                'registrations_week': regs.filter(registration_date__gte=week_ago).count(),
                'nominations': Nomination.objects.count(),
                'nominations_pending': Nomination.objects.filter(is_reviewed=False).count(),
                'albums': GalleryAlbum.objects.count(),
                'photos': GalleryPhoto.objects.count(),
            },
            'tickets': TicketType.objects.filter(is_active=True).annotate(n=Count('registrations')),
            'recent_registrations': regs.select_related('ticket')[:5],
            'registration_open': SiteSettings.get_solo().registration_open,
        }
        return super().index(request, extra_context)


class SummitAdminConfig(AdminConfig):
    default_site = 'summit.admin_site.SummitAdminSite'
