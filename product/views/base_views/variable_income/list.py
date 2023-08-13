from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from .base import BaseView


class ListView(BaseView):
    def get(self, *args, **kwargs) -> HttpResponse:
        products = self.model.objects.filter(
            user=self.request.user
            ).order_by('-id')

        return render(
            self.request,
            self.template_path,
            context={
                'products': products,
                'back_to_page': reverse(self.reverse_url_back_to_page),
            }
        )

    def post(self, *args, **kwargs) -> None:
        raise Http404()
