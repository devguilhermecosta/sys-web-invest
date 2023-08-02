from django import forms
from django.core.exceptions import ValidationError
from utils.forms.style import add_css_class
from datetime import date as dt
import re


default_input_class = 'C-login_input'


class FIIReceiptProfitsForm(forms.Form):
    userproduct = forms.CharField(
        label='fii',
        widget=forms.Select()
    )
    date = forms.DateField(
        label='data',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        ),
        input_formats=['%Y-%m-%d']
    )
    total_price = forms.FloatField(
        label='valor',
        widget=forms.NumberInput(
            {
                'min': 1,
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.items():
            field[1].required = False
            add_css_class(field[1], default_input_class)

    def clean_userproduct(self):
        userproduct = self.cleaned_data["userproduct"]

        if not userproduct or userproduct == '---':
            raise ValidationError(
                ('Selecione um produto'),
                code='required',
            )

        return userproduct

    def clean_date(self):
        date = self.cleaned_data["date"]

        regex_date = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')

        if not date:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )

        if not regex_date.match(dt.strftime(date, '%Y-%m-%d')):
            raise ValidationError(
                ('Informe uma data válida'),
                code='invalid'
            )

        return date

    def clean_total_price(self):
        total_price = self.cleaned_data["total_price"]

        if not total_price:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )

        if total_price <= 0:
            raise ValueError(
                ('O valor deve ser maior que zero'),
                code='invalid',
            )
        return total_price
