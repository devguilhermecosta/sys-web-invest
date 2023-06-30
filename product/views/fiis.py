from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.forms import FIIBuyForm
from product.models import FII, UserFII


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
        form = FIIBuyForm(post)

        if form.is_valid():
            data = form.cleaned_data
            code = data['code']
            qty = int(data['quantity'])
            up = float(data['unit_price'])
            user = self.request.user
            fii = FII.objects.filter(code=code).first()

            user_fii = UserFII.objects.filter(
                fii=fii,
                user=user,
            )

            if user_fii.exists():
                actual_user_fii = user_fii.first()
                actual_user_fii.quantity += qty
                actual_user_fii.unit_price = up
                actual_user_fii.save()

            new_fii = UserFII.objects.create(
                user=user,
                fii=fii,
                quantity=qty,
                unit_price=up,
            )
            new_fii.save()

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

        return redirect(
            reverse('product:fiis_buy')
        )
