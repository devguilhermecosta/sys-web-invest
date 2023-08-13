from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from product.models import UserAction, UserFII


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class BaseView(View):
    model: UserAction | UserFII
    template_path: str
    reverse_url_back_to_page: str

    def get(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user

        total_applied = self.model.get_total_amount_invested(user)
        total_profits = self.model.get_total_profits(user)
        total_tax = None

        if isinstance(self.model(), UserAction):
            total_tax = self.model.get_total_tax(user)

        return render(
            self.request,
            self.template_path,
            context={
                'total_applied': total_applied,
                'total_received_in_profits': total_profits,
                'total_tax': total_tax,
                'back_to_page': reverse(self.reverse_url_back_to_page),
            }
        )
