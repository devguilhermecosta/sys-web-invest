from django.views import View
from django.http import HttpResponse
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
            'product/pages/actions.html',
        )


class AllActionsView(View):
    ...


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class ActionsBuyView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('action-buy', None)
        form = product_forms.ActionForm(session)

        return render(
            self.request,
            'product/pages/actions_buy.html',
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
            code = self.request.POST.get('code', None)
            qty = int(self.request.POST.get('quantity', None))
            up = self.request.POST.get('unit_price', None)
            user = self.request.user
            action = Action.objects.filter(code=code).first()

            user_action = UserAction.objects.filter(
                action=action,
                user=user,
            )

            if user_action.exists():
                actual_user_action = user_action.first()
                actual_user_action.quantity += qty
                actual_user_action.unit_price = up
                actual_user_action.save()

            new_action = UserAction.objects.create(
                user=user,
                action=action,
                quantity=qty,
                unit_price=up,
            )
            new_action.save()

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

        return redirect(
            reverse('product:actions_buy')
        )
