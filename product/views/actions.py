from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.forms import product_forms
from product.models import Action, UserAction


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
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
        login_url='/',
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


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class ActionsBuyView(View):
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
        form = product_forms.ActionForm(session)

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
        form = product_forms.ActionForm(post)

        if form.is_valid():
            data = form.cleaned_data
            action = Action.objects.filter(code=data['code']).first()
            params = {
                'action': action,
                'quantity': int(data['quantity']),
                'unit_price': float(data['unit_price']),
                'user': self.request.user,
            }

            user_action_exists = UserAction.objects.filter(
                action=params['action'],
                user=params['user'],
            ).first()

            if user_action_exists:
                user_action_exists.buy(
                    params['quantity'], params['unit_price'],
                    )
                return self.success_response(
                    params['quantity'], params['action'].code,
                    )

            new_action = UserAction.objects.create(**params)
            new_action.save()
            return self.success_response(
                params['quantity'], params['action'].code,
                )

        return redirect(
            reverse('product:actions_buy')
        )
