from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from product.models import ProductFixedIncome
from product.forms.fixed_income import FixedIncomeRegisterForm


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
                'form_title': 'cadastrar novo ativo',
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


class FixedIncomeApplyView(FixedIncomeView):
    def get(self, *args, **kwargs) -> HttpResponse:
        product = get_object_or_404(
            ProductFixedIncome,
            user=self.request.user,
            id=kwargs.get('id'),
        )

        form = FixedIncomeRegisterForm(instance=product)

        return render(
            self.request,
            'product/pages/fixed_income/product_details.html',
            context={
                'form': form,
                }
        )
