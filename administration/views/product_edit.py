from .base_view import Edit
from product.models import Action
from administration.forms import ActionEditForm


class ActionEdit(Edit):
    model = Action
    form = ActionEditForm
    reverse_url_success_response = 'admin:action_register'
    reverse_url_invalid_form = 'admin:action_edit'
    reverse_url_back_to_page = 'admin:action_register'
