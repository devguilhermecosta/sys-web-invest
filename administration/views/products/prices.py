from .base_view import UpdateLastClose
from product.models import Action, FII


class ActionsUpdateLastCloseView(UpdateLastClose):
    model = Action
    reverse_url_response = 'admin:update_actions_prices'


class FIIsUpdateLastCloseView(UpdateLastClose):
    model = FII
    reverse_url_response = 'admin:update_fiis_prices'
