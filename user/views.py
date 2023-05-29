from django.views import View
from django.shortcuts import render
from django.http import HttpResponse


class UserRegister(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        return render(
            self.request,
            'user/pages/register.html'
        )
