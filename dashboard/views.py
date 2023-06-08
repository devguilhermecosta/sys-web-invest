from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from dashboard.forms.login_form import LoginForm
from dashboard.forms.profile_form import ProfileForm


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

                login(self.request, user)

                if user.last_login is None:
                    messages.success(
                        self.request,
                        ('Este é seu primeiro acesso.'
                         'Antes de continuar, vamos configurar seu perfil.')
                    )
                    return redirect(
                        reverse('dashboard:create_profile')
                    )

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


# marcar como login_required
class CreateProfile(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        form = ProfileForm()

        return render(
            self.request,
            'dashboard/pages/profile.html',
            context={
                'form': form,
                'form_title': 'configurar perfil',
                'button_submit_value': 'finalizar'
            }
        )


class LoginView(TemplateView):
    template_name = 'dashboard/pages/login.html'
