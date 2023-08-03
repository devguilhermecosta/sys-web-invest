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
    FixedIncomeApplyRedeemForm,
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
        )

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
                **data,
            )
            new_obj.save()
            new_obj.make_history(state='apply', value=data['value'])

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
    def get_product(self, id: int = None) -> ProductFixedIncome:
        product = None

        if id is not None:
            product = get_object_or_404(
                ProductFixedIncome,
                pk=id,
            )
        return product

    def render_product(self, form) -> HttpResponse:
        return render(
            self.request,
            'product/pages/fixed_income/fixed_income_edit.html',
            context={
                'form': form,
                'button_submit_value': 'salvar',
                }
        )

    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        product = self.get_product(id)
        session = self.request.session.get('product-fixed-income-edit', None)
        form = FixedIncomeEditForm(session, instance=product)
        return self.render_product(form)

    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        product = self.get_product(id)
        post = self.request.POST
        self.request.session['product-fixed-income-edit'] = post
        form = FixedIncomeEditForm(
            files=self.request.FILES or None,
            data=self.request.POST or None,
            instance=product,
            )

        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()

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
        product = self.get_product(id)
        post = self.request.POST
        self.request.session['product-apply'] = post
        form = FixedIncomeApplyRedeemForm(post)

        if form.is_valid():
            data = form.cleaned_data
            product.value += data['value']
            product.save()
            product.make_history(state='apply',
                                 date=data['date'],
                                 value=data['value'],
                                 )

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
        product = self.get_product(id)
        post = self.request.POST
        self.request.session['product-redeem'] = post
        form = FixedIncomeApplyRedeemForm(post)

        if form.is_valid():
            data = form.cleaned_data

            if data['value'] > product.value:
                messages.error(
                    self.request,
                    'Saldo insuficiente para resgate'
                )
                return redirect(
                    reverse('product:fixed_income_details', args=(product.id,))
                )

            product.value -= data['value']
            product.save()
            product.make_history(state='redeem',
                                 date=data['date'],
                                 value=data['value'],
                                 )

            del self.request.session['product-redeem']

            messages.success(
                self.request,
                'Resgate realizado com sucesso.'
            )

        return redirect(
            reverse('product:fixed_income_details', args=(product.id,))
        )


class FixedIncomeHistoryView(FixedIncomeView):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        product = get_object_or_404(
            ProductFixedIncome,
            user=request.user,
            pk=id,
        )
        history = FixedIncomeHistory.objects.filter(
            product=product
            ).order_by('-id')

        return render(
            request,
            'product/partials/_history_dt_&_fi.html',
            context={
                'product': product,
                'history': history
            }
        )
