from django import forms
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
            'code',
            'description',
            'cnpj',
        ]


class FIIEditForm(ActionEditForm):
    class Meta:
        model = FII
        fields = [
            'code',
            'description',
            'cnpj',
        ]
