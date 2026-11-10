"""Template tags that make content editable on the live site.

    {% load cms %}

    {% cms_block "home.cta.title" "Ready to Join Us?" %}
        Site copy stored in a ContentBlock. Created automatically with the given
        default the first time the page renders. Add ``multiline=True`` for
        paragraphs.

    {% cms_field event_content "title" %}
        A text field on any model instance.

    <img src="..." {% cms_image speaker "photo" %}>
        Adds the attributes that let staff replace an image (or background image).

    {% cms_manage "summit.speaker" "Manage speakers" %}
        A button, shown only in edit mode, linking to the admin list for a model.

Visitors who are not staff get plain, escaped text and no extra markup.
"""
from django import template
from django.db import models
from django.urls import NoReverseMatch, reverse
from django.utils.html import escape, format_html, format_html_join, linebreaks
from django.utils.safestring import mark_safe

from ..cms import can_edit, model_label
from ..models import ContentBlock

register = template.Library()


def _request(context):
    return context.get('request')


def _can_edit(context, model):
    request = _request(context)
    if request is None:
        return False
    cache = request.__dict__.setdefault('_cms_perm_cache', {})
    key = model_label(model)
    if key not in cache:
        cache[key] = can_edit(getattr(request, 'user', None), model)
    return cache[key]


def _render_plain(value, multiline):
    value = value or ''
    if multiline:
        # linebreaks() escapes for us and turns blank lines into paragraphs.
        return mark_safe(linebreaks(value, autoescape=True).replace('<p>', '<span class="cms-p">').replace('</p>', '</span>'))
    return escape(value)


def _render_editable(value, obj, field, multiline, placeholder):
    return format_html(
        '<span class="cms-text{}" data-cms="{}" data-cms-model="{}" data-cms-pk="{}" '
        'data-cms-field="{}" data-cms-placeholder="{}">{}</span>',
        ' cms-multiline' if multiline else '',
        'textarea' if multiline else 'text',
        model_label(obj), obj.pk, field, placeholder, value or '',
    )


def _blocks(request):
    """Load every content block once per request."""
    if request is None:
        return {b.key: b for b in ContentBlock.objects.all()}
    if not hasattr(request, '_cms_blocks'):
        request._cms_blocks = {b.key: b for b in ContentBlock.objects.all()}
    return request._cms_blocks


@register.simple_tag(takes_context=True)
def cms_block(context, key, default='', multiline=False):
    blocks = _blocks(_request(context))
    block = blocks.get(key)
    if block is None:
        block, _ = ContentBlock.objects.get_or_create(
            key=key, defaults={'value': default, 'multiline': bool(multiline)})
        blocks[key] = block
    if _can_edit(context, ContentBlock):
        return _render_editable(block.value, block, 'value', multiline, 'Click to add text')
    return _render_plain(block.value, multiline)


@register.simple_tag(takes_context=True)
def cms_list(context, key, default='', icon='fa-chevron-right text-primary-custom', ul_class='list-unstyled'):
    """A bulleted list stored as one text block: one bullet per line.

    ``default`` separates lines with " | ".
    """
    blocks = _blocks(_request(context))
    block = blocks.get(key)
    if block is None:
        value = '\n'.join(part.strip() for part in default.split('|') if part.strip())
        block, _ = ContentBlock.objects.get_or_create(key=key, defaults={'value': value, 'multiline': True})
        blocks[key] = block
    lines = [line.strip() for line in block.value.splitlines() if line.strip()]
    icon_html = format_html('<i class="fas {} me-2"></i>', icon) if icon else ''
    items = format_html_join('', '<li>{}{}</li>', ((icon_html, line) for line in lines))
    html = format_html('<ul class="{} cms-list-view" data-icon="{}">{}</ul>', ul_class, icon, items)
    if _can_edit(context, ContentBlock):
        editable = format_html(
            '<span class="cms-text cms-multiline cms-list-edit" data-cms="textarea" data-cms-list="1" '
            'data-cms-model="{}" data-cms-pk="{}" data-cms-field="value" '
            'data-cms-placeholder="One item per line">{}</span>',
            model_label(block), block.pk, block.value)
        html = html + editable
    return html


@register.simple_tag(takes_context=True)
def cms_field(context, obj, field_name, multiline=None, placeholder='Click to add text'):
    if obj is None:
        return ''
    value = getattr(obj, field_name, '')
    if multiline is None:
        try:
            multiline = isinstance(obj._meta.get_field(field_name), models.TextField)
        except Exception:
            multiline = False
    if getattr(obj, 'pk', None) and _can_edit(context, type(obj)):
        return _render_editable(value, obj, field_name, multiline, placeholder)
    return _render_plain(value, multiline)


@register.simple_tag(takes_context=True)
def cms_image(context, obj, field_name, background=False):
    """Attributes that make an <img> (or a background-image container) replaceable."""
    if obj is None or not getattr(obj, 'pk', None) or not _can_edit(context, type(obj)):
        return ''
    return format_html(
        ' data-cms="image" data-cms-model="{}" data-cms-pk="{}" data-cms-field="{}"{}',
        model_label(obj), obj.pk, field_name,
        mark_safe(' data-cms-background="1"') if background else '',
    )


@register.simple_tag(takes_context=True)
def cms_manage(context, label, text, action='changelist', obj=None):
    """Edit-mode-only button linking to the admin for a model (or an object)."""
    request = _request(context)
    user = getattr(request, 'user', None)
    if not (user and user.is_authenticated and user.is_staff):
        return ''
    app_label, model_name = label.split('.')
    try:
        if obj is not None:
            url = reverse(f'admin:{app_label}_{model_name}_change', args=[obj.pk])
        else:
            url = reverse(f'admin:{app_label}_{model_name}_{action}')
    except NoReverseMatch:
        return ''
    icon = 'fa-plus' if action == 'add' else 'fa-pen'
    return format_html(
        '<a class="cms-manage" href="{}"><i class="fas {}"></i> {}</a>', url, icon, text)


@register.filter
def naira(value):
    """Format a price as ₦1,234 (or 'Free')."""
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return value
    if not amount:
        return 'Free'
    return '₦{:,.0f}'.format(amount)
