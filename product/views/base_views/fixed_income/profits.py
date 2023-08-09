from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .update import Update
from product.forms.fixed_income import FixedIncomeProfitsReceivForm


class ReceiveProfits(Update):
    reverse_url_if_form_invalid: str

    def get(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(kwargs.get('id', None))
        session = self.request.session.get(
            'product-receive-profits',
            None,
            )
        form = FixedIncomeProfitsReceivForm(session)

        return render(
            self.request,
            self.template_path,
            context={
                'form': form,
                'form_title': product.name.upper(),
                'button_submit_value': 'receber',
                'back_to_page': product.get_absolute_url(),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(kwargs.get('id', None))
        post = self.request.POST
        self.request.session['product-receive-profits'] = post
        form = FixedIncomeProfitsReceivForm(post)

        if form.is_valid():
            data = form.cleaned_data
            product.receive_profits(**data)

            del self.request.session['product-receive-profits']

            messages.success(
                self.request,
                'Recebimento de juros salvo com sucesso',
            )

            return redirect(product.get_absolute_url())

        return redirect(
            reverse(
                self.reverse_url_if_form_invalid,
                args=(product.id,),
                )
        )
