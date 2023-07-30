from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from product.forms import ActionBuyAndSellForm
from product.models import Action, UserAction, ActionHistory
from .base_views.variable_income import Buy, Sell, History


login_url = '/'


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url=login_url,
    ),
    name='dispatch',
)
class ActionsView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        return render(
            self.request,
            'product/pages/actions/actions.html',
        )


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url=login_url,
    ),
    name='dispatch',
)
class AllActionsView(ListView):
    model = UserAction
    template_name = 'product/pages/actions/actions_list.html'
    ordering = ['-id']
    context_object_name = 'actions'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        user = self.request.user
        query_set = query_set.filter(user=user)

        return query_set


class ActionsBuyView(Buy):
    success_response_url_redirect = 'product:actions'
    error_response_url_redirect = 'product:actions_buy'
    form = ActionBuyAndSellForm
    template_get_request = 'product/pages/actions/actions_buy.html'
    product_model = Action
    user_product_model = UserAction
    history_model = ActionHistory


class ActionsSellView(Sell):
    success_response_url_redirect = 'product:actions'
    error_response_url_redirect = 'product:actions_sell'
    form = ActionBuyAndSellForm
    template_get_request = 'product/pages/actions/actions_sell.html'
    product_model = Action
    user_product_model = UserAction


class ActionHistoryDetails(History):
    template_to_render_response = 'product/partials/_history_variable_income.html'  # noqa: E501
    product_model = Action
    user_product_model = UserAction
    history_model = ActionHistory


class ActionManageIncomeView(ActionsView):
    ...
