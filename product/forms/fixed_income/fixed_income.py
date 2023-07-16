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
