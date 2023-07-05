from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from product.models import ProductFixedIncome


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
