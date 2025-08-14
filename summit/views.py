from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import logging
from .models import (
    SiteSettings, EventContent, Speaker, SponsorshipLevel, Sponsor,
    AwardCategory, Nomination, ExhibitionPackage, Exhibitor,
    AboutSectionContent, SummitOrganizer, ConferenceRegistration
)
from .forms import NominationForm, ConferenceRegistrationForm

# Get logger for this module
logger = logging.getLogger('summit')


def home(request):
    try:
        logger.info(f"Home page accessed from IP: {request.META.get('REMOTE_ADDR')}")
        
        site_settings = SiteSettings.objects.first()
        event_content = EventContent.objects.first()
        about_section_content = AboutSectionContent.objects.first()
        featured_speakers = Speaker.objects.all()  # Show all speakers on home page
        sponsors = Sponsor.objects.filter(is_active=True)
        summit_organizers = SummitOrganizer.objects.filter(is_active=True)
        
        context = {
            'site_settings': site_settings,
            'event_content': event_content,
            'about_section_content': about_section_content,
            'featured_speakers': featured_speakers,
            'sponsors': sponsors,
            'summit_organizers': summit_organizers,
        }
        
        logger.info(f"Home page loaded successfully with {featured_speakers.count()} speakers, {sponsors.count()} sponsors, {summit_organizers.count()} organizers")
        return render(request, 'summit/home.html', context)
        
    except Exception as e:
        logger.error(f"Error loading home page: {str(e)}", exc_info=True)
        raise


def speakers(request):
    speakers_list = Speaker.objects.all()
    context = {
        'speakers': speakers_list,
    }
    return render(request, 'summit/speakers.html', context)


def sponsorship(request):
    sponsorship_levels = SponsorshipLevel.objects.all()
    exhibition_packages = ExhibitionPackage.objects.all()
    context = {
        'sponsorship_levels': sponsorship_levels,
        'exhibition_packages': exhibition_packages,
    }
    return render(request, 'summit/sponsorship.html', context)


def nominations(request):
    try:
        logger.info(f"Nominations page accessed from IP: {request.META.get('REMOTE_ADDR')}")
        categories = AwardCategory.objects.filter(is_active=True)
        
        if request.method == 'POST':
            logger.info(f"Nomination form submitted from IP: {request.META.get('REMOTE_ADDR')}")
            form = NominationForm(request.POST, request.FILES)
            if form.is_valid():
                nomination = form.save()
                logger.info(f"New nomination submitted: {nomination.nominee_name} for {nomination.category.name} by {nomination.nominator_email}")
                messages.success(request, 'Your nomination has been submitted successfully!')
                return redirect('nominations')
            else:
                logger.warning(f"Invalid nomination form submission from {request.META.get('REMOTE_ADDR')}: {form.errors}")
        else:
            form = NominationForm()
        
        context = {
            'categories': categories,
            'form': form,
        }
        return render(request, 'summit/nominations.html', context)
        
    except Exception as e:
        logger.error(f"Error in nominations view: {str(e)}", exc_info=True)
        raise


def nomination_success(request):
    return render(request, 'summit/nomination_success.html')


def registration(request):
    try:
        logger.info(f"Registration page accessed from IP: {request.META.get('REMOTE_ADDR')}")
        
        if request.method == 'POST':
            logger.info(f"Registration form submitted from IP: {request.META.get('REMOTE_ADDR')}")
            form = ConferenceRegistrationForm(request.POST)
            if form.is_valid():
                registration = form.save()
                logger.info(f"New registration: {registration.first_name} {registration.last_name} ({registration.email}) - {registration.ticket_type}")
                messages.success(request, 'Your registration has been submitted successfully! We will contact you with further details.')
                return redirect('registration_success')
            else:
                logger.warning(f"Invalid registration form submission from {request.META.get('REMOTE_ADDR')}: {form.errors}")
        else:
            form = ConferenceRegistrationForm()
        
        context = {
            'form': form,
        }
        return render(request, 'summit/registration.html', context)
        
    except Exception as e:
        logger.error(f"Error in registration view: {str(e)}", exc_info=True)
        raise


def registration_success(request):
    return render(request, 'summit/registration_success.html')
