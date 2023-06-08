from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from dashboard.forms.login_form import LoginForm


class HomeView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('login', None)
        form = LoginForm(session)

        return render(
            self.request,
            'dashboard/pages/home.html',
            context={
                'form': form,
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['login'] = post
        form = LoginForm(post)

        if form.is_valid():
            user = authenticate(
                self.request,
                username=post.get('user'),
                password=post.get('password'),
                )

            if user is not None:
                del self.request.session['login']

                # last_login = user.last_login

                login(self.request, user)
                messages.success(
                    self.request,
                    'login realizado com sucesso'
                )
                return redirect(
                    reverse('dashboard:login')
                )

            messages.error(
                self.request,
                'Usuário ou senha incorretos',
            )
            return redirect(
                reverse('dashboard:home')
            )

        return redirect(
            reverse('dashboard:home')
        )


class LoginView(TemplateView):
    template_name = 'dashboard/pages/login.html'
