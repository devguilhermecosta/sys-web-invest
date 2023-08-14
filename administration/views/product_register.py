from product.models import FII, Action
from administration.forms import FIIRegisterForm, ActionRegisterForm
from .base_view import Register


class FIIRegister(Register):
    model = FII
    form = FIIRegisterForm
    form_title = 'Registrar novo FII'
    success_message = 'FII criado com sucesso'
    reverse_url_redirect_response = 'admin:fii_register'


class ActionRegister(Register):
    model = Action
    form = ActionRegisterForm
    form_title = 'Registrar nova Ação'
    success_message = 'Ação criada com sucesso'
    reverse_url_redirect_response = 'admin:action_register'
