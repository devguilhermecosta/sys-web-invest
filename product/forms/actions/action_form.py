from django import forms
from utils.forms.style import add_css_class
from django.core.exceptions import ValidationError
from product.models import Action


default_input_class = 'C-login_input'


class ActionBuyAndSellForm(forms.Form):
    code = forms.CharField(
        label='código',
        widget=forms.TextInput()
    )

    quantity = forms.CharField(
        label='quantidade',
        widget=forms.NumberInput()
    )

    unit_price = forms.FloatField(
        label='valor unitário',
    )

    date = forms.DateField(
        label='data',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )

    trading_note = forms.FileField(
        label='',
        required=False,
        widget=forms.FileInput(
            attrs={
                'accept': 'application/pdf',
                'class': 'custom-input-file',
            },
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.items():
            if field[0] == 'trading_note':
                continue
            field[1].required = False
            add_css_class(field[1], default_input_class)

    def clean_code(self):
        code = self.cleaned_data["code"]
        action = Action.objects.filter(code=code).exists()

        if not code or code == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )

        if code[-1] == 'f' or code[-1] == 'F':
            raise ValidationError(
                (
                    'Não use o código do mercado fracionário. '
                    'Remova a letra "F"'
                ),
                code='invalid',
            )

        if len(code) < 5 or len(code) > 6:
            raise ValidationError(
                ('O código deve ter entre 5 e 6 caracteres'),
                code='invalid',
            )

        if not action:
            raise ValidationError(
                (f'Código {code.upper()} não encontrado'),
                code='invalid',
            )
        return str(code).lower()

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]

        if not quantity or quantity == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )

        if int(quantity) <= 0:
            raise ValidationError(
                ('A quantidade deve ser maior que zero'),
                code='invallid',
            )
        return quantity

    def clean_unit_price(self):
        unit_price = self.cleaned_data["unit_price"]

        if not unit_price or unit_price == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )

        if float(unit_price) <= 0:
            raise ValidationError(
                ('O valor deve ser maior que zero'),
                code='invallid',
            )

        str(unit_price).replace(',', '.')
        return float(unit_price)

    def clean_date(self):
        date = self.cleaned_data["date"]

        if not date or date == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )

        return date
