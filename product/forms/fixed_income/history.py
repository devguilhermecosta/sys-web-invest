from django import forms
from django.core.exceptions import ValidationError
from product.models import FixedIncomeHistory
from utils.forms.style import add_css_class


default_input_class = 'C-login_input'


class FixedIncomeHistoryEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.items():
            field[1].required = False
            add_css_class(field[1], default_input_class)

    class Meta:
        model = FixedIncomeHistory
        fields = [
            'state',
            'date',
            'tax_and_irpf',
            'value',
        ]

        labels = {
            'state': 'movimentação',
            'date': 'data',
            'tax_and_irpf': 'taxas e impostos',
            'value': 'valor',
        }

        widgets = {
            'state': forms.Select(),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                }
            ),
        }

    def clean_state(self):
        state = self.cleaned_data["state"]

        if not state:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )
        return state

    def clean_date(self):
        date = self.cleaned_data["date"]

        if not date:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )
        return date

    def clean_tax_and_irpf(self):
        tax_and_irpf = self.cleaned_data["tax_and_irpf"]
        return tax_and_irpf if tax_and_irpf else 0

    def clean_value(self):
        value = self.cleaned_data["value"]

        if not value:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )
        return value
