from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .history import History
from product.models import (
    ProductFixedIncome,
    DirectTreasure,
    FixedIncomeHistory,
    DirectTreasureHistory,
    )
from product.forms.fixed_income import FixedIncomeHistoryEditForm
from product.forms.direct_treasure import DirectTreasureHistoryForm


class HistoryUpdate(History):
    history_form: FixedIncomeHistoryEditForm | DirectTreasureHistoryForm

    def choices(self, product: ProductFixedIncome | DirectTreasure) -> tuple:
        choices = [
            ('apply', 'aplicação'),
            ('redeem', 'resgate'),
        ]

        if product.interest_receipt != 'não há':
            choices.append(('profits', 'recebimento de juros'))

        return choices

    def get_history_or_404(self,
                           product_id: int,
                           history_id: int,
                           ) -> FixedIncomeHistory | DirectTreasureHistory:
        history = get_object_or_404(
            self.history_model,
            product=self.get_product_or_404(id=product_id),
            pk=history_id,
        )
        return history

    def get(self, *args, **kwargs) -> HttpResponse:
        history = self.get_history_or_404(
            product_id=kwargs.get('product_id', None),
            history_id=kwargs.get('history_id', None)
        )
        product = self.get_product_or_404(kwargs.get('product_id', None))

        history.tax_and_irpf = abs(history.tax_and_irpf)
        history.value = abs(history.value)

        session = self.request.session.get('fixed-income-histyory-edit', None)
        form = self.history_form(session, instance=history)
        form.fields['state'].widget.choices = self.choices(product)

        return render(
            self.request,
            self.template_path,
            context={
                'form': form,
                'form_title': 'editar histórico',
                'button_submit_value': 'salvar',
                'back_to_page': product.get_history_url(),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        history = self.get_history_or_404(
            product_id=kwargs.get('product_id', None),
            history_id=kwargs.get('history_id', None),
        )
        product = self.get_product_or_404(kwargs.get('product_id', None))
        post = self.request.POST
        self.request.session['fixed-income-histyory-edit'] = post
        form = self.history_form(post)

        if form.is_valid():
            data = form.cleaned_data
            history.update(**data)

            del self.request.session['fixed-income-histyory-edit']

            messages.success(
                self.request,
                'histórico salvo com sucesso',
            )

            return redirect(product.get_history_url())

        return redirect(history.get_absolute_url())
