from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from product.models import Action, FII
from utils.forms.style import add_css_class


default_input_class = 'C-login_input'


class ActionEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.items():
            field[1].required = False
            add_css_class(field[1], default_input_class)

    class Meta:
        model = Action
        fields = [
            'id',
            'code',
            'description',
            'cnpj',
        ]

    def clean_code(self) -> Dict[str, Any]:
        code = self.cleaned_data['code']
        pk = self.fields.get('id')
        i_code = Action.objects.filter(code=code).first()
        for key, value in self.fields.items():
            print(key, value)

        if i_code and i_code.id != pk and i_code.code == code:
            raise ValidationError(
                ('Este código já está em uso'),
                code='invalid'
                )
        return code


class FIIEditForm(ActionEditForm):
    class Meta:
        model = FII
        fields = [
            'code',
            'description',
            'cnpj',
        ]
