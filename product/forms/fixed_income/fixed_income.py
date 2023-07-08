from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from product.models import ProductFixedIncome
from utils.forms.style import add_css_class


default_input_class = 'C-login_input'
date_field_formats = [
    '%Y-%m-%d',
    '%Y/%m/%d',
    '%d-%m-%Y',
    '%d/%m/%Y',
    ]


class FixedIncomeRegisterForm(forms.ModelForm):
    category = forms.CharField(
        label='categoria',
        widget=forms.Select(
            choices=(
                ('cdb', 'cdb'),
                ('cra', 'cra'),
                ('cri', 'cri'),
                ('lc', 'lc'),
                ('lci', 'lci'),
                ('lca', 'lca'),
                ('lf', 'lf'),
                ('lfsn', 'lfsn'),
                ('debêntures', 'debêntures'),
            )
        )
    )

    grace_period = forms.DateField(
        label='carência',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }
        ),
        input_formats=date_field_formats,
    )

    maturity_date = forms.DateField(
        label='vencimento',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }
        ),
        input_formats=date_field_formats,
    )

    liquidity = forms.CharField(
        label='liquidez',
        widget=forms.Select(
            choices=(
                ('no vencimento', 'no vencimento'),
                ('diária', 'diária'),
                ('30 dias', '30 dias'),
                ('30 dias +', '30 dias +'),
                ('30 dias -', '30 dias -'),
            )
        )
    )

    interest_receipt = forms.CharField(
        label='pagamento de juros',
        widget=forms.Select(
            choices=(
                ('não há', 'não há'),
                ('mensal', 'mensal'),
                ('trimestral', 'trimestral'),
                ('semestral', 'semestral'),
                ('anual', 'anual'),
            )
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.items():
            field[1].required = False
            add_css_class(field[1], default_input_class)

    class Meta:
        model = ProductFixedIncome
        fields = [
            'category',
            'name',
            'value',
            'grace_period',
            'maturity_date',
            'liquidity',
            'profitability',
            'interest_receipt',
            'description',
        ]

        labels = {
            'name': 'nome',
            'value': 'valor',
            'profitability': 'rentabilidade',
            'description': 'observações',
        }

    def clean(self) -> Dict[str, Any]:
        data = self.cleaned_data

        for key, value in data.items():
            if key == 'description':
                continue
            else:
                if not value or value == '':
                    raise ValidationError(
                        {
                            key: 'Campo obrigatório',
                        },
                        code='required',
                    )

        return super().clean()


class FixedIncomeEditForm(FixedIncomeRegisterForm):
    value = forms.FloatField(
        required=False,
        label='valor',
        help_text=(
            'O valor não pode ser alterado por aqui. '
            'Altere através da Aplicação e Regaste.'),
        widget=forms.NumberInput(
            attrs={
                'readonly': 'readonly',
            }
        )
    )
    add_css_class(value, default_input_class)
