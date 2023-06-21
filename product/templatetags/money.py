from django import template


register = template.Library()


@register.filter('real_brl')
def real_brl(value):
    return (f'R$ {value:.2f}').replace('.', ',')
