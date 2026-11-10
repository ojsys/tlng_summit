import csv

from django.contrib import admin, messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from .forms import GalleryAlbumAdminForm
from .models import (
    AboutSectionContent, AwardCategory, ConferenceRegistration, ContentBlock,
    EventContent, ExhibitionPackage, Exhibitor, GalleryAlbum, GalleryPhoto,
    Highlight, Nomination, SiteSettings, Speaker, Sponsor, SponsorshipLevel,
    SummitOrganizer, TicketType,
)


# ------------------------------------------------------------------ helpers

def thumb(image, height=60, rounded=False):
    if not image:
        return format_html('<span style="color:#999">—</span>')
    return format_html(
        '<img src="{}" style="height:{}px;max-width:{}px;object-fit:cover;border-radius:{};'
        'box-shadow:0 1px 3px rgba(0,0,0,.2)">',
        image.url, height, height * 2, '50%' if rounded else '6px')


def image_preview_field(field_name, height=160):
    def preview(self, obj):
        return thumb(getattr(obj, field_name, None), height) if obj else '—'
    preview.short_description = 'Current image'
    return preview


def export_csv(filename, columns):
    """Build an admin action that downloads the selected rows as CSV."""
    def action(modeladmin, request, queryset):
        response = HttpResponse(content_type='text/csv')
        stamp = timezone.now().strftime('%Y%m%d-%H%M')
        response['Content-Disposition'] = f'attachment; filename="{filename}-{stamp}.csv"'
        writer = csv.writer(response)
        writer.writerow([header for header, _ in columns])
        for obj in queryset:
            writer.writerow([getter(obj) for _, getter in columns])
        return response
    action.short_description = 'Export selected to CSV (Excel)'
    return action


class SingletonAdmin(admin.ModelAdmin):
    """Skip the one-row list page and go straight to the edit form."""

    def changelist_view(self, request, extra_context=None):
        obj = self.model.get_solo()
        return HttpResponseRedirect(
            reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.pk]))

    def has_add_permission(self, request):
        return not self.model.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):
        if '_continue' not in request.POST and '_addanother' not in request.POST:
            self.message_user(request, 'Changes saved. They are live on the site now.', messages.SUCCESS)
            return HttpResponseRedirect(request.path)
        return super().response_change(request, obj)


# ---------------------------------------------------------- website content

@admin.register(SiteSettings)
class SiteSettingsAdmin(SingletonAdmin):
    readonly_fields = ('logo_preview', 'organizer_logo_preview', 'hero_preview')
    logo_preview = image_preview_field('site_logo', 80)
    organizer_logo_preview = image_preview_field('primary_organizer_logo', 80)
    hero_preview = image_preview_field('hero_background_image', 160)
    fieldsets = (
        ('Site Information', {'fields': ('site_name', 'favicon')}),
        ('Logos', {
            'fields': ('primary_organizer_logo', 'organizer_logo_preview', 'site_logo', 'logo_preview'),
            'description': 'The organizer logo appears first in the navigation bar, the summit logo second.'
        }),
        ('Home Page Hero', {'fields': ('hero_background_image', 'hero_preview')}),
        ('Registration', {
            'fields': ('registration_open', 'send_confirmation_emails', 'registration_notify_email'),
            'description': 'Ticket options and prices are managed under Registration › Ticket Types.'
        }),
        ('Contact Information', {'fields': ('contact_email', 'contact_phone', 'contact_address')}),
        ('Enquiry Emails', {
            'fields': ('sponsorship_email', 'exhibition_email', 'speakers_email', 'awards_email'),
            'description': 'Leave blank to use the main contact email.'
        }),
        ('Social Media', {'fields': ('social_facebook', 'social_twitter', 'social_linkedin', 'social_instagram')}),
    )


@admin.register(EventContent)
class EventContentAdmin(SingletonAdmin):
    fieldsets = (
        ('Event Details', {'fields': ('title', 'subtitle', 'event_date', 'venue', 'hero_badge_text')}),
        ('Hero Statistics', {
            'fields': (('stat_1_number', 'stat_1_label'), ('stat_2_number', 'stat_2_label'),
                       ('stat_3_number', 'stat_3_label'), ('stat_4_number', 'stat_4_label')),
        }),
        ('About Section', {'fields': ('about_title', 'about_text')}),
        ('About Features', {
            'fields': (('feature_1_title', 'feature_1_description'),
                       ('feature_2_title', 'feature_2_description'),
                       ('feature_3_title', 'feature_3_description')),
        }),
    )


