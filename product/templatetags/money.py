from django import template
import locale

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF8')

register = template.Library()


@register.filter('real_brl')
def real_brl(value):
    return locale.currency(value)
