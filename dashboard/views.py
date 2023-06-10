from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from dashboard.forms.login_form import LoginForm
from dashboard.forms.profile_form import ProfileForm
from dashboard.models import Profile


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
                profile = Profile.objects.filter(user=user).first()
                login(self.request, user)

                if profile is None:
                    return redirect(
                        reverse('dashboard:create_profile')
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


@method_decorator(login_required(
    redirect_field_name='next',
    login_url='/',
        ),
    name='dispatch'
)
class CreateProfile(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user.is_authenticated or None
        profile = Profile.objects.filter(user=user).first()

        if not profile:
            form = ProfileForm()
            messages.success(
                self.request,
                (
                    'Antes de continuarmos, vamos configurar '
                    'seu perfil de usuário.'
                )
            )

            return render(
                self.request,
                'dashboard/pages/profile.html',
                context={
                    'form': form,
                    'form_title': 'configurar perfil',
                    'button_submit_value': 'finalizar'
                }
            )

        return redirect(
            reverse('dashboard:user_dashboard')
        )


class LoginView(TemplateView):
    template_name = 'dashboard/pages/login.html'
