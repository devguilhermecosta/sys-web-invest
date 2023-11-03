from django.views import View
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from product.models import Action, FII
from decimal import Decimal
from requests.exceptions import HTTPError
from typing import Dict
import yfinance as yf
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

    def get_ticker(self, symbol: str) -> yf.Ticker:
        ticker = yf.Ticker(symbol)
        return ticker

    def previous_close(self, symbol: str) -> Decimal | None:
        try:
            product = self.get_ticker(f'{symbol}.sa')
            previous_close = product.fast_info.get('previousClose', 0)
            return Decimal(previous_close)
        except HTTPError:
            return None

    def get(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user

        if not user.is_staff:
            raise Http404()

        return render(
            self.request,
            self.template_name,
            context={
                'url_update': reverse(self.reverse_url_response),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user

        if not user.is_staff:
            raise Http404()

        up = self.update_all()

        if up['error_list']:
            messages.error(
                self.request,
                up['message_f'],
            )

            return redirect(
                reverse(self.reverse_url_response)
                )

        messages.success(
            self.request,
            up['message_f'],
        )

        return redirect(
            reverse(self.reverse_url_response)
            )

    def update_all(self) -> Dict[str, str]:
        ''' return dict with attrs: message_f, error_list '''
        upgrade = 0
        not_upgrade = 0
        list_not_updagre = []

        for p in self.model.objects.all():
            previous_close = self.previous_close(p.code)

            if previous_close:
                p.update_last_close(previous_close)
                upgrade += 1

            else:
                not_upgrade += 1
                list_not_updagre.append(p)

        message = (
            f'{upgrade} ativo(s) foram atualizados. '
            f'{not_upgrade} ativo(s) não puderam ser atualizados. '
            'Ativos que não foram atualizados: '
            f'{[a for a in list_not_updagre]}. '
        ),

        message_f = re.sub(r"[()']", '', str(message))

        return {
            'message_f': message_f,
            'error_list':  'alguns ativos não foram atualizados',
        }
