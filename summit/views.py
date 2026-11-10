import logging
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from .forms import ConferenceRegistrationForm, NominationForm
from .models import (
    AboutSectionContent, AwardCategory, ConferenceRegistration, EventContent,
    ExhibitionPackage, GalleryAlbum, GalleryPhoto, Highlight, SiteSettings,
    Speaker, Sponsor, SponsorshipLevel, SummitOrganizer, TicketType,
)

logger = logging.getLogger('summit')


def _client_ip(request):
    return request.META.get('REMOTE_ADDR')


def home(request):
    highlights = Highlight.objects.filter(is_active=True)
    public_photos = GalleryPhoto.objects.filter(album__is_published=True)
    gallery_photos = list(public_photos.select_related('album')
                          .order_by('-album__year', 'album__order', 'order', 'id')[:7])
    context = {
        'event_content': EventContent.get_solo(),
        'about_section_content': AboutSectionContent.get_solo(),
        'topics': [h for h in highlights if h.section == 'topics'],
        'why_attend': [h for h in highlights if h.section == 'why_attend'],
        'featured_speakers': Speaker.objects.all(),
        'sponsors': Sponsor.objects.filter(is_active=True).select_related('level'),
        'summit_organizers': SummitOrganizer.objects.filter(is_active=True),
        'gallery_photos': gallery_photos,
        'gallery_total': public_photos.count() if gallery_photos else 0,
    }
    return render(request, 'summit/home.html', context)


def speakers(request):
    return render(request, 'summit/speakers.html', {'speakers': Speaker.objects.all()})


def sponsorship(request):
    context = {
        'sponsorship_levels': SponsorshipLevel.objects.all(),
        'exhibition_packages': ExhibitionPackage.objects.all(),
        'partner_benefits': Highlight.objects.filter(section='partner_benefits', is_active=True),
    }
    return render(request, 'summit/sponsorship.html', context)


def nominations(request):
    categories = AwardCategory.objects.filter(is_active=True)
    if request.method == 'POST':
        form = NominationForm(request.POST, request.FILES)
        if form.is_valid():
            nomination = form.save()
            logger.info('New nomination: %s for %s by %s', nomination.nominee_name,
                        nomination.category.name, nomination.nominator_email)
            return redirect('nomination_success')
        logger.warning('Invalid nomination form from %s: %s', _client_ip(request), form.errors.as_json())
    else:
        form = NominationForm()
    return render(request, 'summit/nominations.html', {'categories': categories, 'form': form})


def nomination_success(request):
    return render(request, 'summit/nomination_success.html')


# ------------------------------------------------------------------ gallery

def _visible_albums(request):
    albums = GalleryAlbum.objects.annotate(photo_count=Count('photos'))
    if not request.user.is_staff:
        albums = albums.filter(is_published=True)
    return albums


def gallery(request):
    albums = [a for a in _visible_albums(request) if a.photo_count or request.user.is_staff]
    photos = (GalleryPhoto.objects.filter(album__in=[a.pk for a in albums])
              .select_related('album')
              .order_by('-album__year', 'album__order', '-album__event_date', 'album_id', 'order', 'id'))
    context = {
        'albums': albums,
        'photos': photos,
        'years': sorted({a.year for a in albums}, reverse=True),
    }
    return render(request, 'summit/gallery.html', context)


def gallery_album(request, slug):
    album = get_object_or_404(_visible_albums(request), slug=slug)
    photos = album.photos.all()
    others = (_visible_albums(request).exclude(pk=album.pk)
              .filter(photo_count__gt=0).prefetch_related('photos')[:3])
    return render(request, 'summit/gallery_album.html',
                  {'album': album, 'photos': photos, 'other_albums': others})


# ------------------------------------------------------------- registration

def _send_registration_emails(request, registration):
    site = SiteSettings.get_solo()
    ctx = {'registration': registration, 'site_settings': site,
           'event_content': EventContent.get_solo(),
           'site_url': request.build_absolute_uri('/')}
    if site.send_confirmation_emails:
        try:
            send_mail(
                subject=f'Your registration is confirmed: {registration.reference}',
                message=render_to_string('summit/emails/registration_confirmation.txt', ctx),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[registration.email],
            )
        except Exception:
            logger.error('Could not send confirmation email to %s', registration.email, exc_info=True)
    if site.registration_notify_contact:
        try:
            send_mail(
                subject=f'New registration: {registration.full_name} ({registration.ticket})',
                message=render_to_string('summit/emails/registration_notification.txt', ctx),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[site.registration_notify_contact],
            )
        except Exception:
            logger.error('Could not send registration notification', exc_info=True)


def registration(request):
    site = SiteSettings.get_solo()
    tickets = TicketType.objects.filter(is_active=True)
    has_tickets = any(not t.is_sold_out for t in tickets)

    if not site.registration_open or not has_tickets:
        return render(request, 'summit/registration.html',
                      {'closed': True, 'sold_out': site.registration_open and not has_tickets})

    if request.method == 'POST':
        form = ConferenceRegistrationForm(request.POST)
        if form.is_valid():
            reg = form.save()
            logger.info('New registration %s: %s (%s) - %s', reg.reference, reg.full_name, reg.email, reg.ticket)
            _send_registration_emails(request, reg)
            request.session['registration_id'] = reg.pk
            return redirect('registration_success')
        logger.warning('Invalid registration form from %s: %s', _client_ip(request), form.errors.as_json())
    else:
        form = ConferenceRegistrationForm()
    return render(request, 'summit/registration.html',
                  {'form': form, 'tickets': tickets, 'event_content': EventContent.get_solo()})


def registration_success(request):
    reg = None
    reg_id = request.session.get('registration_id')
    if reg_id:
        reg = ConferenceRegistration.objects.select_related('ticket').filter(pk=reg_id).first()
    return render(request, 'summit/registration_success.html',
                  {'registration': reg, 'event_content': EventContent.get_solo()})
