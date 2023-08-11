from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from product.models import UserAction, UserFII
from .buy import Buy


class Delete(Buy):
    model: UserAction | UserFII
    reverse_url_response: str

    def get_product_or_404(self, id: int) -> UserAction | UserFII:
        product = get_object_or_404(
            self.model,
            pk=id,
            user=self.request.user,
        )
        return product

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
            reverse(self.reverse_url_response),
        )
