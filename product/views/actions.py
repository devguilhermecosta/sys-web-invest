from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.forms import ActionBuyAndSellForm, ActionsReceivProfitsForm
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


class ActionsManageProfitsView(ActionsView):
    def choices(self) -> tuple:
        choices = [('---', '---')]

        objects = UserAction.objects.filter(
            user=self.request.user
        )

        for user_action in objects:
            choices.append(
                (user_action.id, user_action.product.code)
            )

        return choices

    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('action-receiv-profits', None)
        form = ActionsReceivProfitsForm(session)
        form.fields.get('user_product_id').widget.choices = self.choices()

        return render(
            self.request,
            'product/pages/actions/actions_profits.html',
            context={
                'form': form,
                'form_title': 'lançar rendimento',
                'button_submit_value': 'salvar',
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['action-receiv-profits'] = post
        form = ActionsReceivProfitsForm(post)

        if form.is_valid():
            data = form.cleaned_data

            user_action = get_object_or_404(
                UserAction,
                pk=data['user_product_id'],
            )

            if user_action.user != self.request.user:
                raise Http404()

            user_action.receiv_profits(
                handler=data['profits_type'],
                date=data['date'],
                total_price=data['total_price'],
                tax_and_irpf=data.get('tax_and_irpf', ''),
            )

            del self.request.session['action-receiv-profits']

            messages.success(
                self.request,
                (
                    f'rendimento para {user_action.product.code} '
                    f'lançado com sucesso',
                )
            )

        return redirect(
            reverse('product:actions_manage_profits')
        )
