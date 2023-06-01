from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpRequest
from django.forms import ModelForm
from django.contrib.auth.models import User
from user.forms.user_register_form import UserFormRegister


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
            # criar um password temporário
            # enviar o e-mail de recuperação de senha
            user: User = form.save(commit=False)
            user.set_password(user.password)
            user.save()

            # retornar para uma página de confirmação
            return redirect('user:register_confirmation')

        return redirect('user:register')

    @staticmethod
    def user_register_confirmation(request: HttpRequest):
        session = request.session.get('register_form_data', None)

        if session:
            email = request.session['register_form_data'].get('email')
            del request.session['register_form_data']

            return render(
                request,
                'user/pages/register_confirmation.html',
                context={
                    'message': (
                        f'Um e-mail de confirmação foi enviado para {email}.\n'
                        f'Acesso o link para finalizar seu cadastro.'
                        )
                }
            )

        return render(
            request,
            'user/pages/register_confirmation.html',
            context={
                'message': 'Página não encontrada',
            }
        )
