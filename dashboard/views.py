from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from dashboard.forms.login_form import LoginForm
from user.models import Profile


class LoginView(View):
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
                profile = Profile.objects.filter(user=user).exists()
                login(self.request, user)

                if not profile:
                    return redirect(
                        reverse('user:create_profile')
                        )

                messages.success(
                    self.request,
                    'login realizado com sucesso'
                )
                return redirect(
                    reverse('dashboard:user_dashboard')
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


class LogoutView(View):
    def post(self, *args, **kwargs):
        logout(self.request)

        messages.warning(
            self.request,
            'Logout realizado com sucesso'
        )

        return redirect(
            reverse('dashboard:home')
        )


class DashboardView(TemplateView):
    template_name = 'dashboard/pages/dashboard.html'
