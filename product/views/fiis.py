from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from product.forms import FIIBuyForm, FIIReceiptProfitsForm
from product.models import FII, UserFII, FiiHistory
from .base_views.variable_income import Buy, Sell, History


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


class FIIHistoryDetails(History):
    template_to_render_response = 'product/partials/_history_variable_income.html'  # noqa: E501
    product_model = FII
    user_product_model = UserFII
    history_model = FiiHistory


class FIIManageIncomeReceipt(FIIsView):
    def get(self, *args, **kwargs) -> HttpResponse:
        products = UserFII.objects.filter(
            user=self.request.user
        )

        choices = [('---', '---')]
        for product in products:
            choices.append(
                (product.product.id, product.product.code),
            )

        form = FIIReceiptProfitsForm()
        form.fields.get('product_id').widget.choices = choices

        return render(
            self.request,
            'product/pages/fiis/fiis_income.html',
            context={
                'form': form,
                'custom_id': 'form_fii_receiv_profis',
                'button_submit_value': 'salvar',
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        form = FIIReceiptProfitsForm(post)

        if form.is_valid():
            p_id = form.cleaned_data['product_id']
            value = form.cleaned_data['value']
            date = form.cleaned_data['date']

            product = UserFII.objects.get(
                user=self.request.user,
                product=p_id
            )
            product.receive_profits(
                value=value,
                date=date,
            )

        return JsonResponse({'data': ''})
