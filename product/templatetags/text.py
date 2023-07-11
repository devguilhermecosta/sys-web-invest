from django import template


register = template.Library()


@register.filter('upper')
def upper(value: str):
    return value.upper()


@register.filter('title')
def title(value: str):
    return value.title()


@register.filter('captalize')
def captalize(value: str):
    return value.capitalize()
