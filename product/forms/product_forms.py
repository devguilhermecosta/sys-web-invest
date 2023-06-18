from django import forms
from utils.forms.style import add_css_class
from django.core.exceptions import ValidationError
from product.models import Action


class ActionForm(forms.Form):
    code = forms.CharField(
        label='código',
        required=False,
        widget=forms.TextInput()
    )
    add_css_class(code, 'C-login_input')

    quantity = forms.CharField(
        label='quantidade',
        required=False,
        widget=forms.NumberInput()
    )
    add_css_class(quantity, 'C-login_input')

    unit_price = forms.FloatField(
        label='valor unitário',
        required=False,
    )
    add_css_class(unit_price, 'C-login_input')

    def clean_code(self):
        code = self.cleaned_data["code"]
        action = Action.objects.filter(code=code).exists()

        if not code or code == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )

        if code[-1] == 'f' or code[-1] == 'F':
            raise ValidationError(
                (
                    'Não use o código do mercado fracionário. '
                    'Remova a letra "F"'
                ),
                code='invalid',
            )

        if len(code) < 5 or len(code) > 5:
            raise ValidationError(
                ('O código deve ter 5 caracteres'),
                code='invalid',
            )

        if not action:
            raise ValidationError(
                (f'Código {code.upper()} não encontrado'),
                code='invalid',
            )

        return code

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]

        if not quantity or quantity == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )

        if int(quantity) <= 0:
            raise ValidationError(
                ('A quantidade deve ser maior que zero'),
                code='invallid',
            )

        return quantity

    def clean_unit_price(self):
        unit_price = self.cleaned_data["unit_price"]

        if unit_price == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )

        if unit_price <= 0:
            raise ValidationError(
                ('O valor deve ser maior que zero'),
                code='invallid',
            )

        return str(unit_price).replace(',', '.')
