from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render


class HomeView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        return render(
            self.request,
            'dashboard/pages/home.html'
        )


class LoginView(TemplateView):
    template_name = 'dashboard/pages/login.html'
