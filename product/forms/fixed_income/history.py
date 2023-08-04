from django import forms
from product.models import FixedIncomeHistory


class FixedIncomeHistoryEditForm(forms.ModelForm):
    class Meta:
        model = FixedIncomeHistory
        fields = [
            'state',
            'date',
            'tax_and_irpf',
            'value',
        ]
