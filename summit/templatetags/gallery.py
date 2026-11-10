"""Helpers for the photo collage layout."""
from django import template

register = template.Library()


@register.filter
def tile_class(photo, index):
    """Pick a collage tile shape from the photo's proportions and its position.

    Tiles are placed with ``grid-auto-flow: dense`` so mixed sizes pack tightly.
    """
    i = int(index)
    w, h = photo.width or 0, photo.height or 0
    if i % 10 == 1:
        return 'tile-xl'
    if w and h and h > w * 1.15:
        return 'tile-tall'
    if (w and h and w > h * 1.7) or i % 10 in (4, 8):
        return 'tile-wide'
    return ''
