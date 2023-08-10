from django.http import Http404, HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .delete import Delete
from product.models import ActionHistory, FiiHistory


class HistoryDelete(Delete):
    history_model: ActionHistory | FiiHistory

    def get_history_or_404(self, id: int,) -> ActionHistory | FiiHistory:
        history = get_object_or_404(
            self.history_model,
            pk=id,
        )
        return history

    def post(self, *args, **kwargs) -> HttpResponse:
        history = self.get_history_or_404(kwargs.get('id', None))

        if history.userproduct.user != self.request.user:
            raise Http404()

        history.delete()

        return HttpResponse('')

        # return redirect(
        #     reverse(self.reverse_url_response, args=(product.code,))
        # )
