from django import template

register = template.Library()


@register.filter
def range_(number):
    return range(number)
