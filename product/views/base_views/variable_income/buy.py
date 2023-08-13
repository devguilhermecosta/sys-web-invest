from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from product.forms import ActionBuyAndSellForm, FIIBuyForm
from .base import BaseView
from product.models import (
    Action,
    UserAction,
    ActionHistory,
    FII,
    UserFII,
    FiiHistory,
    )


class Buy(BaseView):
    success_response_url_redirect: str = ''
    error_response_url_redirect: str = ''
    form: ActionBuyAndSellForm | FIIBuyForm = ''
    template_get_request: str = ''
    product_model: Action | FII = ''
    user_product_model: UserAction | UserFII = ''
    history_model: ActionHistory | FiiHistory = ''
    reverse_url_back_to_page: str = ''

    def success_response(self, qty: int, code: str) -> HttpResponseRedirect:
        messages.success(
            self.request,
            (
                f'compra de {qty} unidade(s) de {code.upper()} '
                'realizada com sucesso'
            )
        )
        del self.request.session['handler-buy']
        return redirect(
            reverse(self.success_response_url_redirect)
        )

    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('handler-buy', None)
        form = self.form(session)

        return render(
            self.request,
            self.template_get_request,
            context={
                'form': form,
                'button_submit_value': 'comprar',
                'back_to_page': reverse(self.reverse_url_back_to_page),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['handler-buy'] = post
        form = self.form(
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
            product = self.product_model.objects.filter(
                code=data['code']
                ).first()

            user_product = self.user_product_model.objects.filter(
                product=product,
                user=user,
                ).first()

            if not user_product:
                user_product = self.user_product_model.objects.create(
                    user=user,
                    product=product,
                    )
                user_product.save()

            user_product.buy(trading_note=trading_note, **params)

            return self.success_response(
                qty=params['quantity'], code=product.code,
                )

        return redirect(
            reverse(self.error_response_url_redirect)
        )
