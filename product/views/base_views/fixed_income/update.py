from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .base import FixedIncomeBaseView
from product.models import ProductFixedIncome, DirectTreasure
from product.forms.fixed_income import FixedIncomeEditForm
from product.forms.direct_treasure import DirectTreasureEditForm


class Update(FixedIncomeBaseView):
    model: ProductFixedIncome | DirectTreasure
    form: FixedIncomeEditForm | DirectTreasureEditForm
    form_title: str = 'atualizar'
    template_path: str

    def get_product_or_404(self,
                           id: int = None,
                           ) -> ProductFixedIncome | DirectTreasure:
        product = None
        if id is not None:
            product = get_object_or_404(
                self.model,
                user=self.request.user,
                pk=id,
            )
        return product

    def render_product(self,
                       form: FixedIncomeEditForm | DirectTreasureEditForm,
                       product: ProductFixedIncome | DirectTreasure,
                       ) -> HttpResponse:
        return render(
            self.request,
            self.template_path,
            context={
                'form': form,
                'form_title': self.form_title.capitalize(),
                'button_submit_value': 'salvar',
                'back_to_page': product.get_absolute_url(),
            }
        )

    def get(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(kwargs.get('id', None))
        session = self.request.session.get('fixed-income-edit', None)
        form = self.form(session, instance=product)
        return self.render_product(form, product)

    def post(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(kwargs.get('id', None))
        post = self.request.POST
        self.request.session['fixed-income-edit'] = post
        form = self.form(post, instance=product)

        if form.is_valid():
            form.save()
            del self.request.session['fixed-income-edit']

            messages.success(
                self.request,
                'Salvo com sucesso',
            )

            return redirect(product.get_absolute_url())

        return self.render_product(form, product)
