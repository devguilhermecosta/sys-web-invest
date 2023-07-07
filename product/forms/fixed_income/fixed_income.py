from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from product.models import ProductFixedIncome


class FixedIncomeRegisterForm(forms.ModelForm):
    category = forms.CharField(
        required=False,
        label='categoria',
    )
    name = forms.CharField(
        required=False,
        label='nome',
    )
    value = forms.FloatField(
        required=False,
        label='valor',
    )
    grace_period = forms.CharField(
        required=False,
        label='carência',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )
    maturity_date = forms.DateField(
        required=False,
        label='vencimento',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )
    liquidity = forms.CharField(
        required=False,
        label='liquidez',
    )
    profitability = forms.CharField(
        required=False,
        label='rentabilidade',
    )
    interest_receipt = forms.CharField(
        required=False,
        label='pagamento de juros',
    )
    description = forms.CharField(
        required=False,
        label='observações',
    )

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

    def clean(self) -> Dict[str, Any]:
        data = self.cleaned_data

        for key, value in data.items():
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
        widget=forms.NumberInput(
            attrs={
                'readonly': 'readonly',
            }
        )
    )
