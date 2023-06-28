from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
    )
from django.http import Http404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.forms import ActionBuyAndSellForm
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
        form = ActionBuyAndSellForm(session)

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
        form = ActionBuyAndSellForm(
            data=post or None,
            files=self.request.FILES or None,
            )

        if form.is_valid():
            data = form.cleaned_data
            params = {
                'quantity': int(data['quantity']),
                'unit_price': float(data['unit_price']),
                'date': data['date'],
            }
            trading_note = data.get('trading_note', None)
            user = self.request.user
            action = Action.objects.filter(code=data['code']).first()

            user_action_exists = UserAction.objects.filter(
                action=action,
                user=user,
            ).first()

            if user_action_exists:
                user_action_exists.buy(trading_note=trading_note, **params)
                return self.success_response(
                    qty=params['quantity'], code=action.code,
                    )

            new_useraction = UserAction.objects.create(
                user=user,
                action=action,
                **params,
                )
            new_useraction.save()

            action_history = ActionHistory.objects.create(
                useraction=new_useraction,
                handler='buy',
                total_price=params['quantity'] * params['unit_price'],
                trading_note=trading_note,
                **params,
            )
            action_history.save()

            return self.success_response(
                qty=params['quantity'], code=action.code,
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
        form = ActionBuyAndSellForm(session)

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
        form = ActionBuyAndSellForm(
            data=post or None,
            files=self.request.FILES or None,
            )

        if form.is_valid():
            data = form.cleaned_data
            user = self.request.user
            params = {
                'quantity': int(data['quantity']),
                'unit_price': float(data['unit_price']),
                'date': data['date'],
                'trading_note': data.get('trading_note', None),
            }
            action = Action.objects.filter(code=data['code']).first()

            user_action_exists = UserAction.objects.filter(
                user=user,
                action=action
            ).first()

            if user_action_exists:
                try:
                    user_action_exists.sell(**params)
                    return self.success_response(
                        qty=params['quantity'], code=data['code']
                        )
                except ValidationError:
                    messages.error(
                        self.request,
                        (
                            'Quantidade insuficiente para venda. '
                            f'Você possui {user_action_exists.quantity} '
                            'unidade(s) em seu portifólio e está tentando '
                            f'vender {params["quantity"]}.'
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


class ActionHistoryDetails(ActionsView):
    def get(self, *args, **kwargs) -> HttpResponse:
        action = get_object_or_404(
            Action,
            code=kwargs.get('code', None)
        )

        user_action = get_object_or_404(
            UserAction,
            user=self.request.user,
            action=action,
        )

        if user_action:
            action_history = ActionHistory.objects.filter(
                useraction=user_action,
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
