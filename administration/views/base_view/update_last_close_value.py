from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from product.models import Action, FII
from decimal import Decimal
import requests as r
import os
import re


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class UpdateLastClose(View):
    model: Action | FII
    template_name: str = 'administration/pages/update_prices.html'
    reverse_url_response: str

    def get_ticker(self, symbol: str) -> str:
        token = os.environ.get('BRAPI_API_TOKEN')
        request = r.get(f'https://brapi.dev/api/quote/{symbol}?token={token}')
        response = request.json()
        product = response.get('results')[0]
        return product

    def previous_close(self, symbol: str) -> Decimal:
        product = self.get_ticker(symbol)
        previous_close = product.get('regularMarketPreviousClose')
        return Decimal(previous_close)

    def get(self, *args, **kwargs) -> HttpResponse:
        return render(
            self.request,
            self.template_name,
            context={
                'url_update': reverse(self.reverse_url_response),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        upgrade = 0
        not_upgrade = 0
        list_not_updagre = []
        error_list = []

        for p in self.model.objects.all():
            try:
                previous_close = self.previous_close(p.code)
                p.update_last_close(previous_close)
                upgrade += 1

            except Exception as e:
                not_upgrade += 1
                list_not_updagre.append(p.code)
                error_list.append(e)

        message = (
            f'{upgrade} ativo(s) foram atualizados. '
            f'{not_upgrade} ativo(s) não puderam ser atualizados. '
            'Ativos que não foram atualizados: '
            f'{[a for a in list_not_updagre]}. '
            f'Erros: {error_list}'
        ),

        message_f = re.sub(r"[()']", '', str(message))

        if error_list:
            messages.error(
                self.request,
                message_f,
            )

            return redirect(
                reverse(self.reverse_url_response)
                )

        messages.success(
            self.request,
            message_f,
        )

        return redirect(
            reverse(self.reverse_url_response)
            )
