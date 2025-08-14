from django import forms
from .models import Nomination, AwardCategory, ConferenceRegistration


class NominationForm(forms.ModelForm):
    class Meta:
        model = Nomination
        fields = [
            'category', 'nominee_name', 'nominee_company',
            'nominator_name', 'nominator_email', 'nominator_phone',
            'nomination_reason', 'supporting_documents'
        ]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'nominee_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full name of nominee',
                'required': True
            }),
            'nominee_company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company/Organization name (optional)'
            }),
            'nominator_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your full name',
                'required': True
            }),
            'nominator_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'nominator_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+234 xxx xxx xxxx'
            }),
            'nomination_reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Please explain why this person/organization deserves this award...',
                'required': True
            }),
            'supporting_documents': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = AwardCategory.objects.filter(is_active=True)
        self.fields['category'].empty_label = "Select an award category"


class ConferenceRegistrationForm(forms.ModelForm):
    class Meta:
        model = ConferenceRegistration
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'company', 'job_title',
            'attendee_type', 'ticket_type', 'dietary_requirements', 'special_needs',
            'how_did_you_hear'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required': True
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+234 xxx xxx xxxx',
                'required': True
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company/Organization (optional)'
            }),
            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Job Title (optional)'
            }),
            'attendee_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'ticket_type': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'dietary_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any dietary requirements or allergies (optional)'
            }),
            'special_needs': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any accessibility requirements (optional)'
            }),
            'how_did_you_hear': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'How did you hear about this event? (optional)'
            })
        }