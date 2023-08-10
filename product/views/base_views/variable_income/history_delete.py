from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .delete import Delete
from product.models import ActionHistory, FiiHistory


class HistoryDelete(Delete):
    history_model: ActionHistory | FiiHistory

    def get_history_or_404(self, h_id: int, p_id: int) -> ActionHistory | FiiHistory:  # noqa: E501
        product = self.get_product_or_404(p_id)
        history = get_object_or_404(
            self.history_model,
            pk=h_id,
            userproduct=product,
        )
        return history

    def post(self, *args, **kwargs) -> HttpResponse:
        p = self.get_product_or_404(kwargs.get('p_id', None))
        history = self.get_history_or_404(
            kwargs.get('h_id', None),
            kwargs.get('p_id', None),
            )

        history.delete()

        return redirect(
            reverse(self.reverse_url_response, args=(p.product.code,))
        )
