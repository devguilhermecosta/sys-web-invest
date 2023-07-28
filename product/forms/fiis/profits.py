from django import forms
from django.core.exceptions import ValidationError
from utils.forms.style import add_css_class
from product.models import UserFII

default_input_class = 'C-login_input'


class FIIReceiptProfitsForm(forms.Form):
    user_product_id = forms.CharField(
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
    value = forms.FloatField(
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

    def clean_product(self):
        product = self.cleaned_data["product"]

        if not product:
            raise ValidationError(
                ('Selecione um produto'),
                code='required',
            )

        if not isinstance(product, UserFII):
            raise ValidationError(
                ('O produto deve ser um FII'),
                code='invalid',
            )

        return product

    def clean_date(self):
        date = self.cleaned_data["date"]

        if not date:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )
        return date

    def clean_value(self):
        value = self.cleaned_data["value"]

        if not value:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )

        if value <= 0:
            raise ValueError(
                ('O valor deve ser maior que zero'),
                code='invalid',
            )
        return value
