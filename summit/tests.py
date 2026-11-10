import json
import shutil
import tempfile
from io import BytesIO

from django.contrib.auth.models import Permission, User
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import (
    ConferenceRegistration, ContentBlock, EventContent, GalleryAlbum,
    GalleryPhoto, Highlight, Nomination, SiteSettings, TicketType,
)

MEDIA = tempfile.mkdtemp()


def image_file(name='photo.jpg', size=(3000, 2000), color=(0, 135, 81), fmt='JPEG'):
    buf = BytesIO()
    Image.new('RGB', size, color).save(buf, fmt)
    return SimpleUploadedFile(name, buf.getvalue(), content_type=f'image/{fmt.lower()}')


@override_settings(MEDIA_ROOT=MEDIA)
class BaseTest(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA, ignore_errors=True)

    def make_staff(self, superuser=True):
        if superuser:
            user = User.objects.create_superuser('admin', 'a@example.com', 'pw')
        else:
            user = User.objects.create_user('editor', 'e@example.com', 'pw', is_staff=True)
        self.client.force_login(user)
        return user


class PublicPagesTest(BaseTest):
    def test_all_pages_render_without_existing_content(self):
        for name in ['home', 'speakers', 'sponsorship', 'nominations', 'registration',
                     'registration_success', 'nomination_success', 'gallery']:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_seeded_cards_shown_on_home(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Last-Mile Delivery Innovation')
        self.assertContains(response, 'Why Attend?')

    def test_visitors_get_no_edit_markup(self):
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'data-cms=')
        self.assertNotContains(response, 'cms-toolbar')

    def test_content_blocks_created_with_defaults(self):
        self.client.get(reverse('home'))
        self.assertEqual(ContentBlock.objects.get(key='home.cta.title').value, 'Ready to Join Us?')

    def test_block_text_is_escaped(self):
        self.client.get(reverse('home'))
        ContentBlock.objects.filter(key='home.cta.title').update(value='<script>alert(1)</script>')
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, '<script>alert(1)</script>')
        self.assertContains(response, '&lt;script&gt;alert(1)&lt;/script&gt;')


class LiveEditingTest(BaseTest):
    def setUp(self):
        self.event = EventContent.get_solo()

    def post(self, **data):
        return self.client.post(reverse('cms_update'), data)

    def test_staff_see_toolbar_and_editable_markup(self):
        self.make_staff()
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'id="cms-toolbar"')
        self.assertContains(response, 'data-cms-model="summit.eventcontent"')

    def test_update_text_field(self):
        self.make_staff()
        r = self.post(model='summit.eventcontent', pk=self.event.pk, field='title', value='  New Title\n ')
        self.assertEqual(r.status_code, 200, r.content)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'New Title')

    def test_update_content_block_keeps_newlines(self):
        self.make_staff()
        self.client.get(reverse('home'))
        block = ContentBlock.objects.get(key='home.cta.text')
        self.post(model='summit.contentblock', pk=block.pk, field='value', value='Line one\nLine two')
        block.refresh_from_db()
        self.assertEqual(block.value, 'Line one\nLine two')

    def test_max_length_enforced(self):
        self.make_staff()
        r = self.post(model='summit.eventcontent', pk=self.event.pk, field='stat_1_number', value='x' * 50)
        self.assertEqual(r.status_code, 400)

    def test_anonymous_rejected(self):
        r = self.post(model='summit.eventcontent', pk=self.event.pk, field='title', value='Hacked')
        self.assertEqual(r.status_code, 302)  # redirected to admin login
        self.event.refresh_from_db()
        self.assertNotEqual(self.event.title, 'Hacked')

    def test_staff_without_permission_rejected(self):
        self.make_staff(superuser=False)
        r = self.post(model='summit.eventcontent', pk=self.event.pk, field='title', value='Hacked')
        self.assertEqual(r.status_code, 403)

    def test_staff_with_permission_allowed(self):
        user = self.make_staff(superuser=False)
        user.user_permissions.add(Permission.objects.get(codename='change_eventcontent'))
        r = self.post(model='summit.eventcontent', pk=self.event.pk, field='title', value='OK')
        self.assertEqual(r.status_code, 200)

    def test_submissions_and_users_not_editable(self):
        self.make_staff()
        ticket = TicketType.objects.first()
        reg = ConferenceRegistration.objects.create(first_name='A', last_name='B', email='a@b.co', phone='1', ticket=ticket)
        for model, pk, field in [('summit.conferenceregistration', reg.pk, 'first_name'),
                                 ('auth.user', 1, 'username')]:
            with self.subTest(model=model):
                self.assertEqual(self.post(model=model, pk=pk, field=field, value='x').status_code, 403)

    def test_non_text_fields_rejected(self):
        self.make_staff()
        r = self.post(model='summit.highlight', pk=Highlight.objects.first().pk, field='section', value='x')
        self.assertEqual(r.status_code, 400)

    def test_replace_image(self):
        self.make_staff()
        site = SiteSettings.get_solo()
        r = self.client.post(reverse('cms_update'), {
            'model': 'summit.sitesettings', 'pk': site.pk, 'field': 'hero_background_image',
            'file': image_file('hero.jpg', (800, 400))})
        self.assertEqual(r.status_code, 200, r.content)
        site.refresh_from_db()
        self.assertTrue(site.hero_background_image.name.startswith('hero_images/hero'))
        self.assertEqual(r.json()['url'], site.hero_background_image.url)

    def test_non_image_upload_rejected(self):
        self.make_staff()
        site = SiteSettings.get_solo()
        r = self.client.post(reverse('cms_update'), {
            'model': 'summit.sitesettings', 'pk': site.pk, 'field': 'site_logo',
            'file': SimpleUploadedFile('evil.jpg', b'not an image', content_type='image/jpeg')})
        self.assertEqual(r.status_code, 400)


