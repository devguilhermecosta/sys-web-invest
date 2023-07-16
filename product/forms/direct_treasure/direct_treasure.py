from django import forms
from product.models import DirectTreasure
from django.core.exceptions import ValidationError
from utils.forms.style import add_css_class


default_input_class = 'C-login_input'


class DirectTreasureRegisterForm(forms.ModelForm):
    maturity_date = forms.DateField(
        label='vencimento',
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.items():
            field[1].required = False
            add_css_class(field[1], default_input_class)

    class Meta:
        model = DirectTreasure
        fields = [
            'name',
            'category',
            'interest_receipt',
            'profitability',
            'maturity_date',
            'value',
            'description',
        ]

        labels = {
            'name': 'nome',
            'category': 'categoria',
            'interest_receipt': 'recebimento de juros',
            'profitability': 'rentabilidade',
            'value': 'valor',
            'description': 'descrição',
        }

        widgets = {
            'value': forms.NumberInput(
                attrs={
                    'min': 1,
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"]

        if not name or name == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )
        return name

    def clean_category(self):
        category = self.cleaned_data["category"]

        if not category or category == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )
        return category

    def clean_interest_receipt(self):
        interest_receipt = self.cleaned_data["interest_receipt"]

        if not interest_receipt or interest_receipt == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )
        return interest_receipt

    def clean_profitability(self):
        profitability = self.cleaned_data["profitability"]

        if not profitability or profitability == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )
        return profitability

    def clean_maturity_date(self):
        maturity_date = self.cleaned_data["maturity_date"]

        if not maturity_date or maturity_date == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )
        return maturity_date

    def clean_value(self):
        value = self.cleaned_data["value"]

        if not value or value == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )
        return value
