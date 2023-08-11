from django.views import View
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from product.models import (
    Action,
    UserAction,
    ActionHistory,
    FII,
    UserFII,
    FiiHistory,
    )


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class History(View):
    template_to_render_response: str = ''
    product_model: Action | FII = ''
    user_product_model: UserAction | UserFII = ''
    history_model: ActionHistory | FiiHistory = ''
    reverse_url_back_to_page: str

    def get(self, *args, **kwargs) -> HttpResponse:
        product = get_object_or_404(
            self.product_model,
            code=kwargs.get('code', None),
        )

        user_product = get_object_or_404(
            self.user_product_model,
            user=self.request.user,
            product=product,
        )

        if not user_product:
            raise Http404()

        product_history = self.history_model.objects.filter(
            userproduct=user_product,
        ).order_by('-date')

        return render(
            self.request,
            self.template_to_render_response,
            context={
                'history': product_history,
                'product': product,
                'back_to_page': reverse(self.reverse_url_back_to_page),
            }
        )
