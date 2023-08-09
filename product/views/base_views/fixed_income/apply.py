from django.http import HttpResponse, Http404
from django.contrib import messages
from django.shortcuts import redirect
from .update import Update
from product.forms.fixed_income import FixedIncomeApplyRedeemForm


class Apply(Update):
    def get(self, *args, **kwargs) -> HttpResponse:
        raise Http404()

    def post(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(kwargs.get('id', None))
        post = self.request.POST
        self.request.session['product-apply'] = post
        form = FixedIncomeApplyRedeemForm(post)

        if form.is_valid():
            data = form.cleaned_data
            product.apply(date=data['date'], value=data['value'])

            del self.request.session['product-apply']

            messages.success(
                self.request,
                'Aplicação realizada com sucesso.'
            )

        return redirect(product.get_absolute_url())
