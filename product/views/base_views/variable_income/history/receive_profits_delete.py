from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from .receive_profits_edit import ReceiveProfitsEdit


class ReceiveProfitsDelete(ReceiveProfitsEdit):
    def get(self, *args, **kwargs) -> None:
        raise Http404()

    def post(self, *args, **kwargs) -> HttpResponse:
        history = self.get_history_or_404(kwargs.get('id', None))
        history.delete()
        return redirect(
            reverse(self.reverse_url_success_response)
        )
