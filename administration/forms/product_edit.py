from django.core.exceptions import ValidationError
from product.models import Action, FII
from .product_register import ActionRegisterForm
import c2validator as c2


default_input_class = 'C-login_input'


class ActionEditForm(ActionRegisterForm):
    class Meta:
        model = Action
        fields = [
            'code',
            'description',
            'cnpj',
        ]

    def clean_code(self):
        code = self.cleaned_data['code']

        if len(code) != 5:
            raise ValidationError(
                ('O código deve ter 5 caracteres'),
                code='invalid'
            )
        return code

    def clean_cnpj(self):
        cnpj = c2.validate(self.cleaned_data['cnpj'])

        if not cnpj.is_valid():
            raise ValidationError(
                ('CNPJ inválido'),
                code='invalid',
            )
        return cnpj.formatted(punctuation=True)


class FIIEditForm(ActionEditForm):
    class Meta:
        model = FII
        fields = [
            'code',
            'description',
            'cnpj',
        ]
