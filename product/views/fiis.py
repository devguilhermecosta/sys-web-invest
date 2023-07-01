from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from product.forms import FIIBuyForm
from product.models import FII, UserFII, FiiHistory


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class FIIsView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        return render(
            self.request,
            'product/pages/fiis/fiis.html',
        )


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class AllFIIsView(ListView):
    model = UserFII
    template_name = 'product/pages/fiis/fiis_list.html'
    ordering = ['-id']
    context_object_name = 'fiis'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        user = self.request.user
        query_set = query_set.filter(user=user)

        return query_set


class FIISBuyView(FIIsView):
    def success_response(self, qty: int, code: str) -> HttpResponseRedirect:
        messages.success(
            self.request,
            (
                f'compra de {qty} unidade(s) de {code.upper()} '
                'realizada com sucesso'
            )
        )
        del self.request.session['fiis-buy']
        return redirect(
            reverse('product:fiis')
        )

    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('fiis-buy', None)
        form = FIIBuyForm(session)

        return render(
            self.request,
            'product/pages/fiis/fiis_buy.html',
            context={
                'form': form,
                'button_submit_value': 'comprar',
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['fiis-buy'] = post
        form = FIIBuyForm(
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
            fii = FII.objects.filter(code=data['code']).first()

            user_fii_exisits = UserFII.objects.filter(
                fii=fii,
                user=user,
            ).first()

            if user_fii_exisits:
                user_fii_exisits.buy(
                    trading_note=trading_note, **params,
                )
                return self.success_response(
                    qty=params['quantity'], code=fii.code,
                )

            new_user_fii = UserFII.objects.create(
                user=user,
                fii=fii,
                **params,
            )
            new_user_fii.save()

            fii_history = FiiHistory.objects.create(
                userfii=new_user_fii,
                handler='buy',
                total_price=params['quantity'] * params['unit_price'],
                trading_note=trading_note,
                **params,
            )
            fii_history.save()

            return self.success_response(
                qty=params['quantity'], code=fii.code,
            )

        return redirect(
            reverse('product:fiis_buy')
        )


class FIIsSellView(FIIsView):
    def success_response(self, qty: int, code: str) -> HttpResponseRedirect:
        messages.success(
            self.request,
            (
                f'venda de {qty} unidade(s) de {code.upper()} '
                'realizada com sucesso'
            )
        )
        del self.request.session['fii-sell']
        return redirect(
            reverse('product:fiis')
        )

    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('fii-sell', None)
        form = FIIBuyForm(session)

        return render(
            self.request,
            'product/pages/fiis/fiis_sell.html',
            context={
                'form': form,
                'button_submit_value': 'vender',
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['fii-sell'] = post
        form = FIIBuyForm(
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
            fii = FII.objects.filter(code=data['code']).first()

            user_fii_exists = UserFII.objects.filter(
                user=user,
                fii=fii,
            ).first()

            if user_fii_exists:
                try:
                    user_fii_exists.sell(**params)
                    return self.success_response(
                        qty=params['quantity'], code=data['code']
                        )
                except ValidationError:
                    messages.error(
                        self.request,
                        (
                            'Quantidade insuficiente para venda. '
                            f'Você possui {user_fii_exists.quantity} '
                            'unidade(s) em seu portifólio e está tentando '
                            f'vender {params["quantity"]}.'
                        ),
                    )
                    return redirect(
                        reverse('product:fiis_sell')
                        )

            del self.request.session['fii-sell']
            messages.error(
                self.request,
                'Você não possui este fii em seu portifólio',
            )

        return redirect(
            reverse('product:fiis_sell')
            )
