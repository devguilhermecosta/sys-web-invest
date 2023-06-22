from django.core.exceptions import ValidationError
from product.forms.actions.action_buy import ActionBuyForm
from product.models import FIIS


default_input_class = 'C-login_input'


class FIIBuyForm(ActionBuyForm):
    def clean_code(self):
        code = self.cleaned_data["code"]
        fii = FIIS.objects.filter(code=code).exists()

        if not code or code == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )

        if len(code) != 6:
            raise ValidationError(
                ('O código deve ter 6 caracteres'),
                code='invalid',
            )

        if not fii:
            raise ValidationError(
                (f'Código {code.upper()} não encontrado'),
                code='invalid',
            )

        return str(code).lower()
