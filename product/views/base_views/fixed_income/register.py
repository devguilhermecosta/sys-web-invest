from .base import FixedIncomeBaseView
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from product.models import DirectTreasure, ProductFixedIncome
from product.forms.direct_treasure import DirectTreasureRegisterForm
from product.forms.fixed_income import FixedIncomeRegisterForm


class Register(FixedIncomeBaseView):
    model: DirectTreasure | ProductFixedIncome
    form: DirectTreasureRegisterForm | FixedIncomeRegisterForm
    form_title: str = 'registrar'
    template_path: str
    reverse_url_back_to_page: str
    reverse_url_if_form_invalid: str

    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('fixed-income-register', None)
        form = self.form(session)

        return render(
            self.request,
            self.template_path,
            context={
                'form': form,
                'form_title': self.form_title.capitalize(),
                'button_submit_value': 'investir',
                'back_to_page': reverse(self.reverse_url_back_to_page),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['fixed-income-register'] = post
        form = self.form(post)

        if form.is_valid():
            data = form.cleaned_data

            if isinstance(form, DirectTreasureRegisterForm):
                new_obj = DirectTreasure.objects.create(
                    user=self.request.user,
                    name=data['name'],
                    category=data['category'],
                    interest_receipt=data['interest_receipt'],
                    profitability=data['profitability'],
                    maturity_date=data['maturity_date'],
                    description=data['description'],
                )
                new_obj.save()
                new_obj.apply(data['date'], data['value'])

            elif isinstance(form, FixedIncomeRegisterForm):
                new_obj = ProductFixedIncome.objects.create(
                    user=self.request.user,
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
                new_obj.apply(data['grace_period'], data['value'])
                print('ativo criado com sucesso')

            del self.request.session['fixed-income-register']

            messages.success(
                self.request,
                'Aplicação criada com sucesso',
            )

            return redirect(
                reverse(self.reverse_url_back_to_page),
            )

        return redirect(
            reverse(self.reverse_url_if_form_invalid),
        )
