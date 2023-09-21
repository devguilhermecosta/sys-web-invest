from django import forms
from django.core.exceptions import ValidationError
from improvement.models import Improvement
from utils.forms.style import add_css_class


class ImprovementManagerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for field in self.fields.items():
            field[1].required = False
            add_css_class(field[1], 'C-login_input')

    class Meta:
        model = Improvement
        fields = [
            'status',
        ]

        labels = {
            'status': '',
        }

    def clean_status(self):
        status = self.cleaned_data["status"]

        if not status or status == '':
            raise ValidationError(
                ('campo obrigatório'),
                code='required',
            )

        return status
