from django import forms
from improvement.models import Improvement


class ImprovementManagerForm(forms.ModelForm):
    class Meta:
        model = Improvement
        fields = [
            'id',
            'user',
            'title',
            'description',
            'status',
        ]

        labels = {
            'user': 'usuário',
            'title': 'título',
            'description': 'descrição',
            'status': 'status',
        }
