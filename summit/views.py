from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    SiteSettings, EventContent, Speaker, SponsorshipLevel, Sponsor,
    AwardCategory, Nomination, ExhibitionPackage, Exhibitor
)
from .forms import NominationForm


def home(request):
    site_settings = SiteSettings.objects.first()
    event_content = EventContent.objects.first()
    featured_speakers = Speaker.objects.filter(is_featured=True)[:6]
    sponsors = Sponsor.objects.filter(is_active=True)
    
    context = {
        'site_settings': site_settings,
        'event_content': event_content,
        'featured_speakers': featured_speakers,
        'sponsors': sponsors,
    }
    return render(request, 'summit/home.html', context)


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
    categories = AwardCategory.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = NominationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your nomination has been submitted successfully!')
            return redirect('nominations')
    else:
        form = NominationForm()
    
    context = {
        'categories': categories,
        'form': form,
    }
    return render(request, 'summit/nominations.html', context)


def nomination_success(request):
    return render(request, 'summit/nomination_success.html')
