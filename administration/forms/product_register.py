from django import forms
from django.core.exceptions import ValidationError
from product.models import FII, Action
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

        return str(code).lower()

    def clean_description(self):
        description = self.cleaned_data["description"]

        if not description or len(description) < 3:
            raise ValidationError(
                ('A descrição deve ter pelo menos 3 caracteres'),
                code='invalid'
            )
        return str(description).lower()

    def clean_cnpj(self):
        cnpj = c2.validate(self.cleaned_data['cnpj'])

        if not cnpj.is_valid():
            raise ValidationError(
                ('CNPJ inválido'),
                code='invalid',
            )

        fii_e = FII.objects.filter(cnpj=cnpj.formatted(punctuation=True))

        if fii_e.exists():
            raise ValidationError(
                ('Este CNPJ já está em uso'),
                code='unique',
            )

        return cnpj.formatted(punctuation=True)


class ActionRegisterForm(FIIRegisterForm):
    class Meta:
        model = Action
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

        if not code or len(code) < 5 or len(code) > 6:
            raise ValidationError(
                ('O código deve ter entre 5 e 6 caracteres'),
                code='invalid'
            )

        return str(code).lower()

    def clean_cnpj(self):
        cnpj = c2.validate(self.cleaned_data['cnpj'])

        if not cnpj.is_valid():
            raise ValidationError(
                ('CNPJ inválido'),
                code='invalid',
            )

        action_e = Action.objects.filter(
            cnpj=cnpj.formatted(punctuation=True)
            )

        if action_e.exists():
            raise ValidationError(
                ('Este CNPJ já está em uso'),
                code='unique',
            )

        return cnpj.formatted(punctuation=True)
