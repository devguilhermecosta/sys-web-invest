from django import forms
from django.core.exceptions import ValidationError
from product.models import FII
from utils.forms.style import add_css_class
import c2validator as c2


default_input_class = 'C-login_input'


class FIIRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.items():
            field[1].required = False
            add_css_class(field[1], default_input_class)

    class Meta:
        model = FII
        fields = [
            'code',
            'description',
            'cnpj',
        ]

        labels = {
            'code': 'código',
            'description': 'descrição',
            'cnpj': 'cnpj',
        }

    def clean_code(self):
        code = self.cleaned_data["code"]

        if not code or len(code) != 6:
            raise ValidationError(
                ('O código deve ter 6 caracteres'),
                code='invalid'
            )

        product = FII.objects.filter(code=code)

        if product.exists():
            raise ValidationError(
                ('FII já registrado'),
                code='invalid'
            )

        return code

    def clean_description(self):
        description = self.cleaned_data["description"]

        if not description or len(description) < 6:
            raise ValidationError(
                ('A descrição deve ter pelo menos 6 caracteres'),
                code='invalid'
            )
        return description

    def clean_cnpj(self):
        cnpj = self.cleaned_data["cnpj"]
        validate_cnpj = c2.validate(cnpj)

        if not cnpj:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )

        if not validate_cnpj.is_valid():
            raise ValidationError(
                ('Cnpj inválido'),
                code='invalid'
            )

        cpf_valid = validate_cnpj.formatted(punctuation=True)
        product = FII.objects.filter(
            cnpj=cpf_valid
        )

        if product.exists():
            raise ValidationError(
                ('CNPJ já registrado'),
                code='invalid'
            )

        return cpf_valid