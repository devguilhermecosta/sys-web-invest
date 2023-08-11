from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from product.forms import ActionBuyAndSellForm, FIIBuyForm
from product.models import (
    Action,
    UserAction,
    FII,
    UserFII
    )


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class Sell(View):
    success_response_url_redirect: str = ''
    error_response_url_redirect: str = ''
    form: ActionBuyAndSellForm | FIIBuyForm = ''
    template_get_request: str = ''
    product_model: Action | FII = ''
    user_product_model: UserAction | UserFII = ''

    def success_response(self, qty: int, code: str) -> HttpResponseRedirect:
        messages.success(
            self.request,
            (
                f'venda de {qty} unidade(s) de {code.upper()} '
                'realizada com sucesso'
            )
        )
        del self.request.session['handler-sell']
        return redirect(
            reverse(self.success_response_url_redirect)
        )

    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('handler-sell', None)
        form = self.form(session)

        return render(
            self.request,
            self.template_get_request,
            context={
                'form': form,
                'button_submit_value': 'vender',
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['handler-sell'] = post
        form = self.form(
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
            product = self.product_model.objects.filter(
                code=data['code']
                ).first()

            user_product_exists = self.user_product_model.objects.filter(
                user=user,
                product=product,
            ).first()

            if user_product_exists:
                try:
                    user_product_exists.sell(**params)
                    return self.success_response(
                        qty=params['quantity'], code=data['code']
                        )
                except ValidationError:
                    messages.error(
                        self.request,
                        (
                            'Quantidade insuficiente para venda. '
                            f'Você possui {user_product_exists.get_quantity()}'
                            ' unidade(s) em seu portifólio e está tentando '
                            f'vender {params["quantity"]}.'
                        ),
                    )
                    return redirect(
                        reverse(self.error_response_url_redirect)
                        )

            del self.request.session['handler-sell']
            messages.error(
                self.request,
                (
                    f'Você não possui o produto {product.code.upper()} '
                    'em seu portifólio'
                    ),
            )

        return redirect(
            reverse(self.error_response_url_redirect)
            )
