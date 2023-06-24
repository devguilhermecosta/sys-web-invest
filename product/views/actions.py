from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.forms import ActionSellForm, ActionBuyForm
from product.models import Action, UserAction, ActionHistory
from django.core.exceptions import ValidationError


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


class ActionsBuyView(ActionsView):
    def success_response(self, qty: int, code: str) -> HttpResponseRedirect:
        messages.success(
            self.request,
            (
                f'compra de {qty} unidade(s) de {code.upper()} '
                'realizada com sucesso'
            )
        )

        del self.request.session['action-buy']

        return redirect(
            reverse('product:actions')
        )

    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('action-buy', None)
        form = ActionBuyForm(session)

        return render(
            self.request,
            'product/pages/actions/actions_buy.html',
            context={
                'form': form,
                'button_submit_value': 'comprar',
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['action-buy'] = post
        form = ActionBuyForm(
            data=post or None,
            files=self.request.FILES or None,
            )

        if form.is_valid():
            data = form.cleaned_data
            action = Action.objects.filter(code=data['code']).first()
            user = self.request.user
            params = {
                'quantity': int(data['quantity']),
                'unit_price': float(data['unit_price']),
                'date': data['date'],
                'trading_note': data.get('trading_note', None),
            }

            user_action_exists = UserAction.objects.filter(
                action=action,
                user=user,
            ).first()

            if user_action_exists:
                user_action_exists.buy(**params)
                return self.success_response(
                    params['quantity'], action.code,
                    )

            new_action = UserAction.objects.create(
                **params,
            )
            new_action.save()
            action_history = ActionHistory.objects.create(
                useraction=new_action,
                handler='buy',
                total_price=params['quantity']*params['unit_price'],
                **params,
            )
            action_history.save()
            return self.success_response(
                params['quantity'], params['action'].code,
                )

        return redirect(
            reverse('product:actions_buy')
        )


class ActionsSellView(ActionsView):
    def success_response(self, qty: int, code: str) -> HttpResponseRedirect:
        messages.success(
            self.request,
            (
                f'venda de {qty} unidade(s) de {code.upper()} '
                'realizada com sucesso'
            )
        )
        del self.request.session['action-sell']
        return redirect(
            reverse('product:actions')
        )

    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('action-sell', None)
        form = ActionSellForm(session)

        return render(
            self.request,
            'product/pages/actions/actions_sell.html',
            context={
                'form': form,
                'button_submit_value': 'vender',
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['action-sell'] = post
        form = ActionSellForm(post)

        if form.is_valid():
            data = form.cleaned_data
            code = data['code']
            quantity = int(data['quantity'])
            user = self.request.user

            action = Action.objects.filter(code=code).first()
            user_action_exists = UserAction.objects.filter(
                user=user,
                action=action
            ).first()

            if user_action_exists:
                try:
                    user_action_exists.sell(quantity=quantity)
                    return self.success_response(quantity, code)
                except ValidationError:
                    messages.error(
                        self.request,
                        (
                            'Quantidade insuficiente para venda. '
                            f'Você possui {user_action_exists.quantity} '
                            'unidade(s) em seu portifólio e está tentando '
                            f'vender {quantity}.'
                        ),
                    )
                    return redirect(
                        reverse('product:actions_sell')
                        )

            del self.request.session['action-sell']
            messages.error(
                self.request,
                'Você não possui esta ação em seu portifólio',
            )

        return redirect(
            reverse('product:actions_sell')
            )