@admin.register(AboutSectionContent)
class AboutSectionContentAdmin(SingletonAdmin):
    readonly_fields = ('preview',)
    preview = image_preview_field('about_image', 200)
    fields = ('about_image', 'preview', 'image_alt_text')


PAGE_NAMES = {
    'home': 'Home page', 'site': 'Header & footer', 'speakers': 'Speakers page',
    'sponsorship': 'Sponsorship page', 'nominations': 'Nominations page',
    'registration': 'Registration page', 'gallery': 'Gallery page',
}


class PageFilter(admin.SimpleListFilter):
    title = 'page'
    parameter_name = 'page'

    def lookups(self, request, model_admin):
        pages = ContentBlock.objects.values_list('page', flat=True).distinct()
        return [(p, PAGE_NAMES.get(p, p.title())) for p in pages]

    def queryset(self, request, queryset):
        return queryset.filter(page=self.value()) if self.value() else queryset


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ('label', 'page_name', 'short_value', 'updated_at')
    list_filter = (PageFilter,)
    search_fields = ('key', 'value')
    readonly_fields = ('key', 'page_name')
    fields = ('page_name', 'key', 'value')
    list_per_page = 100

    def changelist_view(self, request, extra_context=None):
        extra_context = {**(extra_context or {}), 'title': 'Text blocks: all site copy, by page'}
        if request.method == 'GET' and not request.GET:
            self.message_user(
                request, 'Tip: the quickest way to edit text is on the site itself. Open any page, '
                'click "Edit page" in the toolbar at the bottom, then click the text you want to change.',
                messages.INFO)
        return super().changelist_view(request, extra_context)

    def has_add_permission(self, request):
        return False  # blocks are created automatically by the templates

    @admin.display(description='Page', ordering='page')
    def page_name(self, obj):
        return PAGE_NAMES.get(obj.page, obj.page.title())

    @admin.display(description='Text')
    def short_value(self, obj):
        return (obj.value[:90] + '…') if len(obj.value) > 90 else obj.value


@admin.register(Highlight)
class HighlightAdmin(admin.ModelAdmin):
    list_display = ('icon_preview', 'title', 'section', 'order', 'is_active')
    list_display_links = ('icon_preview', 'title')
    list_editable = ('order', 'is_active')
    list_filter = ('section', 'is_active')
    search_fields = ('title', 'description')
    fields = ('section', 'icon', 'title', 'description', 'order', 'is_active')

    @admin.display(description='Icon')
    def icon_preview(self, obj):
        return format_html('<i class="fas {}" style="font-size:20px;color:#008751"></i>', obj.icon)

    class Media:
        css = {'all': ('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css',)}


# ------------------------------------------------------------------ gallery

class GalleryPhotoInline(admin.TabularInline):
    model = GalleryPhoto
    extra = 0
    fields = ('preview', 'image', 'caption', 'order')
    readonly_fields = ('preview',)
    ordering = ('order', 'id')

    @admin.display(description='Preview')
    def preview(self, obj):
        return thumb(obj.thumbnail or obj.image, 70) if obj.pk else ''


@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    form = GalleryAlbumAdminForm
    inlines = [GalleryPhotoInline]
    list_display = ('cover_preview', 'title', 'year', 'photo_count', 'is_published', 'order', 'view_link')
    list_display_links = ('cover_preview', 'title')
    list_editable = ('is_published', 'order')
    list_filter = ('year', 'is_published')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {'fields': ('title', 'year', 'event_date', 'location', 'description')}),
        ('Add Photos', {'fields': ('bulk_photos',),
                        'description': 'You can also add photos straight from the album page on the '
                                       'site while in Edit mode.'}),
        ('Display', {'fields': ('cover_image', 'is_published', 'order', 'slug')}),
    )

    @admin.display(description='Cover')
    def cover_preview(self, obj):
        url = obj.cover
        return format_html('<img src="{}" style="height:50px;width:80px;object-fit:cover;border-radius:6px">', url) if url else '—'

    @admin.display(description='Photos')
    def photo_count(self, obj):
        return obj.photos.count()

    @admin.display(description='')
    def view_link(self, obj):
        return format_html('<a href="{}" target="_blank">View on site ↗</a>', obj.get_absolute_url())

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        files = form.cleaned_data.get('bulk_photos') or []
        if files:
            album = form.instance
            start = album.photos.count()
            for i, f in enumerate(files, start=1):
                GalleryPhoto.objects.create(album=album, image=f, order=start + i)
            self.message_user(request, f'{len(files)} photo(s) added to “{album}”.', messages.SUCCESS)


