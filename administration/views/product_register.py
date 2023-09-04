from product.models import FII, Action
from administration.forms import FIIRegisterForm, ActionRegisterForm
from .base_view import Register, AutoRegister


class FIIRegister(Register):
    model = FII
    form = FIIRegisterForm
    form_title = 'Registrar novo FII'
    success_message = 'FII criado com sucesso'
    reverse_url_redirect_response = 'admin:fii_register'
    reverse_url_obj_auto_register = 'admin:fii_auto_register'


class ActionRegister(Register):
    model = Action
    form = ActionRegisterForm
    form_title = 'Registrar nova Ação'
    success_message = 'Ação criada com sucesso'
    reverse_url_redirect_response = 'admin:action_register'
    reverse_url_obj_auto_register = 'admin:action_auto_register'


class ActionAutoRegister(AutoRegister):
    model = Action
    reverse_url_redirect_response = 'admin:action_register'


class FIIAutoRegister(AutoRegister):
    model = FII
    reverse_url_redirect_response = 'admin:fii_register'
