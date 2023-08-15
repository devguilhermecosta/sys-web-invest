from .base_view import Delete
from product.models import (
    Action,
    FII,
    UserAction,
    UserFII
)


class ActionDelete(Delete):
    model = Action
    userproduct_model = UserAction
    reverse_url_error_response = 'admin:action_register'
    reverse_url_success_response = 'admin:action_register'


class FIIDelete(Delete):
    model = FII
    userproduct_model = UserFII
    reverse_url_error_response = 'admin:fii_register'
    reverse_url_success_response = 'admin:fii_register'
