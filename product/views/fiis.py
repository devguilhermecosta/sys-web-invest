from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from product.forms import FIIBuyForm
from product.models import FII, UserFII, FiiHistory
from .base_views.variable_income import Buy, Sell


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


class FIISBuyView(Buy):
    success_response_url_redirect = 'product:fiis'
    error_response_url_redirect = 'product:fiis_buy'
    form = FIIBuyForm
    template_get_request = 'product/pages/fiis/fiis_buy.html'
    product_model = FII
    user_product_model = UserFII
    history_model = FiiHistory


class FIIsSellView(Sell):
    success_response_url_redirect = 'product:fiis'
    error_response_url_redirect = 'product:fiis_sell'
    form = FIIBuyForm
    template_get_request = 'product/pages/fiis/fiis_sell.html'
    product_model = FII
    user_product_model = UserFII


class FIIHistoryDetails(FIIsView):
    def get(self, *args, **kwargs) -> HttpResponse:
        fii = get_object_or_404(
            FII,
            code=kwargs.get('code', None)
        )

        user_fii = get_object_or_404(
            UserFII,
            user=self.request.user,
            product=fii,
        )

        if user_fii:
            fii_history = FiiHistory.objects.filter(
                userproduct=user_fii,
            ).order_by('-date')
        else:
            raise Http404()

        return render(
            self.request,
            'product/pages/fiis/fiis_history.html',
            context={
                'history': fii_history,
            }
        )
