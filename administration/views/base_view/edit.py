from typing import Any, Dict
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from product.models import FII, Action
from .register import Register
from administration.forms import ActionEditForm, FIIEditForm


class Edit(Register):
    form: ActionEditForm | FIIEditForm
    reverse_url_success_response: str
    reverse_url_invalid_form: str

    def get_product_or_404(self, code: str) -> FII | Action:
        product = get_object_or_404(
            self.model,
            code=code,
        )
        return product

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        product = self.get_product_or_404(kwargs.get('code', None))
        session = self.request.session.get('admin-product-edit', None)
        form = self.form(session, instance=product)

        context_data.update({
            'form': form,
            'form_title': self.form_title or product.description,
            'button_submit_value': 'salvar',
            'is_main_page': False,
        })

        return context_data

    def post(self, *args, **kwargs) -> HttpResponse:
        code = kwargs.get('code', None)
        product = self.get_product_or_404(code)
        post = self.request.POST
        self.request.session['admin-product-edit'] = post
        form = self.form(post)

        if form.is_valid():
            data = form.cleaned_data
            product.update(**data)

            messages.success(
                self.request,
                'salvo com sucesso',
            )

            del self.request.session['admin-product-edit']

            return redirect(
                reverse(self.reverse_url_success_response)
            )

        return redirect(
            reverse(self.reverse_url_invalid_form, args=(code,))
        )
