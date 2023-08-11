from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .delete import Delete
from product.models import ActionHistory, FiiHistory


class HistoryDelete(Delete):
    history_model: ActionHistory | FiiHistory

    def get_history_or_404(self, h_id: int, p_id: int) -> ActionHistory | FiiHistory:  # noqa: E501
        userproduct = self.get_product_or_404(p_id)
        history = get_object_or_404(
            self.history_model,
            pk=h_id,
            userproduct=userproduct,
        )
        return history, userproduct

    def post(self, *args, **kwargs) -> HttpResponse:
        history, userproduct = self.get_history_or_404(
            kwargs.get('h_id', None),
            kwargs.get('p_id', None),
            )

        history.delete()

        messages.success(
            self.request,
            'histórico deletado com sucesso',
        )

        return redirect(
            reverse(self.reverse_url_response,
                    args=(userproduct.product.code,),
                    )
        )
