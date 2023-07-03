from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from product.forms import ActionBuyAndSellForm
from product.models import Action, UserAction, ActionHistory
from .base_views.variable_income import Buy, Sell


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


class ActionHistoryDetails(ActionsView):
    def get(self, *args, **kwargs) -> HttpResponse:
        action = get_object_or_404(
            Action,
            code=kwargs.get('code', None)
        )

        user_action = get_object_or_404(
            UserAction,
            user=self.request.user,
            product=action,
        )

        if user_action:
            action_history = ActionHistory.objects.filter(
                userproduct=user_action,
            ).order_by('-date')
        else:
            raise Http404()

        return render(
            self.request,
            'product/pages/actions/actions_history.html',
            context={
                'history': action_history,
            }
        )