@admin.register(GalleryPhoto)
class GalleryPhotoAdmin(admin.ModelAdmin):
    list_display = ('preview', 'caption', 'album', 'order', 'uploaded_at')
    list_display_links = ('preview',)
    list_editable = ('caption', 'order')
    list_filter = ('album',)
    search_fields = ('caption', 'album__title')
    fields = ('album', 'image', 'large_preview', 'caption', 'order')
    readonly_fields = ('large_preview',)
    list_per_page = 50

    @admin.display(description='Photo')
    def preview(self, obj):
        return thumb(obj.thumbnail or obj.image, 60)

    large_preview = image_preview_field('image', 240)


# ------------------------------------------------------------- registration

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'capacity', 'registered', 'spots_left_display', 'is_active', 'order')
    list_editable = ('price', 'is_active', 'order')
    prepopulated_fields = {'code': ('name',)}
    fields = ('name', 'code', 'price', 'description', 'capacity', 'is_active', 'order')

    @admin.display(description='Registered')
    def registered(self, obj):
        return obj.registrations.count()

    @admin.display(description='Spots left')
    def spots_left_display(self, obj):
        left = obj.spots_left
        return 'Unlimited' if left is None else left

    def has_delete_permission(self, request, obj=None):
        if obj and obj.registrations.exists():
            return False  # deactivate instead, so existing registrations keep their ticket
        return super().has_delete_permission(request, obj)


