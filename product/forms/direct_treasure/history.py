from django import forms
from product.models import DirectTreasureHistory
from product.forms.fixed_income import FixedIncomeHistoryEditForm


class DirectTreasureHistoryForm(FixedIncomeHistoryEditForm):
    class Meta:
        model = DirectTreasureHistory
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
