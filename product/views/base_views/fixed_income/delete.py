from django.http import HttpResponse, Http404
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from .update import Update


class Delete(Update):
    reverse_url_redirect: str

    def get(self, *args, **kwargs) -> None:
        raise Http404()

    def post(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(kwargs.get('id', None))
        product.delete()

        messages.success(
            self.request,
            'ativo deletado com sucesso',
        )

        return redirect(
            reverse(self.reverse_url_redirect)
        )
