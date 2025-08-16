from django.contrib import admin
from .models import (
    SiteSettings, EventContent, Speaker, SponsorshipLevel, Sponsor,
    AwardCategory, Nomination, ExhibitionPackage, Exhibitor,
    AboutSectionContent, SummitOrganizer, ConferenceRegistration
)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'updated_at')
    fieldsets = (
        ('Site Information', {
            'fields': ('site_name', 'favicon')
        }),
        ('Organizer Logos', {
            'fields': ('primary_organizer_logo', 'site_logo'),
            'description': 'Primary organizer logo appears first, summit logo appears second in navigation'
        }),
        ('Hero Section', {
            'fields': ('hero_background_image',)
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Social Media', {
            'fields': ('social_facebook', 'social_twitter', 'social_linkedin', 'social_instagram')
        }),
    )
    
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(EventContent)
class EventContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'venue', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'event_date', 'venue', 'hero_badge_text')
        }),
        ('Hero Statistics', {
            'fields': (
                ('stat_1_number', 'stat_1_label'),
                ('stat_2_number', 'stat_2_label'),
                ('stat_3_number', 'stat_3_label'),
                ('stat_4_number', 'stat_4_label'),
            )
        }),
        ('About Section', {
            'fields': ('about_title', 'about_text')
        }),
        ('About Features', {
            'fields': (
                ('feature_1_title', 'feature_1_description'),
                ('feature_2_title', 'feature_2_description'),
                ('feature_3_title', 'feature_3_description'),
            )
        }),
    )
    
    def has_add_permission(self, request):
        return not EventContent.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'company', 'is_featured', 'order')
    list_filter = ('is_featured', 'company')
    search_fields = ('name', 'title', 'company')
    ordering = ('order', 'name')
    fields = (
        'name', 'title', 'company', 'bio', 'photo',
        'linkedin_url', 'twitter_url', 'is_featured', 'order'
    )


@admin.register(SponsorshipLevel)
class SponsorshipLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'max_sponsors', 'order')
    ordering = ('order',)


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'has_logo', 'is_active', 'created_at')
    list_filter = ('level', 'is_active')
    search_fields = ('name', 'website')
    ordering = ('level__order', 'name')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'level', 'logo', 'website')
        }),
        ('Details', {
            'fields': ('description', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def has_logo(self, obj):
        return bool(obj.logo)
    has_logo.boolean = True
    has_logo.short_description = 'Logo Uploaded'


@admin.register(AwardCategory)
class AwardCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('order', 'name')
    fields = ('name', 'description', 'criteria', 'is_active', 'order')


@admin.register(Nomination)
class NominationAdmin(admin.ModelAdmin):
    list_display = ('nominee_name', 'category', 'nominator_name', 'submitted_at', 'is_reviewed', 'is_approved')
    list_filter = ('category', 'is_reviewed', 'is_approved', 'submitted_at')
    search_fields = ('nominee_name', 'nominator_name', 'nominee_company')
    readonly_fields = ('submitted_at',)
    fieldsets = (
        ('Nominee Information', {
            'fields': ('category', 'nominee_name', 'nominee_company')
        }),
        ('Nominator Information', {
            'fields': ('nominator_name', 'nominator_email', 'nominator_phone')
        }),
        ('Nomination Details', {
            'fields': ('nomination_reason', 'supporting_documents', 'submitted_at')
        }),
        ('Review Status', {
            'fields': ('is_reviewed', 'is_approved')
        }),
    )


@admin.register(ExhibitionPackage)
class ExhibitionPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'space_size', 'max_exhibitors', 'order')
    ordering = ('order',)


@admin.register(AboutSectionContent)
class AboutSectionContentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'updated_at')
    fields = ('about_image', 'image_alt_text')
    
    def has_add_permission(self, request):
        return not AboutSectionContent.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SummitOrganizer)
class SummitOrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('order', 'name')
    fields = ('name', 'logo', 'website', 'description', 'order', 'is_active')


@admin.register(ConferenceRegistration)
class ConferenceRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'company', 'ticket_type', 'payment_status', 'registration_date')
    list_filter = ('attendee_type', 'ticket_type', 'payment_status', 'is_confirmed')
    search_fields = ('first_name', 'last_name', 'email', 'company')
    readonly_fields = ('registration_date',)
    ordering = ('-registration_date',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Professional Information', {
            'fields': ('company', 'job_title', 'attendee_type')
        }),
        ('Registration Details', {
            'fields': ('ticket_type', 'dietary_requirements', 'special_needs', 'how_did_you_hear')
        }),
        ('Status', {
            'fields': ('is_confirmed', 'payment_status', 'registration_date')
        }),
    )
    
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'


@admin.register(Exhibitor)
class ExhibitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'package', 'contact_person', 'is_approved', 'created_at')
    list_filter = ('package', 'is_approved')
    search_fields = ('name', 'contact_person')
    fieldsets = (
        ('Company Information', {
            'fields': ('name', 'package', 'company_description', 'logo', 'website')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_email', 'contact_phone')
        }),
        ('Approval Status', {
            'fields': ('is_approved',)
        }),
    )
