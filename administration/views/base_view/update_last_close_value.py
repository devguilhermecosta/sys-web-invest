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
        try:
            for p in self.model.objects.all():
                previous_close = self.previous_close(p.code)
                p.update_last_close(previous_close)

            messages.success(
                self.request,
                'Preços atualizados com sucesso',
            )

        except Exception as e:
            messages.error(
                self.request,
                f'{e}: Erro ao atualizar os valores',
            )

        return redirect(
            reverse(self.reverse_url_response)
        )