@admin.register(ConferenceRegistration)
class ConferenceRegistrationAdmin(admin.ModelAdmin):
    list_display = ('reference', 'full_name', 'email', 'phone', 'company', 'ticket',
                    'payment_status', 'is_confirmed', 'registration_date')
    list_display_links = ('reference', 'full_name')
    list_filter = ('ticket', 'attendee_type', 'payment_status', 'is_confirmed', 'registration_date')
    search_fields = ('reference', 'first_name', 'last_name', 'email', 'company', 'phone')
    readonly_fields = ('reference', 'registration_date')
    date_hierarchy = 'registration_date'
    list_per_page = 50
    actions = [
        'mark_confirmed', 'mark_paid',
        export_csv('registrations', [
            ('Reference', lambda r: r.reference), ('First name', lambda r: r.first_name),
            ('Last name', lambda r: r.last_name), ('Email', lambda r: r.email),
            ('Phone', lambda r: r.phone), ('Company', lambda r: r.company),
            ('Job title', lambda r: r.job_title), ('Attendee type', lambda r: r.get_attendee_type_display()),
            ('Ticket', lambda r: r.ticket), ('Payment', lambda r: r.get_payment_status_display()),
            ('Confirmed', lambda r: 'Yes' if r.is_confirmed else 'No'),
            ('Dietary', lambda r: r.dietary_requirements), ('Accessibility', lambda r: r.special_needs),
            ('Heard via', lambda r: r.how_did_you_hear),
            ('Registered', lambda r: timezone.localtime(r.registration_date).strftime('%Y-%m-%d %H:%M')),
        ]),
    ]
    fieldsets = (
        ('Registration', {'fields': ('reference', 'registration_date', 'ticket')}),
        ('Personal Information', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Professional Information', {'fields': ('company', 'job_title', 'attendee_type')}),
        ('Additional Details', {'fields': ('dietary_requirements', 'special_needs', 'how_did_you_hear')}),
        ('Status', {'fields': ('is_confirmed', 'payment_status')}),
    )

    @admin.action(description='Mark selected as confirmed')
    def mark_confirmed(self, request, queryset):
        n = queryset.update(is_confirmed=True)
        self.message_user(request, f'{n} registration(s) marked as confirmed.', messages.SUCCESS)

    @admin.action(description='Mark selected as paid')
    def mark_paid(self, request, queryset):
        n = queryset.update(payment_status='paid')
        self.message_user(request, f'{n} registration(s) marked as paid.', messages.SUCCESS)


# ------------------------------------------------------------------- awards

@admin.register(AwardCategory)
class AwardCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('order', 'name')
    fields = ('name', 'description', 'criteria', 'is_active', 'order')


@admin.register(Nomination)
class NominationAdmin(admin.ModelAdmin):
    list_display = ('nominee_name', 'category', 'nominator_name', 'submitted_at', 'is_reviewed', 'is_approved')
    list_editable = ('is_reviewed', 'is_approved')
    list_filter = ('category', 'is_reviewed', 'is_approved', 'submitted_at')
    search_fields = ('nominee_name', 'nominator_name', 'nominee_company', 'nominator_email')
    readonly_fields = ('submitted_at',)
    date_hierarchy = 'submitted_at'
    actions = [export_csv('nominations', [
        ('Category', lambda n: n.category), ('Nominee', lambda n: n.nominee_name),
        ('Nominee company', lambda n: n.nominee_company), ('Nominator', lambda n: n.nominator_name),
        ('Nominator email', lambda n: n.nominator_email), ('Nominator phone', lambda n: n.nominator_phone),
        ('Reason', lambda n: n.nomination_reason),
        ('Reviewed', lambda n: 'Yes' if n.is_reviewed else 'No'),
        ('Approved', lambda n: 'Yes' if n.is_approved else 'No'),
        ('Submitted', lambda n: timezone.localtime(n.submitted_at).strftime('%Y-%m-%d %H:%M')),
    ])]
    fieldsets = (
        ('Nominee Information', {'fields': ('category', 'nominee_name', 'nominee_company')}),
        ('Nominator Information', {'fields': ('nominator_name', 'nominator_email', 'nominator_phone')}),
        ('Nomination Details', {'fields': ('nomination_reason', 'supporting_documents', 'submitted_at')}),
        ('Review Status', {'fields': ('is_reviewed', 'is_approved')}),
    )


# ------------------------------------------------------- speakers & partners

@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ('photo_preview', 'name', 'title', 'company', 'is_featured', 'order')
    list_display_links = ('photo_preview', 'name')
    list_editable = ('is_featured', 'order')
    list_filter = ('is_featured',)
    search_fields = ('name', 'title', 'company')
    ordering = ('order', 'name')
    readonly_fields = ('current_photo',)
    current_photo = image_preview_field('photo', 160)
    fields = ('name', 'title', 'company', 'bio', 'photo', 'current_photo',
              'linkedin_url', 'twitter_url', 'is_featured', 'order')

    @admin.display(description='Photo')
    def photo_preview(self, obj):
        return thumb(obj.photo, 44, rounded=True)


@admin.register(SponsorshipLevel)
class SponsorshipLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'max_sponsors', 'order')
    list_editable = ('price', 'order')
    ordering = ('order',)


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('logo_preview', 'name', 'level', 'is_active')
    list_display_links = ('logo_preview', 'name')
    list_editable = ('is_active',)
    list_filter = ('level', 'is_active')
    search_fields = ('name', 'website')
    ordering = ('level__order', 'name')
    readonly_fields = ('created_at', 'current_logo')
    current_logo = image_preview_field('logo', 100)
    fieldsets = (
        ('Basic Information', {'fields': ('name', 'level', 'logo', 'current_logo', 'website')}),
        ('Details', {'fields': ('description', 'is_active')}),
        ('Timestamps', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )

    @admin.display(description='Logo')
    def logo_preview(self, obj):
        return thumb(obj.logo, 40)


@admin.register(SummitOrganizer)
class SummitOrganizerAdmin(admin.ModelAdmin):
    list_display = ('logo_preview', 'name', 'order', 'is_active')
    list_display_links = ('logo_preview', 'name')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('order', 'name')
    readonly_fields = ('current_logo',)
    current_logo = image_preview_field('logo', 100)
    fields = ('name', 'logo', 'current_logo', 'website', 'description', 'order', 'is_active')

    @admin.display(description='Logo')
    def logo_preview(self, obj):
        return thumb(obj.logo, 40)


@admin.register(ExhibitionPackage)
class ExhibitionPackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'space_size', 'max_exhibitors', 'order')
    list_editable = ('price', 'order')
    ordering = ('order',)


@admin.register(Exhibitor)
class ExhibitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'package', 'contact_person', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    list_filter = ('package', 'is_approved')
    search_fields = ('name', 'contact_person')
    fieldsets = (
        ('Company Information', {'fields': ('name', 'package', 'company_description', 'logo', 'website')}),
        ('Contact Information', {'fields': ('contact_person', 'contact_email', 'contact_phone')}),
        ('Approval Status', {'fields': ('is_approved',)}),
    )
