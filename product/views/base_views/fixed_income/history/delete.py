from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from .update import HistoryUpdate


class HistoryDelete(HistoryUpdate):
    def get(self, *args, **kwargs) -> None:
        raise Http404()

    def post(self, *args, **kwargs) -> HttpResponse:
        history = self.get_history_or_404(
            product_id=kwargs.get('product_id', None),
            history_id=kwargs.get('history_id', None),
        )

        if history.product.user != self.request.user:
            raise Http404()

        history.delete()

        messages.success(
            self.request,
            'histórico deletado com sucesso',
        )

        return redirect(history.product.get_history_url())
