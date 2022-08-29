from django import template

register = template.Library()


@register.filter
def range_(number):
    """Returns range from 0 to number"""
    return range(number)
