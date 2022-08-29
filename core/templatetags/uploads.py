from django import template

from foodate.settings import HOST_SCHEME, PARENT_HOST, MEDIA_URL

register = template.Library()


@register.simple_tag
def uploads(file_path):
    """Returns uploads link"""
    return f'{HOST_SCHEME}{PARENT_HOST}/{MEDIA_URL}{file_path}'
