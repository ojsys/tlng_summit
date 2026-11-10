"""Live ("on the fly") editing for staff users.

Templates mark content as editable with the tags in ``summit.templatetags.cms``.
When a staff member turns on *Edit page* in the toolbar, those elements become
editable in place and changes are posted to the views below.

Only the models listed in ``EDITABLE_MODELS`` can be changed this way, only
text and image fields can be touched, and the user needs the normal Django
"change" permission for the model. Visitor submissions (registrations,
nominations) are deliberately not editable from the front end.
"""
import json
import logging

from django import forms
from django.apps import apps
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .forms import MAX_UPLOAD_MB
from .models import GalleryAlbum, GalleryPhoto

logger = logging.getLogger('summit')

EDITABLE_MODELS = {
    'summit.sitesettings', 'summit.eventcontent', 'summit.aboutsectioncontent',
    'summit.contentblock', 'summit.highlight', 'summit.speaker', 'summit.sponsor',
    'summit.summitorganizer', 'summit.awardcategory', 'summit.tickettype',
    'summit.exhibitionpackage', 'summit.galleryalbum', 'summit.galleryphoto',
}
TEXT_FIELDS = (models.CharField, models.TextField)


def model_label(obj_or_model):
    return obj_or_model._meta.label_lower


def can_edit(user, model):
    if not (user and user.is_authenticated and user.is_staff):
        return False
    meta = model._meta
    return (meta.label_lower in EDITABLE_MODELS
            and user.has_perm(f'{meta.app_label}.change_{meta.model_name}'))


def editable_field(model, field_name):
    """Return the model field if it may be edited live, else None."""
    try:
        field = model._meta.get_field(field_name)
    except Exception:
        return None
    if not getattr(field, 'editable', False) or getattr(field, 'choices', None):
        return None
    if isinstance(field, (models.ImageField,) + TEXT_FIELDS) and not isinstance(field, models.SlugField):
        return field
    return None


def _error(message, status=400):
    return JsonResponse({'ok': False, 'error': message}, status=status)


def _check_image(upload):
    if upload.size > MAX_UPLOAD_MB * 1024 * 1024:
        raise ValidationError(f'Image is too large. The maximum size is {MAX_UPLOAD_MB} MB.')
    return forms.ImageField().clean(upload)


@staff_member_required
@require_POST
def update_field(request):
    """Save one text or image field. Expects model, pk, field and value / file."""
    try:
        model = apps.get_model(request.POST.get('model', ''))
    except (LookupError, ValueError):
        return _error('Unknown content type.')
    if not can_edit(request.user, model):
        return _error('You do not have permission to edit this content.', 403)
    field = editable_field(model, request.POST.get('field', ''))
    if field is None:
        return _error('This field cannot be edited here.')

    obj = get_object_or_404(model, pk=request.POST.get('pk'))
    try:
        if isinstance(field, models.ImageField):
            upload = request.FILES.get('file')
            if not upload:
                return _error('No image was uploaded.')
            setattr(obj, field.name, _check_image(upload))
        else:
            value = request.POST.get('value', '').replace('\r\n', '\n').strip()
            if not isinstance(field, models.TextField):
                value = ' '.join(value.split())  # single-line fields: collapse newlines
            setattr(obj, field.name, field.clean(value, obj))
        obj.save()
    except ValidationError as e:
        return _error(' '.join(e.messages))

    logger.info('Live edit by %s: %s #%s .%s', request.user, model_label(model), obj.pk, field.name)
    new_value = getattr(obj, field.name)
    if isinstance(field, models.ImageField):
        return JsonResponse({'ok': True, 'url': new_value.url if new_value else ''})
    return JsonResponse({'ok': True, 'value': new_value})


@staff_member_required
@require_POST
def gallery_upload(request, pk):
    if not request.user.has_perm('summit.add_galleryphoto'):
        raise PermissionDenied
    album = get_object_or_404(GalleryAlbum, pk=pk)
    files = request.FILES.getlist('files')
    if not files:
        return _error('No photos were selected.')
    start = (album.photos.aggregate(m=models.Max('order'))['m'] or 0) + 1
    created, errors = [], []
    for i, upload in enumerate(files):
        try:
            image = _check_image(upload)
        except ValidationError as e:
            errors.append(f'{upload.name}: {" ".join(e.messages)}')
            continue
        photo = GalleryPhoto.objects.create(album=album, image=image, order=start + i)
        created.append({'id': photo.pk, 'thumb': photo.thumb_url, 'full': photo.image.url})
    logger.info('%s uploaded %d photos to album %s', request.user, len(created), album.slug)
    return JsonResponse({'ok': bool(created), 'photos': created, 'errors': errors,
                         'error': '; '.join(errors) if not created else ''})


@staff_member_required
@require_POST
def gallery_photo_delete(request, pk):
    if not request.user.has_perm('summit.delete_galleryphoto'):
        raise PermissionDenied
    photo = get_object_or_404(GalleryPhoto, pk=pk)
    photo.delete()
    return JsonResponse({'ok': True})


@staff_member_required
@require_POST
def gallery_reorder(request, pk):
    if not request.user.has_perm('summit.change_galleryphoto'):
        raise PermissionDenied
    album = get_object_or_404(GalleryAlbum, pk=pk)
    try:
        ids = [int(i) for i in json.loads(request.body).get('order', [])]
    except (ValueError, TypeError, AttributeError):
        return _error('Invalid order.')
    photos = {p.pk: p for p in album.photos.filter(pk__in=ids)}
    for position, photo_id in enumerate(ids, start=1):
        if photo_id in photos:
            photos[photo_id].order = position
    GalleryPhoto.objects.bulk_update(photos.values(), ['order'])
    return JsonResponse({'ok': True})
