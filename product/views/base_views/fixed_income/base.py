from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from product.models import (
    DirectTreasure,
    ProductFixedIncome,
)


@method_decorator(
    login_required(redirect_field_name='next',
                   login_url='/',
                   ),
    name='dispatch',
)
class FixedIncomeBaseView(View):
    model: DirectTreasure | ProductFixedIncome
    template_title: str
    template_path: str = 'product/partials/_dt_and_fi_intro.html'
    reverse_url_register: str
    reverse_url_back_to_page: str

    def get(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user
        products = self.model.objects.filter(
            user=user,
        ).order_by('-id')

        return render(
            self.request,
            self.template_path,
            context={
                'template_title': self.template_title.capitalize(),
                'url_register': reverse(self.reverse_url_register),
                'products': products,
                'total_applied': self.model.get_total_amount_invested(
                    user=self.request.user,
                ),
                'total_received_in_profits': self.model.get_total_profits(
                    user=self.request.user,
                ),
                'total_tax': self.model.get_total_tax(
                    user=self.request.user,
                ),
                'back_to_page': reverse(self.reverse_url_back_to_page),
            }
        )
