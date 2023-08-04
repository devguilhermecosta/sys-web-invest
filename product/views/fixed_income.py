from django.views import View
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
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


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class FixedIncomeView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        fixed_income_objects = ProductFixedIncome.objects.filter(
            user=self.request.user,
        ).order_by('-id')

        return render(
            self.request,
            'product/pages/fixed_income/fixed_income.html',
            context={
                'fixed_income_objects': fixed_income_objects,
            }
        )


class FixedIncomeRegisterView(FixedIncomeView):
    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get(
            'fixed-income-register', None,
        )
        form = FixedIncomeRegisterForm(session)

        return render(
            self.request,
            'product/pages/fixed_income/fixed_income_register.html',
            context={
                'form': form,
                'form_title': 'Novo ativo',
                'button_submit_value': 'aplicar',
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['fixed-income-register'] = post
        form = FixedIncomeRegisterForm(post)

        if form.is_valid():
            data = form.cleaned_data
            user = self.request.user

            new_obj = ProductFixedIncome.objects.create(
                user=user,
                category=data['category'],
                name=data['name'],
                grace_period=data['grace_period'],
                maturity_date=data['maturity_date'],
                liquidity=data['liquidity'],
                profitability=data['profitability'],
                interest_receipt=data['interest_receipt'],
                description=data.get('description', ''),
            )
            new_obj.save()
            new_obj.apply(date=data['grace_period'], value=data['value'])

            del self.request.session['fixed-income-register']

            messages.success(
                self.request,
                f"Ativo {data['name'].upper()} criado com sucesso."
            )
            return redirect(
                reverse('product:fixed_income'),
            )

        return redirect(
            reverse('product:fixed_income_register'),
        )


class FixedIncomeEditView(FixedIncomeView):
    def get_product_or_404(self, id: int = None) -> ProductFixedIncome:
        product = None

        if id is not None:
            product = get_object_or_404(
                ProductFixedIncome,
                user=self.request.user,
                pk=id,
            )
        return product

    def render_product(self, form) -> HttpResponse:
        return render(
            self.request,
            'product/pages/fixed_income/fixed_income_edit.html',
            context={
                'form': form,
                'button_submit_valget_product_or_404ue': 'salvar',
            }
        )

    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        product = self.get_product_or_404(id)
        session = self.request.session.get('product-fixed-income-edit', None)
        form = FixedIncomeEditForm(session, instance=product)
        return self.render_product(form)

    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        product = self.get_product_or_404(id)
        post = self.request.POST
        self.request.session['product-fixed-income-edit'] = post
        form = FixedIncomeEditForm(
            files=self.request.FILES or None,
            data=self.request.POST or None,
            instance=product,
        )

        if form.is_valid():
            form.save()

            del self.request.session['product-fixed-income-edit']

            messages.success(
                self.request,
                'Salvo com sucesso',
            )

            return redirect(
                reverse('product:fixed_income_details', args=(product.id,))
            )

        messages.error(
            self.request,
            'Verifique os dados abaixo',
        )

        return self.render_product(form)


class FixedIncomeDetailsView(FixedIncomeView):
    def get(self, request: HttpRequest, id: int = None) -> HttpResponse:
        product = get_object_or_404(
            ProductFixedIncome,
            pk=id,
            user=self.request.user,
        )

        session_apply = self.request.session.get('product-apply', None)
        session_redeem = self.request.session.get('product-redeem', None)
        form_apply = FixedIncomeApplyRedeemForm(session_apply)
        form_redeem = FixedIncomeApplyRedeemForm(session_redeem)

        return render(
            self.request,
            'product/pages/fixed_income/product_details.html',
            context={
                'product': product,
                'form_apply': form_apply,
                'form_redeem': form_redeem,
                'url_apply': reverse(
                    'product:fixed_income_apply', args=(product.id,)
                ),
                'url_redeem': reverse(
                    'product:fixed_income_redeem', args=(product.id,)
                ),
                'profits_payment': (
                    True if product.interest_receipt != 'não há' else False
                )
            },
        )


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
            'product/pages/fixed_income/profits_receipt.html',
            context={
                'form': form,
                'form_title': product.name.upper(),
                'button_submit_value': 'receber',
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
                'history': history
            }
        )


class FixedIncomeHistoryEditView(FixedIncomeProfitsReceiptView):
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
        history.tax_and_irpf = abs(history.tax_and_irpf)
        history.value = abs(history.value)

        session = self.request.session.get('fixed-income-histyory-edit', None)
        form = FixedIncomeHistoryEditForm(session, instance=history)

        return render(
            self.request,
            'product/pages/fixed_income/history_edit.html',
            context={
                'form': form,
                'form_title': 'editar histórico',
                'button_submit_value': 'salvar',
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
