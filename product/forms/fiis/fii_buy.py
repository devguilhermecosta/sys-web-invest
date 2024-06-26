from django.core.exceptions import ValidationError
from product.forms.actions.action_form import ActionBuyAndSellForm
from product.models import FII


default_input_class = 'C-login_input'


class FIIBuyForm(ActionBuyAndSellForm):
    def clean_code(self):
        code = self.cleaned_data["code"]
        fii = FII.objects.filter(code=str(code).lower()).exists()

        if not code or code == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required'
            )

        if len(code) < 6 or len(code) > 8:
            raise ValidationError(
                ('O código deve ter entre 6 e 8 caracteres'),
                code='invalid',
            )

        if not fii:
            raise ValidationError(
                (f'Código {code.upper()} não encontrado'),
                code='invalid',
            )

        return str(code).lower()
