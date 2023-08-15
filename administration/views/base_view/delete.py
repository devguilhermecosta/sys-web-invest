from django.http import Http404, HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from .update import Update
from product.models import UserAction, UserFII


class Delete(Update):
    userproduct_model: UserAction | UserFII
    reverse_url_error_response: str

    def get(self, *args, **kwargs) -> None:
        raise Http404()

    def post(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(kwargs.get('code', None))
        userproduct = self.userproduct_model.objects.filter(product=product)

        if userproduct.exists():
            messages.error(
                self.request,
                'Este ativo não pode ser deletado, '
                'pois está em uso por algum usuário.'
            )

            return redirect(
                reverse(self.reverse_url_error_response)
            )

        product.delete()

        messages.success(
            self.request,
            'ativo deletado com sucesso',
        )

        return redirect(
            reverse(self.reverse_url_success_response)
        )
