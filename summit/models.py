from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default="Nigeria Transport and Logistics Summit and Awards")
    site_logo = models.ImageField(upload_to='site_assets/', blank=True, null=True, help_text="Logo for navigation and footer")
    favicon = models.ImageField(upload_to='site_assets/', blank=True, null=True, help_text="Favicon (.ico, .png)")
    hero_background_image = models.ImageField(upload_to='hero_images/', blank=True, null=True, help_text="Hero section background image")
    contact_email = models.EmailField(default="info@tlngsummit.com")
    contact_phone = models.CharField(max_length=20, default="+234 xxx xxx xxxx")
    social_facebook = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)
    social_linkedin = models.URLField(blank=True)
    social_instagram = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValidationError('There can be only one SiteSettings instance')
        return super(SiteSettings, self).save(*args, **kwargs)


class EventContent(models.Model):
    title = models.CharField(max_length=200, default="Nigeria Transport and Logistics Summit and Awards")
    subtitle = models.TextField(default="Join industry leaders, innovators, and stakeholders as we shape the future of Nigeria's transport and logistics sector.", help_text="Hero section subtitle/description")
    event_date = models.DateTimeField()
    venue = models.CharField(max_length=300)
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

    def save(self, *args, **kwargs):
        if not self.pk and EventContent.objects.exists():
            raise ValidationError('There can be only one EventContent instance')
        return super(EventContent, self).save(*args, **kwargs)


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
