from django import template

from foodate.settings import HOST_SCHEME, PARENT_HOST

register = template.Library()


@register.simple_tag
def uploads(file_path):
    return f'{HOST_SCHEME}{PARENT_HOST}/{file_path}'
