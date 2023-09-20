from .base_view import Update
from product.models import Action, FII
from administration.forms import ActionRegisterForm, FIIRegisterForm


class ActionUpdate(Update):
    model = Action
    form = ActionRegisterForm
    reverse_url_success_response = 'admin:action_register'
    reverse_url_invalid_form = 'admin:action_edit'
    reverse_url_back_to_page = 'admin:action_register'


class FIIUpdate(Update):
    model = FII
    form = FIIRegisterForm
    reverse_url_success_response = 'admin:fii_register'
    reverse_url_invalid_form = 'admin:fii_edit'
    reverse_url_back_to_page = 'admin:fii_register'
