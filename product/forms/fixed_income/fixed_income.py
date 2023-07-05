from django import forms
from product.models import ProductFixedIncome


class FixedIncomeForm(forms.ModelForm):
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
