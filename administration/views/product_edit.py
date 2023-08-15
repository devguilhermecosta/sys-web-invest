from .base_view import Edit
from product.models import Action, FII
from administration.forms import ActionRegisterForm, FIIRegisterForm


class ActionEdit(Edit):
    model = Action
    form = ActionRegisterForm
    reverse_url_success_response = 'admin:action_register'
    reverse_url_invalid_form = 'admin:action_edit'
    reverse_url_back_to_page = 'admin:action_register'


class FIIEdit(Edit):
    model = FII
    form = FIIRegisterForm
    reverse_url_success_response = 'admin:action_register'
    reverse_url_invalid_form = 'admin:action_edit'
    reverse_url_back_to_page = 'admin:action_register'
