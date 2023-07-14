from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from product.models import DirectTreasure


@method_decorator(
    login_required(redirect_field_name='next',
                   login_url='/',
                   ),
    name='dispatch',
)
class DirectTreasureView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user
        products = DirectTreasure.objects.filter(
            user=user,
        )

        return render(
            self.request,
            'product/pages/direct_treasure/direct_treasure.html',
            context={
                'products': products,
            }
        )


class DirectTreasureRegisterView(DirectTreasureView):
    def get(self, *args, **kwargs) -> HttpResponse:
        return render(
            self.request,
            'product/pages/direct_treasure/register.html',
        )
