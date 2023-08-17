from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpRequest
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from utils.tokens.token_generate import account_activation_token

from user.forms.profile_form import ProfileForm
from user.forms.user_register_form import UserFormRegister
from user.models import Profile

from django.conf import settings


def email_activation(request, user, to_email):
    mail_subject = 'Ativação de conta'
    message = render_to_string(
        'user/pages/template_activate_account.html',
        {
            'user': str(user.first_name).capitalize(),
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http',
        },
        )
    try:
        send_mail(mail_subject,
                  message,
                  from_email='guilherme.partic@gmail.com',
                  recipient_list=[to_email],
                  auth_user=settings.EMAIL_HOST_USER,
                  fail_silently=False,
                  )
        messages.success(
            request,
            (
                f'Prezado(a) {str(user.first_name).capitalize()}. '
                f'Um email de confirmação foi enviado para '
                f'{to_email}. '
                'Acesse o link para ativar sua conta. Caso não tenha recebido '
                'o email, verifique sua caixa de spam.'
            )
        )
    except Exception as e:
        messages.error(
            request,
            (
                f'{e}. Houve um problema ao enviar o email de ativação '
                f'para {to_email}. '
                'Verifique se digitou o email corretamente.')
        )


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request,
            (
                'Obrigado por confirmar seu e-mail. '
                'Agora você pode fazer login em sua conta.'
                )
        )
        return redirect(
            reverse('dashboard:home')
        )
    else:
        messages.error(
            request,
            'Este link de ativação é inválido'
        )
        return redirect(
            reverse('dashboard:home')
        )


class UserRegister(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        register_form_data: dict | None = self.request.session.get(
            'register_form_data',
            None,
            )
        form: ModelForm = UserFormRegister(register_form_data)

        return render(self.request,
                      'user/pages/register.html',
                      context={
                          'form': form,
                          'form_action': reverse('user:register_create')
                          },
                      )

    def post(self, *args, **kwargs) -> HttpResponse:
        post: dict = self.request.POST
        self.request.session['register_form_data']: dict = self.request.POST
        form: ModelForm = UserFormRegister(post)

        if form.is_valid():
            user: User = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.is_active = False
            user.save()
            email_activation(
                self.request, user, form.cleaned_data.get('email')
                )

            del self.request.session['register_form_data']
            return redirect('user:register_confirmation')

        return redirect('user:register')

    @staticmethod
    def user_register_confirmation(request: HttpRequest):
        return render(
            request,
            'user/pages/register_confirmation.html'
        )


@method_decorator(login_required(
    redirect_field_name='next',
    login_url='/',
        ),
    name='dispatch'
)
class CreateProfile(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user
        profile = Profile.objects.filter(user=user).exists()

        if not profile:
            session = self.request.session.get('create_profile', None)
            form = ProfileForm(session)
            messages.success(
                self.request,
                (
                    'Antes de continuarmos, vamos configurar '
                    'seu perfil de usuário.'
                )
            )

            return render(
                self.request,
                'user/pages/create_profile.html',
                context={
                    'form': form,
                    'form_title': 'Configurar perfil',
                    'button_submit_value': 'finalizar'
                }
            )

        return redirect(
            reverse('dashboard:user_dashboard')
        )

    def post(self, *args, **kwargs):
        post = self.request.POST
        self.request.session['create_profile'] = post
        form = ProfileForm(post)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = self.request.user
            profile.save()

            messages.success(
                self.request,
                ('Perfil criado com sucesso.')
            )

            del self.request.session['create_profile']

            return redirect(
                reverse('dashboard:user_dashboard')
            )

        return redirect(
            reverse('user:create_profile')
        )
