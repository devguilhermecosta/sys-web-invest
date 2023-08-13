from django.http import JsonResponse, Http404
from product.forms import FIIBuyForm, FIIReceiptProfitsForm
from product.models import FII, UserFII, FiiHistory
from .base_views.variable_income import (
    BaseView,
    ListView,
    Buy,
    Sell,
    History,
    HistoryDelete,
    Delete,
    ReceiveProfits,
    ReceiveProfitsEdit,
    ReceiveProfitsDelete,
    )


class FIIsView(BaseView):
    model = UserFII
    template_path = 'product/pages/fiis/fiis.html'
    reverse_url_back_to_page = 'dashboard:user_dashboard'


class AllFIIsView(ListView):
    model = UserFII
    template_path = 'product/pages/fiis/fiis_list.html'
    reverse_url_back_to_page = 'product:fiis'


class FIISBuyView(Buy):
    success_response_url_redirect = 'product:fiis'
    error_response_url_redirect = 'product:fiis_buy'
    form = FIIBuyForm
    template_get_request = 'product/pages/fiis/fiis_buy.html'
    product_model = FII
    user_product_model = UserFII
    history_model = FiiHistory
    reverse_url_back_to_page = 'product:fiis'


class FIIsSellView(Sell):
    success_response_url_redirect = 'product:fiis'
    error_response_url_redirect = 'product:fiis_sell'
    form = FIIBuyForm
    template_get_request = 'product/pages/fiis/fiis_sell.html'
    product_model = FII
    user_product_model = UserFII
    reverse_url_back_to_page = 'product:fiis'


class FiisDeleteView(Delete):
    model = UserFII
    reverse_url_response = 'product:fiis_list'


class FIIHistoryDetails(History):
    template_to_render_response = 'product/partials/_history_variable_income.html'  # noqa: E501
    product_model = FII
    user_product_model = UserFII
    history_model = FiiHistory
    reverse_url_back_to_page = 'product:fiis_list'


class FiisHistoryDeleteView(HistoryDelete):
    model = UserFII
    history_model = FiiHistory
    reverse_url_response = 'product:fii_history'


class FIIManageIncomeReceipt(ReceiveProfits):
    user_product_model = UserFII
    profits_form = FIIReceiptProfitsForm
    template_path = 'product/pages/fiis/fiis_profits.html'
    form_custom_id = 'form_fii_receiv_profis'
    reverse_url_history_profits = 'product:fii_history_json'
    reverse_url_receive_profits = 'product:fiis_manage_income_receipt'
    reverse_url_total_profits = 'product:fii_total_profits_json'
    reverse_url_back_to_page = 'product:fiis'


class FIIManageIncomeReceiptHistory(FIIsView):
    def get(self, *args, **kwargs) -> JsonResponse:
        history = UserFII.get_full_history(
            user=self.request.user,
            handler='profits',
            )
        return JsonResponse({'data': history})

    def post(self, *args, **kwargs) -> Http404:
        raise Http404()


class FIIManageIncomeReceiptEditHistory(ReceiveProfitsEdit):
    user_product_model = UserFII
    history_model = FiiHistory
    profits_form = FIIReceiptProfitsForm
    template_path = 'product/pages/fiis/fiis_profits.html'
    reverse_url_back_to_page = 'product:fiis_manage_income'
    reverse_url_success_response = 'product:fiis_manage_income'
    reverse_url_invalid_form = 'product:fii_manage_income_receipt_edit'


class FIIManageIncomeReceiptDeleteHistory(ReceiveProfitsDelete):
    user_product_model = UserFII
    history_model = FiiHistory
    reverse_url_success_response = 'product:fiis_manage_income'


class GetTotalProfitsView(FIIsView):
    def get(self, *args, **kwargs) -> JsonResponse:
        total = UserFII.get_total_profits(self.request.user)
        return JsonResponse({'value': total})

    def post(self, *args, **kwargs) -> None:
        raise Http404()
