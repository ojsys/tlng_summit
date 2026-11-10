from django import forms
from django.core.exceptions import ValidationError

from .models import (
    AwardCategory, ConferenceRegistration, GalleryAlbum, Nomination, TicketType,
)

MAX_UPLOAD_MB = 10


class HoneypotMixin(forms.Form):
    """Invisible field that real visitors leave empty; bots tend to fill it in."""
    website = forms.CharField(required=False, label='Leave this field empty',
                              widget=forms.TextInput(attrs={'autocomplete': 'off', 'tabindex': '-1'}))

    def clean_website(self):
        if self.cleaned_data.get('website'):
            raise ValidationError('Spam detected.')
        return ''


class NominationForm(HoneypotMixin, forms.ModelForm):
    class Meta:
        model = Nomination
        fields = [
            'category', 'nominee_name', 'nominee_company',
            'nominator_name', 'nominator_email', 'nominator_phone',
            'nomination_reason', 'supporting_documents'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'nominee_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Full name of nominee', 'required': True}),
            'nominee_company': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Company/Organization name (optional)'}),
            'nominator_name': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': 'Your full name', 'required': True}),
            'nominator_email': forms.EmailInput(attrs={
                'class': 'form-control', 'placeholder': 'your.email@example.com', 'required': True}),
            'nominator_phone': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '+234 xxx xxx xxxx'}),
            'nomination_reason': forms.Textarea(attrs={
                'class': 'form-control', 'rows': 5, 'required': True,
                'placeholder': 'Please explain why this person/organization deserves this award...'}),
            'supporting_documents': forms.FileInput(attrs={
                'class': 'form-control', 'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = AwardCategory.objects.filter(is_active=True)
        self.fields['category'].empty_label = "Select an award category"

    def clean_supporting_documents(self):
        f = self.cleaned_data.get('supporting_documents')
        if f and f.size > MAX_UPLOAD_MB * 1024 * 1024:
            raise ValidationError(f'File is too large. The maximum size is {MAX_UPLOAD_MB} MB.')
        return f


class TicketChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class ConferenceRegistrationForm(HoneypotMixin, forms.ModelForm):
    ticket = TicketChoiceField(queryset=TicketType.objects.none(), widget=forms.RadioSelect,
                               empty_label=None, error_messages={'required': 'Please choose a ticket.'})

    class Meta:
        model = ConferenceRegistration
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'company', 'job_title',
            'attendee_type', 'ticket', 'dietary_requirements', 'special_needs',
            'how_did_you_hear'
        ]
        labels = {
            'email': 'Email address',
            'phone': 'Phone number',
            'company': 'Company / organisation',
            'how_did_you_hear': 'How did you hear about us?',
        }
        help_texts = {'how_did_you_hear': '', 'dietary_requirements': '', 'special_needs': ''}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'autocomplete': 'given-name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'autocomplete': 'family-name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your.email@example.com', 'autocomplete': 'email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+234 xxx xxx xxxx', 'autocomplete': 'tel'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company/Organization (optional)', 'autocomplete': 'organization'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Job Title (optional)', 'autocomplete': 'organization-title'}),
            'attendee_type': forms.Select(attrs={'class': 'form-select'}),
            'dietary_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Any dietary requirements or allergies (optional)'}),
            'special_needs': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Any accessibility requirements (optional)'}),
            'how_did_you_hear': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. LinkedIn, a colleague, email (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available = [t.pk for t in TicketType.objects.filter(is_active=True) if not t.is_sold_out]
        self.fields['ticket'].queryset = TicketType.objects.filter(pk__in=available)
        if len(available) == 1 and not self.is_bound:
            self.initial['ticket'] = available[0]

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if ConferenceRegistration.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                'This email address is already registered. If you need to change your '
                'registration, please contact us.')
        return email


# ---------------------------------------------------------------- admin forms

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput(attrs={'accept': 'image/*', 'multiple': True}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single = super().clean
        if isinstance(data, (list, tuple)):
            return [single(d, initial) for d in data]
        return [single(data, initial)] if data else []


class GalleryAlbumAdminForm(forms.ModelForm):
    bulk_photos = MultipleImageField(
        required=False, label='Upload photos',
        help_text='Select as many photos as you like (hold Ctrl/Cmd or Shift to pick several). '
                  'They are resized automatically.')

    class Meta:
        model = GalleryAlbum
        fields = '__all__'
