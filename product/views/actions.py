from django.http import Http404, JsonResponse
from product.forms import ActionBuyAndSellForm, ActionsReceivProfitsForm
from product.models import Action, UserAction, ActionHistory
from .base_views.variable_income import (
    BaseView,
    ListView,
    Buy,
    Sell,
    Delete,
    History,
    HistoryDelete,
    ReceiveProfits,
    ReceiveProfitsEdit,
    ReceiveProfitsDelete,
    )


class ActionsView(BaseView):
    model = UserAction
    template_path = 'product/pages/actions/actions.html'
    reverse_url_back_to_page = 'dashboard:user_dashboard'


class AllActionsView(ListView):
    model = UserAction
    template_path = 'product/pages/actions/actions_list.html'
    reverse_url_back_to_page = 'product:actions'


class ActionsDeleteView(Delete):
    model = UserAction
    reverse_url_response = 'product:actions_list'


class ActionsBuyView(Buy):
    success_response_url_redirect = 'product:actions'
    error_response_url_redirect = 'product:actions_buy'
    form = ActionBuyAndSellForm
    template_get_request = 'product/pages/actions/actions_buy.html'
    product_model = Action
    user_product_model = UserAction
    history_model = ActionHistory
    reverse_url_back_to_page = 'product:actions'


class ActionsSellView(Sell):
    success_response_url_redirect = 'product:actions'
    error_response_url_redirect = 'product:actions_sell'
    form = ActionBuyAndSellForm
    template_get_request = 'product/pages/actions/actions_sell.html'
    product_model = Action
    user_product_model = UserAction
    reverse_url_back_to_page = 'product:actions'


class ActionHistoryDetails(History):
    template_to_render_response = 'product/partials/_history_variable_income.html'  # noqa: E501
    product_model = Action
    user_product_model = UserAction
    history_model = ActionHistory
    reverse_url_back_to_page = 'product:actions_list'


class ActionsHistoryDeleteView(HistoryDelete):
    model = UserAction
    history_model = ActionHistory
    reverse_url_response = 'product:action_history'


class ActionsManageProfitsView(ReceiveProfits):
    user_product_model = UserAction
    profits_form = ActionsReceivProfitsForm
    template_path = 'product/pages/actions/actions_profits.html'
    form_custom_id = 'actions-receive-profits-form'
    reverse_url_history_profits = 'product:action_history_json'
    reverse_url_receive_profits = 'product:actions_manage_profits'
    reverse_url_total_profits = 'product:action_total_profits_json'
    reverse_url_back_to_page = 'product:actions'


class ActionsManageProfitsHistoryView(ActionsView):
    def get(self, *args, **kwargs) -> JsonResponse:
        history = UserAction.get_full_profits_history(
            user=self.request.user
        )
        return JsonResponse({'data': history})

    def post(self, *args, **kwargs) -> None:
        raise Http404()


class ActionsManageProfitsHistoryDeleteView(ReceiveProfitsDelete):
    user_product_model = UserAction
    history_model = ActionHistory
    reverse_url_success_response = 'product:actions_manage_profits'


class ActionsManageProfitsHistoryEditView(ReceiveProfitsEdit):
    user_product_model = UserAction
    history_model = ActionHistory
    profits_form = ActionsReceivProfitsForm
    template_path = 'product/pages/actions/actions_profits.html'
    reverse_url_back_to_page = 'product:actions_manage_profits'
    reverse_url_success_response = 'product:actions_manage_profits'
    reverse_url_invalid_form = 'product:action_manage_profits_edit'


class ActionsGetTotalProfitsView(ActionsView):
    def get(self, *args, **kwargs) -> JsonResponse:
        total = UserAction.get_total_profits(user=self.request.user)
        return JsonResponse({"value": total})

    def post(self, *args, **kwargs) -> None:
        raise Http404()
