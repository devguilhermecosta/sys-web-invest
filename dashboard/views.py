from django.views import View
from django.http import HttpResponse
from django.shortcuts import render


class HomeView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        return render(
            self.request,
            'dashboard/pages/home.html'
        )
