from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from .update import Update
from product.forms.fixed_income import FixedIncomeApplyRedeemForm


class Details(Update):
    reverse_url_edit: str
    reverse_url_history: str
    reverse_url_delete: str
    reverse_url_profits: str
    reverse_url_apply: str
    reverse_url_redeem: str

    def get(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(kwargs.get('id', None))
        pk = product.id

        session_apply = self.request.session.get('product-apply', None)
        session_redeem = self.request.session.get('product-redeem', None)

        form_apply = FixedIncomeApplyRedeemForm(session_apply)
        form_redeem = FixedIncomeApplyRedeemForm(session_redeem)

        return render(
            self.request,
            self.template_path,
            context={
                'product': product,
                'form_apply': form_apply,
                'form_redeem': form_redeem,
                'url_edit': reverse(self.reverse_url_edit, args=(pk,)),
                'url_history': reverse(self.reverse_url_history, args=(pk,)),
                'url_delete': reverse(self.reverse_url_delete, args=(pk,)),
                'url_profits': reverse(self.reverse_url_profits, args=(pk,)),
                'url_apply': reverse(self.reverse_url_apply, args=(pk,)),
                'url_redeem': reverse(self.reverse_url_redeem, args=(pk,)),
                'profits_payment': (
                    True if product.interest_receipt != 'não há' else False
                ),
                'back_to_page': reverse(self.reverse_url_back_to_page),
            },
        )

    def post(self, *args, **kwargs) -> None:
        raise Http404()
