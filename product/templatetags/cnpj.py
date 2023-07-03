from django import template
import c2validator as c2


register = template.Library()


@register.filter('fomated_cnpj')
def fomated_cnpj(value):
    cnpj = c2.validate(value)
    if cnpj.is_valid():
        return cnpj.formatted(punctuation=True)
    return value
