import secrets
from io import BytesIO
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


def current_year():
    return timezone.now().year


class SingletonModel(models.Model):
    """A model that only ever has one row. Use ``Model.get_solo()`` to fetch it."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and type(self).objects.exists():
            raise ValidationError(f'There can be only one {type(self).__name__} instance')
        return super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj


def resize_image(fieldfile, max_px, quality=82):
    """Return (ContentFile, (w, h)) of the image scaled to fit max_px, as JPEG."""
    from PIL import Image, ImageOps

    fieldfile.open('rb')
    fieldfile.seek(0)
    img = Image.open(fieldfile)
    img = ImageOps.exif_transpose(img)
    img.thumbnail((max_px, max_px))
    if img.mode not in ('RGB', 'L'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1])
        img = background
    buf = BytesIO()
    img.save(buf, 'JPEG', quality=quality, optimize=True, progressive=True)
    return ContentFile(buf.getvalue()), img.size


class SiteSettings(SingletonModel):
    site_name = models.CharField(max_length=200, default="Nigeria Transport and Logistics Summit and Awards")
    primary_organizer_logo = models.ImageField(upload_to='site_assets/', blank=True, null=True, help_text="Primary organizer logo (appears first in navigation)")
    site_logo = models.ImageField(upload_to='site_assets/', blank=True, null=True, help_text="Main summit logo (appears second in navigation)")
    favicon = models.ImageField(upload_to='site_assets/', blank=True, null=True, help_text="Favicon (.ico, .png)")
    hero_background_image = models.ImageField(upload_to='hero_images/', blank=True, null=True, help_text="Hero section background image")
    contact_email = models.EmailField(default="info@tlngsummit.com")
    contact_phone = models.CharField(max_length=20, default="+234 xxx xxx xxxx")
    social_facebook = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)
    social_linkedin = models.URLField(blank=True)
    social_instagram = models.URLField(blank=True)
    contact_address = models.CharField(max_length=300, blank=True, help_text="Office address shown in the footer (optional)")

    # Email routing
    sponsorship_email = models.EmailField(blank=True, help_text="Where 'Get Started' sponsorship buttons send enquiries. Defaults to the contact email.")
    exhibition_email = models.EmailField(blank=True, help_text="Where 'Book Booth' buttons send enquiries. Defaults to the contact email.")
    speakers_email = models.EmailField(blank=True, help_text="Where 'Interested in speaking?' enquiries go. Defaults to the contact email.")
    awards_email = models.EmailField(blank=True, help_text="Where nomination questions go. Defaults to the contact email.")

    # Registration
    registration_open = models.BooleanField(default=True, help_text="Untick to close registration. Visitors will see the 'registration closed' message instead of the form.")
    send_confirmation_emails = models.BooleanField(default=True, help_text="Email registrants a confirmation with their reference number")
    registration_notify_email = models.EmailField(blank=True, help_text="Send a notification here for every new registration. Defaults to the contact email.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def _email(self, value):
        return value or self.contact_email

    @property
    def sponsorship_contact(self):
        return self._email(self.sponsorship_email)

    @property
    def exhibition_contact(self):
        return self._email(self.exhibition_email)

    @property
    def speakers_contact(self):
        return self._email(self.speakers_email)

    @property
    def awards_contact(self):
        return self._email(self.awards_email)

    @property
    def registration_notify_contact(self):
        return self._email(self.registration_notify_email)


class EventContent(SingletonModel):
    title = models.CharField(max_length=200, default="Nigeria Transport and Logistics Summit and Awards")
    subtitle = models.TextField(default="Join industry leaders, innovators, and stakeholders as we shape the future of Nigeria's transport and logistics sector.", help_text="Hero section subtitle/description")
    event_date = models.DateTimeField(default=timezone.now)
    venue = models.CharField(max_length=300, default="Lagos, Nigeria")
    about_title = models.CharField(max_length=200, default="Nigeria's Premier Transport & Logistics Event")
    about_text = models.TextField(default="The Nigeria Transport and Logistics Summit and Awards brings together industry leaders, innovators, and decision-makers to shape the future of the transport and logistics sector.")
    hero_badge_text = models.CharField(max_length=100, blank=True, help_text="Text for hero badge (e.g., 'Coming Soon')")
    
    # Hero Stats
    stat_1_number = models.CharField(max_length=20, default="500+")
    stat_1_label = models.CharField(max_length=50, default="Attendees")
    stat_2_number = models.CharField(max_length=20, default="50+")
    stat_2_label = models.CharField(max_length=50, default="Speakers")
    stat_3_number = models.CharField(max_length=20, default="100+")
    stat_3_label = models.CharField(max_length=50, default="Companies")
    stat_4_number = models.CharField(max_length=20, default="2")
    stat_4_label = models.CharField(max_length=50, default="Days")
    
    # About Features
    feature_1_title = models.CharField(max_length=100, default="Networking Opportunities")
    feature_1_description = models.CharField(max_length=200, default="with 500+ industry professionals")
    feature_2_title = models.CharField(max_length=100, default="Innovation Showcase")
    feature_2_description = models.CharField(max_length=200, default="featuring latest technologies and solutions")
    feature_3_title = models.CharField(max_length=100, default="Awards Ceremony")
    feature_3_description = models.CharField(max_length=200, default="recognizing excellence in the industry")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Event Content"
        verbose_name_plural = "Event Content"

    def __str__(self):
        return self.title


class Speaker(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=300)
    company = models.CharField(max_length=200, blank=True)
    bio = models.TextField()
    photo = models.ImageField(upload_to='speakers/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.title}"


class SponsorshipLevel(models.Model):
    LEVEL_CHOICES = [
        ('platinum', 'Platinum'),
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
        ('supporting', 'Supporting'),
    ]
    
    name = models.CharField(max_length=100, choices=LEVEL_CHOICES, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    benefits = models.TextField(help_text="List benefits, one per line")
    max_sponsors = models.PositiveIntegerField(default=10)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.get_name_display()} - ${self.price}"


class Sponsor(models.Model):
    name = models.CharField(max_length=200)
    level = models.ForeignKey(SponsorshipLevel, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='sponsors/')
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['level__order', 'name']

    def __str__(self):
        return f"{self.name} ({self.level.get_name_display()})"


class AwardCategory(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    criteria = models.TextField(help_text="Judging criteria")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Award Categories"

    def __str__(self):
        return self.name


class Nomination(models.Model):
    category = models.ForeignKey(AwardCategory, on_delete=models.CASCADE)
    nominee_name = models.CharField(max_length=200)
    nominee_company = models.CharField(max_length=200, blank=True)
    nominator_name = models.CharField(max_length=200)
    nominator_email = models.EmailField()
    nominator_phone = models.CharField(max_length=20, blank=True)
    nomination_reason = models.TextField()
    supporting_documents = models.FileField(upload_to='nominations/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.nominee_name} - {self.category.name}"


class AboutSectionContent(SingletonModel):
    about_image = models.ImageField(upload_to='about_section/', blank=True, null=True, help_text="Image for the about section after hero")
    image_alt_text = models.CharField(max_length=200, default="Transport and Logistics", help_text="Alt text for the about section image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Section Content"
        verbose_name_plural = "About Section Content"

    def __str__(self):
        return "About Section Content"


class SummitOrganizer(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='organizers/')
    website = models.URLField(blank=True)
    description = models.TextField(blank=True, help_text="Brief description of the organization")
    order = models.PositiveIntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Summit Organizer"
        verbose_name_plural = "Summit Organizers"

    def __str__(self):
        return self.name


class ConferenceRegistration(models.Model):
    ATTENDEE_TYPES = [
        ('individual', 'Individual'),
        ('corporate', 'Corporate'),
        ('student', 'Student'),
        ('media', 'Media'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=200, blank=True)
    attendee_type = models.CharField(max_length=20, choices=ATTENDEE_TYPES, default='individual')
    ticket = models.ForeignKey('TicketType', on_delete=models.PROTECT, null=True, related_name='registrations')
    reference = models.CharField(max_length=20, unique=True, null=True, blank=True, editable=False)
    dietary_requirements = models.TextField(blank=True, help_text="Any special dietary requirements")
    special_needs = models.TextField(blank=True, help_text="Any accessibility requirements")
    how_did_you_hear = models.CharField(max_length=200, blank=True, help_text="How did you hear about this event?")
    registration_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, default='pending', choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ])

    class Meta:
        ordering = ['-registration_date']
        verbose_name = "Conference Registration"
        verbose_name_plural = "Conference Registrations"

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @staticmethod
    def generate_reference():
        alphabet = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
        while True:
            code = 'TLNG-{}-{}'.format(timezone.now().year, ''.join(secrets.choice(alphabet) for _ in range(6)))
            if not ConferenceRegistration.objects.filter(reference=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.generate_reference()
        super().save(*args, **kwargs)


class ExhibitionPackage(models.Model):
    PACKAGE_TYPES = [
        ('standard', 'Standard Booth'),
        ('premium', 'Premium Booth'),
        ('corner', 'Corner Booth'),
        ('island', 'Island Booth'),
    ]
    
    name = models.CharField(max_length=100, choices=PACKAGE_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    space_size = models.CharField(max_length=50, help_text="e.g., 3m x 3m")
    features = models.TextField(help_text="List features, one per line")
    max_exhibitors = models.PositiveIntegerField(default=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.get_name_display()} - ${self.price}"


class Exhibitor(models.Model):
    name = models.CharField(max_length=200)
    package = models.ForeignKey(ExhibitionPackage, on_delete=models.CASCADE)
    company_description = models.TextField()
    logo = models.ImageField(upload_to='exhibitors/')
    website = models.URLField(blank=True)
    contact_person = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.package.get_name_display()})"


class TicketType(models.Model):
    """Registration ticket options, managed by admins."""
    name = models.CharField(max_length=100)
    code = models.SlugField(max_length=50, unique=True, help_text="Short internal identifier, e.g. 'vip'")
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Price in Naira. Use 0 for free tickets.")
    description = models.TextField(blank=True, help_text="What this ticket includes (one item per line)")
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum registrations for this ticket. Leave blank for unlimited.")
    is_active = models.BooleanField(default=True, help_text="Show this ticket on the registration form")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'price']
        verbose_name = "Ticket Type"

    def __str__(self):
        return self.name

    @property
    def is_free(self):
        return not self.price

    @property
    def spots_left(self):
        if self.capacity is None:
            return None
        return max(self.capacity - self.registrations.count(), 0)

    @property
    def is_sold_out(self):
        return self.spots_left == 0


class ContentBlock(models.Model):
    """A piece of editable site copy, identified by a key such as 'home.cta.title'.

    Blocks are created automatically the first time a page that uses them is shown,
    so they always appear in the admin and can be edited live on the site.
    """
    key = models.CharField(max_length=150, unique=True)
    value = models.TextField(blank=True)
    multiline = models.BooleanField(default=False, editable=False)
    page = models.CharField(max_length=50, editable=False, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['page', 'key']
        verbose_name = "Text Block"
        verbose_name_plural = "Text Blocks"

    def __str__(self):
        return self.label

    @property
    def label(self):
        parts = self.key.split('.')[1:] or [self.key]
        return ' › '.join(p.replace('_', ' ').capitalize() for p in parts)

    def save(self, *args, **kwargs):
        self.page = self.key.split('.', 1)[0]
        super().save(*args, **kwargs)


class Highlight(models.Model):
    """Repeatable icon cards ('Key Topics', 'Why Attend', 'Why Partner With Us')."""
    SECTION_CHOICES = [
        ('topics', 'Key Topics & Sessions'),
        ('why_attend', 'Why Attend'),
        ('partner_benefits', 'Why Partner With Us (Sponsorship page)'),
    ]
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    icon = models.CharField(max_length=50, default='fa-star', help_text="Font Awesome icon name, e.g. fa-leaf, fa-truck, fa-users. Browse at fontawesome.com/icons")
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['section', 'order', 'id']
        verbose_name = "Feature Card"
        verbose_name_plural = "Feature Cards"

    def __str__(self):
        return f"{self.get_section_display()}: {self.title}"


class GalleryAlbum(models.Model):
    """A photo album, typically one per summit edition or side event."""
    title = models.CharField(max_length=200, help_text="e.g. 'TLNG Summit & Awards 2024'")
    slug = models.SlugField(max_length=220, unique=True, blank=True, help_text="Used in the web address. Filled in automatically.")
    year = models.PositiveSmallIntegerField(default=current_year, help_text="Used to group albums on the gallery page")
    event_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='gallery/covers/', blank=True, null=True, help_text="Optional. The first photo is used if this is empty.")
    is_published = models.BooleanField(default=True, help_text="Untick to hide this album from the public site")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first within the same year")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-year', 'order', '-event_date', '-id']
        verbose_name = "Gallery Album"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200] or 'album'
            slug, n = base, 2
            while GalleryAlbum.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('gallery_album', args=[self.slug])

    @property
    def cover(self):
        """URL for the album cover: the explicit cover, else the first photo."""
        if self.cover_image:
            return self.cover_image.url
        first = self.photos.first()
        return first.thumb_url if first else ''


class GalleryPhoto(models.Model):
    MAX_SIZE = 2400   # longest edge of stored originals
    THUMB_SIZE = 800  # longest edge of grid thumbnails

    album = models.ForeignKey(GalleryAlbum, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='gallery/%Y/%m/')
    thumbnail = models.ImageField(upload_to='gallery/thumbs/%Y/%m/', blank=True, editable=False)
    width = models.PositiveIntegerField(default=0, editable=False)
    height = models.PositiveIntegerField(default=0, editable=False)
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']
        verbose_name = "Gallery Photo"

    def __str__(self):
        return self.caption or Path(self.image.name).name

    @property
    def thumb_url(self):
        return (self.thumbnail or self.image).url

    def save(self, *args, **kwargs):
        is_new_upload = self.image and not getattr(self.image, '_committed', True)
        if is_new_upload or (self.image and not self.thumbnail):
            stem = Path(self.image.name).stem[:80]
            try:
                if is_new_upload:
                    content, (self.width, self.height) = resize_image(self.image, self.MAX_SIZE, quality=86)
                    self.image.save(f'{stem}.jpg', content, save=False)
                thumb, size = resize_image(self.image, self.THUMB_SIZE)
                if not self.width:
                    self.width, self.height = size
                self.thumbnail.save(f'{stem}_thumb.jpg', thumb, save=False)
            except Exception:  # unreadable image: keep the original as-is
                import logging
                logging.getLogger('summit').warning('Could not process gallery image %s', self.image.name, exc_info=True)
        super().save(*args, **kwargs)


# Remove image files from storage when gallery rows are deleted.
from django.db.models.signals import post_delete  # noqa: E402
from django.dispatch import receiver  # noqa: E402


@receiver(post_delete, sender=GalleryPhoto)
def _delete_photo_files(sender, instance, **kwargs):
    for f in (instance.image, instance.thumbnail):
        if f:
            f.storage.delete(f.name)


@receiver(post_delete, sender=GalleryAlbum)
def _delete_album_cover(sender, instance, **kwargs):
    if instance.cover_image:
        instance.cover_image.storage.delete(instance.cover_image.name)
