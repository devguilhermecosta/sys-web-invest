from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from product.models import ProductFixedIncome, FixedIncomeHistory
from product.forms.fixed_income import (
    FixedIncomeRegisterForm,
    FixedIncomeEditForm,
    FixedIncomeHistoryEditForm,
    FixedIncomeApplyRedeemForm,
    FixedIncomeProfitsReceivForm,
)
from product.views.base_views.fixed_income import (
    FixedIncomeBaseView,
    Register,
    Update,
    Delete,
    Details,
    )


class FixedIncomeView(FixedIncomeBaseView):
    model = ProductFixedIncome
    template_title = 'renda fixa'
    template_path = 'product/partials/_dt_and_fi_intro.html'
    reverse_url_register = 'product:fixed_income_register'
    reverse_url_back_to_page = 'dashboard:user_dashboard'


class FixedIncomeRegisterView(Register):
    model = ProductFixedIncome
    form = FixedIncomeRegisterForm
    template_path = 'product/partials/_dt_and_fi_register.html'
    reverse_url_back_to_page = 'product:fixed_income'
    reverse_url_if_form_invalid = 'product:fixed_income_register'


class FixedIncomeEditView(Update):
    model = ProductFixedIncome
    form = FixedIncomeEditForm
    template_path = 'product/partials/_dt_and_fi_edit.html'


class FixedIncomeDeleteView(Delete):
    model = ProductFixedIncome
    reverse_url_redirect = 'product:fixed_income'


class FixedIncomeDetailsView(Details):
    model = ProductFixedIncome
    template_path = 'product/partials/_dt_and_fi_details.html'
    reverse_url_back_to_page = 'product:fixed_income'
    reverse_url_edit = 'product:fixed_income_edit'
    reverse_url_history = 'product:fixed_income_history'
    reverse_url_delete = 'product:fixed_income_delete'
    reverse_url_profits = 'product:fixed_income_profits_receipt'
    reverse_url_apply = 'product:fixed_income_apply'
    reverse_url_redeem = 'product:fixed_income_redeem'


class FixedIncomeApplyView(FixedIncomeEditView):
    def get(self, *args, **kwargs) -> HttpResponse:
        raise Http404()

    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        product = self.get_product_or_404(id)
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

        return redirect(
            reverse('product:fixed_income_details', args=(product.id,))
        )


class FixedIncomeRedeemView(FixedIncomeApplyView):
    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        product = self.get_product_or_404(id)
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
                return redirect(
                    reverse('product:fixed_income_details', args=(product.id,))
                )

            product.redeem(date=data['date'], value=data['value'])

            del self.request.session['product-redeem']

            messages.success(
                self.request,
                'Resgate realizado com sucesso.'
            )

        return redirect(
            reverse('product:fixed_income_details', args=(product.id,))
        )


class FixedIncomeProfitsReceiptView(FixedIncomeView):
    def get_product_or_404(self, id: int) -> ProductFixedIncome:
        product = get_object_or_404(
            ProductFixedIncome,
            pk=id,
            user=self.request.user,
        )
        return product

    def get(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(id=kwargs.get('id', None))
        session = self.request.session.get(
            'fixed-income-profits-receive', None,
            )
        form = FixedIncomeProfitsReceivForm(session)

        return render(
            self.request,
            'product/partials/_dt_and_fi_profits_receipt.html',
            context={
                'form': form,
                'form_title': product.name.upper(),
                'button_submit_value': 'receber',
                'back_to_page': reverse(
                    'product:fixed_income_details',
                    args=(product.id,)
                    ),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(id=kwargs.get('id', None))
        post = self.request.POST
        self.request.session['fixed-income-profits-receive'] = post
        form = FixedIncomeProfitsReceivForm(post)

        if form.is_valid():
            data = form.cleaned_data
            product.receive_profits(**data)

            del self.request.session['fixed-income-profits-receive']

            messages.success(
                self.request,
                'Recebimento de juros salvo com sucesso',
            )

            return redirect(
                reverse('product:fixed_income_details', args=(product.id,))
            )

        return redirect(
            reverse('product:fixed_income_profits_receipt', args=(product.id,))
        )


class FixedIncomeHistoryView(FixedIncomeView):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        product = get_object_or_404(
            ProductFixedIncome,
            pk=id,
            user=request.user,
        )
        history = FixedIncomeHistory.objects.filter(
            product=product
        ).order_by('-date')

        return render(
            request,
            'product/partials/_history_dt_and_fi.html',
            context={
                'product': product,
                'history': history,
                'profits_payment': (
                    False if product.interest_receipt == 'não há' else True
                    ),
                'fixed_income': True,
                'back_to_page': reverse(
                    'product:fixed_income_details',
                    args=(product.id,)
                    ),
            }
        )


class FixedIncomeHistoryEditView(FixedIncomeProfitsReceiptView):
    def choices(self, product: ProductFixedIncome) -> tuple:
        choices = [
            ('apply', 'aplicação'),
            ('redeem', 'resgate'),
        ]

        if product.interest_receipt != 'não há':
            choices.append(('profits', 'recebimento de juros'))

        return choices

    def get_history_or_404(self, product_id: int, history_id: int) -> FixedIncomeHistory:  # noqa: E501
        history = get_object_or_404(
            FixedIncomeHistory,
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
        form = FixedIncomeHistoryEditForm(session, instance=history)
        form.fields['state'].widget.choices = self.choices(product)

        return render(
            self.request,
            'product/partials/_dt_and_fi_history_edit.html',
            context={
                'form': form,
                'form_title': 'editar histórico',
                'button_submit_value': 'salvar',
                'back_to_page': reverse(
                    'product:fixed_income_history',
                    args=(product.id,)
                    ),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        history = self.get_history_or_404(
            product_id=kwargs.get('product_id', None),
            history_id=kwargs.get('history_id', None),
        )
        post = self.request.POST
        self.request.session['fixed-income-histyory-edit'] = post
        form = FixedIncomeHistoryEditForm(post)

        if form.is_valid():
            data = form.cleaned_data
            history.update(**data)

            del self.request.session['fixed-income-histyory-edit']

            messages.success(
                self.request,
                'histórico salvo com sucesso',
            )

            return redirect(
                reverse(
                    'product:fixed_income_history',
                    args=(kwargs.get('product_id', None),),
                    )
            )

        return redirect(
            reverse(
                'product:fixed_income_history_edit',
                kwargs={
                    'product_id': kwargs.get('product_id', None),
                    'history_id': kwargs.get('history_id', None),
                }
                )
        )


class FixedIncomeHistoryDeleteView(FixedIncomeHistoryEditView):
    def get(self, *args, **kwargs) -> None:
        raise Http404()

    def post(self, *args, **kwargs) -> HttpResponse:
        history = self.get_history_or_404(
            product_id=kwargs.get('product_id', None),
            history_id=kwargs.get('history_id', None),
        )

        if history.product.user != self.request.user:
            raise Http404()

        history.delete()

        messages.success(
            self.request,
            'histórico deletado com sucesso',
        )

        return redirect(
            reverse('product:fixed_income_history',
                    args=(kwargs.get('product_id', None),)
                    )
            )
