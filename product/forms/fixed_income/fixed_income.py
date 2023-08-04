from django import forms
from django.core.exceptions import ValidationError
from product.models import ProductFixedIncome
from utils.forms.style import add_css_class


default_input_class = 'C-login_input'


class FixedIncomeRegisterForm(forms.ModelForm):
    value = forms.FloatField(
        label='valor',
        required=False,
        widget=forms.NumberInput(
            attrs={
                'min': 0,
                'step': 0.00,
            }
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
            'grace_period',
            'maturity_date',
            'liquidity',
            'profitability',
            'interest_receipt',
            'description',
        ]

        labels = {
            'category': 'categoria',
            'name': 'nome',
            'grace_period': 'carência',
            'maturity_date': 'vencimento',
            'profitability': 'rentabilidade',
            'liquidity': 'liquidez',
            'description': 'observações',
            'interest_receipt': 'pagamento de juros',
        }

        widgets = {
            'grace_period': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    }
                ),
            'maturity_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    }
                ),
            }

    def clean_category(self):
        category = self.cleaned_data["category"]

        if not category or category == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='invalid',
            )
        return category

    def clean_name(self):
        name = self.cleaned_data["name"]

        if not name or name == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='invalid',
            )
        return name

    def clean_value(self):
        value = self.cleaned_data["value"]

        if not value or value == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='invalid',
            )
        return value

    def clean_grace_period(self):
        grace_period = self.cleaned_data["grace_period"]

        if not grace_period or grace_period == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='invalid',
            )
        return grace_period

    def clean_maturity_date(self):
        maturity_date = self.cleaned_data["maturity_date"]

        if not maturity_date or maturity_date == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='invalid',
            )
        return maturity_date

    def clean_liquidity(self):
        liquidity = self.cleaned_data["liquidity"]

        if not liquidity or liquidity == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='invalid',
            )
        return liquidity

    def clean_profitability(self):
        profitability = self.cleaned_data["profitability"]

        if not profitability or profitability == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='invalid',
            )
        return profitability

    def clean_interest_receipt(self):
        interest_receipt = self.cleaned_data["interest_receipt"]

        if not interest_receipt or interest_receipt == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='invalid',
            )
        return interest_receipt


class FixedIncomeEditForm(FixedIncomeRegisterForm):
    value = forms.CharField(
        label='',
        widget=forms.HiddenInput(),
    )
    add_css_class(value, default_input_class)

    def clean_value(self):
        value = self.cleaned_data["value"]
        if not value:
            return


class FixedIncomeApplyRedeemForm(forms.Form):
    value = forms.FloatField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                'min': 1,
                'placeholder': 'valor',
            }
        )
    )
    add_css_class(value, 'C-fixed_income_input')

    date = forms.DateField(
        required=False,
        label='data',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            },
        )
    )
    add_css_class(date, 'C-fixed_income_input')

    def clean_value(self):
        value = self.cleaned_data["value"]

        if not value or value == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )

        if value <= 0:
            raise ValidationError(
                ('O valor deve ser maior do que zero.'),
                code='invalid',
            )

        return value


class FixedIncomeProfitsReceivForm(forms.Form):
    date = forms.DateField(
        required=False,
        label='data',
        widget=forms.DateInput(
            format='%Y-%m-%d',
            attrs={
                'type': 'date',
            }
        )
    )
    value = forms.FloatField(
        required=False,
        label='valor bruto',
        widget=forms.NumberInput(
            attrs={
                'min': 0,
            }
        )
    )
    tax_and_irpf = forms.FloatField(
        required=False,
        label='taxas e impostos',
        widget=forms.NumberInput(
            attrs={
                'min': 0,
                'step': 0.01,
            }
        )
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.items():
            field[1].required = False
            add_css_class(field[1], default_input_class)

    def clean_date(self):
        date = self.cleaned_data["date"]

        if not date:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )
        return date

    def clean_value(self):
        value = self.cleaned_data["value"]

        if not value:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )

        if not isinstance(value, float):
            raise ValidationError(
                ('Digite somente números'),
                code='invalid',
            )

        return value

    def clean_tax_and_irpf(self):
        tax_and_irpf = self.cleaned_data["tax_and_irpf"]

        if tax_and_irpf:
            if not isinstance(tax_and_irpf, float):
                raise ValidationError(
                    ('Digite somente números'),
                    code='invalid'
                )

        return tax_and_irpf if tax_and_irpf else 0
