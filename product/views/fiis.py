from django.views import View
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import ListView
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.forms import FIIBuyForm, FIIReceiptProfitsForm
from product.models import FII, UserFII, FiiHistory
from .base_views.variable_income import Buy, Sell, History
from typing import List


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
    def choices(self) -> List[tuple]:
        products = UserFII.objects.filter(
            user=self.request.user
        )

        choices = [('---', '---')]
        for product in products:
            choices.append(
                (product.product.id, str(product.product.code).upper()),
            )
        return choices

    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('fiis_manage_income', None)
        form = FIIReceiptProfitsForm(session)
        form.fields.get('product_id').widget.choices = self.choices()

        return render(
            self.request,
            'product/pages/fiis/fiis_profits.html',
            context={
                'url': reverse('product:fii_history_json'),
                'form': form,
                'form_title': 'Receber Proventos',
                'custom_id': 'form_fii_receiv_profis',
                'button_submit_value': 'salvar',
                'history_table': True,
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['fiis_manage_income'] = post
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

            del self.request.session['fiis_manage_income']

            return JsonResponse({'success': 'success request'})

        return redirect(
            reverse('product:fiis_manage_income')
        )


class FIIManageIncomeReceiptHistory(FIIsView):
    def get(self, *args, **kwargs) -> HttpResponse:
        history = UserFII.get_full_history(
            user=self.request.user,
            handler='profits',
            )
        return JsonResponse(
            {'data': history}
        )

    def post(self, *args, **kwargs) -> Http404:
        raise Http404()


class FIIManageIncomeReceiptEditHistory(FIIManageIncomeReceipt):
    def get(self, *args, **kwargs) -> HttpResponse:
        history = get_object_or_404(
            FiiHistory,
            pk=kwargs.get('id', None)
        )

        session = self.request.session.get('fiis-profits-edit', None)

        form = FIIReceiptProfitsForm(
            session,
            initial={
                'product_id': history.userproduct.id,
                'date': str(history.date),
                'value': f'{history.total_price:.2f}',
                }
            )
        form.fields.get('product_id').widget.choices = self.choices()

        return render(
            self.request,
            'product/pages/fiis/fiis_profits.html',
            context={
                'form': form,
                'form_title': 'editar',
                'button_submit_value': 'salvar',
                'history_table': False,
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get('id', None)
        post = self.request.POST
        self.request.session['fiis-profits-edit'] = post
        form = FIIReceiptProfitsForm(post)

        if form.is_valid():
            data = form.cleaned_data
            history = FiiHistory.objects.filter(pk=pk).first()
            user_product = UserFII.objects.get(pk=data['product_id'])

            history.userproduct = user_product
            history.date = data['date']
            history.total_price = data['value']
            history.save()

            del self.request.session['fiis-profits-edit']

            messages.success(
                self.request,
                'salvo com sucesso',
            )

            return redirect(
                reverse('product:fiis_manage_income')
            )

        return redirect(
            reverse(
                'product:fii_manage_income_receipt_edit', args=(pk,)
                )
        )


class FIIManageIncomeReceiptDeleteHistory(FIIsView):
    ...
    # criar o método para somar o total de proventos
