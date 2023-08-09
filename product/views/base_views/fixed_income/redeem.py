from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from .apply import Apply
from product.forms.fixed_income import FixedIncomeApplyRedeemForm


class Redeem(Apply):
    def post(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(kwargs.get('id', None))
        post = self.request.POST
        self.request.session['product-redeem'] = post
        form = FixedIncomeApplyRedeemForm(post)

        if form.is_valid():
            data = form.cleaned_data

            if data['value'] > product.get_current_value():
                messages.error(
                    self.request,
                    'Saldo insuficiente para resgate'
                )
                return redirect(product.get_absolute_url())

            product.redeem(date=data['date'], value=data['value'])

            del self.request.session['product-redeem']

            messages.success(
                self.request,
                'Resgate realizado com sucesso.'
            )

        return redirect(product.get_absolute_url())