class RegistrationTest(BaseTest):
    def data(self, **overrides):
        data = {'first_name': 'Ada', 'last_name': 'Obi', 'email': 'Ada@Example.com',
                'phone': '+2348000000000', 'attendee_type': 'individual',
                'ticket': TicketType.objects.get(code='regular').pk}
        data.update(overrides)
        return data

    def test_register_creates_reference_and_sends_emails(self):
        r = self.client.post(reverse('registration'), self.data())
        self.assertRedirects(r, reverse('registration_success'))
        reg = ConferenceRegistration.objects.get()
        self.assertRegex(reg.reference, r'^TLNG-\d{4}-[A-Z0-9]{6}$')
        self.assertEqual(reg.email, 'ada@example.com')
        self.assertEqual(len(mail.outbox), 2)  # confirmation + admin notification
        self.assertIn(reg.reference, mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].to, ['ada@example.com'])
        success = self.client.get(reverse('registration_success'))
        self.assertContains(success, reg.reference)

    def test_duplicate_email_rejected(self):
        self.client.post(reverse('registration'), self.data())
        r = self.client.post(reverse('registration'), self.data(email='ada@example.com'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'already registered')
        self.assertEqual(ConferenceRegistration.objects.count(), 1)

    def test_honeypot_blocks_bots(self):
        r = self.client.post(reverse('registration'), self.data(website='http://spam'))
        self.assertEqual(r.status_code, 200)
        self.assertFalse(ConferenceRegistration.objects.exists())

    def test_closed_registration(self):
        site = SiteSettings.get_solo()
        site.registration_open = False
        site.save()
        r = self.client.get(reverse('registration'))
        self.assertContains(r, 'Registration is currently closed')
        self.assertNotContains(r, 'id="registrationForm"')

    def test_sold_out_ticket_hidden(self):
        TicketType.objects.exclude(code='regular').update(is_active=False)
        TicketType.objects.filter(code='regular').update(capacity=1)
        self.client.post(reverse('registration'), self.data())
        r = self.client.get(reverse('registration'))
        self.assertContains(r, 'Tickets are sold out')

    def test_inactive_ticket_not_accepted(self):
        vip = TicketType.objects.get(code='vip')
        vip.is_active = False
        vip.save()
        r = self.client.post(reverse('registration'), self.data(ticket=vip.pk))
        self.assertEqual(r.status_code, 200)
        self.assertFalse(ConferenceRegistration.objects.exists())

    def test_csv_export(self):
        self.client.post(reverse('registration'), self.data())
        self.make_staff()
        reg = ConferenceRegistration.objects.get()
        page =self.client.get(reverse('admin:summit_conferenceregistration_changelist'))
        action = [a for a in page.context['action_form'].fields['action'].choices if 'CSV' in str(a[1])][0][0]
        r = self.client.post(reverse('admin:summit_conferenceregistration_changelist'),
                             {'action': action, '_selected_action': [reg.pk]})
        self.assertEqual(r['Content-Type'], 'text/csv')
        self.assertIn(reg.reference, r.content.decode())


class NominationTest(BaseTest):
    def test_nomination_redirects_to_success(self):
        from .models import AwardCategory
        cat = AwardCategory.objects.create(name="Nigeria's Best", description='d', criteria='c')
        r = self.client.post(reverse('nominations'), {
            'category': cat.pk, 'nominee_name': 'X', 'nominator_name': 'Y',
            'nominator_email': 'y@example.com', 'nomination_reason': 'Because'})
        self.assertRedirects(r, reverse('nomination_success'))
        self.assertEqual(Nomination.objects.count(), 1)

    def test_category_name_with_apostrophe_safe_in_button(self):
        from .models import AwardCategory
        AwardCategory.objects.create(name="Nigeria's Best", description='d', criteria='c')
        r = self.client.get(reverse('nominations'))
        self.assertContains(r, 'data-category-name="Nigeria&#x27;s Best"')
        self.assertNotContains(r, 'onclick="selectCategory')


class GalleryTest(BaseTest):
    def setUp(self):
        self.album = GalleryAlbum.objects.create(title='Summit 2024', year=2024)

    def test_slug_generated_and_unique(self):
        other = GalleryAlbum.objects.create(title='Summit 2024', year=2024)
        self.assertEqual(self.album.slug, 'summit-2024')
        self.assertEqual(other.slug, 'summit-2024-2')

    def test_photo_resized_and_thumbnailed(self):
        photo = GalleryPhoto.objects.create(album=self.album, image=image_file())
        self.assertEqual(max(photo.width, photo.height), GalleryPhoto.MAX_SIZE)
        self.assertTrue(photo.thumbnail)
        with Image.open(photo.thumbnail.path) as thumb:
            self.assertEqual(max(thumb.size), GalleryPhoto.THUMB_SIZE)

    def test_png_with_transparency(self):
        buf = BytesIO()
        Image.new('RGBA', (100, 100), (255, 0, 0, 0)).save(buf, 'PNG')
        photo = GalleryPhoto.objects.create(
            album=self.album, image=SimpleUploadedFile('t.png', buf.getvalue(), 'image/png'))
        self.assertTrue(photo.image.name.endswith('.jpg'))

    def test_album_page_and_listing(self):
        GalleryPhoto.objects.create(album=self.album, image=image_file(size=(400, 300)), caption='Opening')
        self.assertContains(self.client.get(reverse('gallery')), 'Summit 2024')
        r = self.client.get(self.album.get_absolute_url())
        self.assertContains(r, 'Opening')
        self.assertContains(r, 'data-lightbox="album"')
        self.assertContains(self.client.get(reverse('home')), 'Moments from Past Summits')

    def test_unpublished_album_hidden_from_public(self):
        GalleryPhoto.objects.create(album=self.album, image=image_file(size=(400, 300)))
        self.album.is_published = False
        self.album.save()
        self.assertEqual(self.client.get(self.album.get_absolute_url()).status_code, 404)
        self.assertNotContains(self.client.get(reverse('gallery')), 'Summit 2024')
        self.make_staff()
        self.assertEqual(self.client.get(self.album.get_absolute_url()).status_code, 200)

    def test_live_upload_delete_reorder(self):
        self.make_staff()
        r = self.client.post(reverse('cms_gallery_upload', args=[self.album.pk]),
                             {'files': [image_file('a.jpg', (500, 400)), image_file('b.jpg', (500, 400))]})
        self.assertEqual(len(r.json()['photos']), 2)
        a, b = self.album.photos.all()
        r = self.client.post(reverse('cms_gallery_reorder', args=[self.album.pk]),
                             json.dumps({'order': [b.pk, a.pk]}), content_type='application/json')
        self.assertTrue(r.json()['ok'])
        self.assertEqual(list(self.album.photos.values_list('pk', flat=True)), [b.pk, a.pk])
        path = a.image.path
        self.client.post(reverse('cms_photo_delete', args=[a.pk]))
        self.assertEqual(self.album.photos.count(), 1)
        import os
        self.assertFalse(os.path.exists(path))

    def test_upload_requires_staff(self):
        r = self.client.post(reverse('cms_gallery_upload', args=[self.album.pk]), {'files': [image_file()]})
        self.assertEqual(r.status_code, 302)
        self.assertFalse(self.album.photos.exists())

    def test_admin_bulk_upload(self):
        self.make_staff()
        url = reverse('admin:summit_galleryalbum_change', args=[self.album.pk])
        data = {'title': 'Summit 2024', 'slug': 'summit-2024', 'year': 2024, 'order': 0, 'is_published': 'on',
                'photos-TOTAL_FORMS': 0, 'photos-INITIAL_FORMS': 0,
                'bulk_photos': [image_file('x.jpg', (300, 200)), image_file('y.jpg', (300, 200))]}
        r = self.client.post(url, data)
        self.assertEqual(r.status_code, 302, r.content[:2000])
        self.assertEqual(self.album.photos.count(), 2)


class AdminTest(BaseTest):
    def test_dashboard_and_changelists_load(self):
        self.make_staff()
        self.assertContains(self.client.get(reverse('admin:index')), 'Edit the website live')
        for model in ['sitesettings', 'eventcontent', 'contentblock', 'highlight', 'galleryalbum',
                      'galleryphoto', 'tickettype', 'conferenceregistration', 'nomination', 'speaker',
                      'sponsor', 'awardcategory', 'summitorganizer', 'aboutsectioncontent']:
            with self.subTest(model=model):
                r = self.client.get(reverse(f'admin:summit_{model}_changelist'), follow=True)
                self.assertEqual(r.status_code, 200)

    def test_singleton_redirects_to_form(self):
        self.make_staff()
        r = self.client.get(reverse('admin:summit_sitesettings_changelist'))
        self.assertRedirects(r, reverse('admin:summit_sitesettings_change', args=[SiteSettings.get_solo().pk]))
