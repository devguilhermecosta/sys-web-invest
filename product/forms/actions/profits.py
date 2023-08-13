from django import forms
from django.core.exceptions import ValidationError
from utils.forms.style import add_css_class
from datetime import date as dt
import re


default_input_class = 'C-login_input'

profitys_type_choices = (
    ('---', '---'),
    ('dividends', 'dividendos'),
    ('jscp', 'jscp'),
    ('remuneration', 'remuneração'),
    ('renting', 'aluguel'),
)


class ActionsReceivProfitsForm(forms.Form):
    userproduct = forms.CharField(
        label='ação',
        max_length=255,
        widget=forms.Select()
    )
    handler = forms.CharField(
        label='tipo de rendimento',
        max_length=255,
        widget=forms.Select(
            choices=profitys_type_choices
        )
    )
    date = forms.DateField(
        label='data',
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            },
            format='%Y-%m-%d',
        )
    )
    tax_and_irpf = forms.FloatField(
        label='taxas e irpf',
        widget=forms.NumberInput(
            attrs={
                'min': 0,
                'step': 0.01,
            }
        )
    )
    unit_price = forms.FloatField(
        label='valor bruto',
        widget=forms.NumberInput(
            attrs={
                'min': 0.01,
                'step': 0.01,
            }
        )
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.items():
            add_css_class(field[1], default_input_class)
            field[1].required = False

    def clean_userproduct(self):
        userproduct = self.cleaned_data["userproduct"]

        if not userproduct or userproduct == '---':
            raise ValidationError(
                ('selecione uma ação'),
                code='required',
                )

        userproduct = int(userproduct)

        if not isinstance(userproduct, int):
            raise ValidationError(
                ('selecione uma ação'),
                code='invalid',
                )

        return userproduct

    def clean_handler(self):
        handler = self.cleaned_data["handler"]

        if not handler or handler == '---':
            raise ValidationError(
                ('selecione um tipo de rendimento'),
                code='required',
                )

        return handler

    def clean_date(self):
        date = self.cleaned_data["date"]
        regex_date = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')

        if not date:
            raise ValidationError(
                ('campo obrigatório'),
                code='required',
                )

        if not regex_date.match(dt.strftime(date, '%Y-%m-%d')):
            raise ValidationError(
                ('informe uma data válida'),
                code='invalid',
                )
        return date

    def clean_tax_and_irpf(self):
        tax_and_irpf = self.cleaned_data["tax_and_irpf"]

        if tax_and_irpf:
            if not isinstance(tax_and_irpf, (int, float)):
                raise ValidationError(
                    ('digite somente números'),
                    code='required',
                    )

        return tax_and_irpf if tax_and_irpf else 0

    def clean_total_price(self):
        total_price = self.cleaned_data["total_price"]

        if not total_price:
            raise ValidationError(
                ('campo obrigatório'),
                code='required',
                )

        if not isinstance(total_price, (int, float)):
            raise ValidationError(
                ('digite somente números'),
                code='required',
                )
        return total_price
