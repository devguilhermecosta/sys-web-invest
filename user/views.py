from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, Http404
from django.forms import ModelForm
from django.contrib.auth.models import User
from user.forms.user_register_form import UserFormRegister


class UserRegister(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        form = UserFormRegister()

        return render(
            self.request,
            'user/pages/register.html',
            context={
                'form': form
            }
        )


def user_register(request, *args, **kwargs) -> HttpResponse:
    register_form_data = request.session.get('register_form_data',
                                             None,
                                             )
    form = UserFormRegister(register_form_data)

    return render(request,
                  'user/pages/register.html',
                  context={
                      'form': form,
                      'form_action': reverse('user:register_session')
                      },
                  )


def user_create(request, *args, **kwargs):
    if not request.POST:
        raise Http404()

    post: dict = request.POST
    request.session['register_form_data'] = post
    form: ModelForm = UserFormRegister(post)

    if form.is_valid():
        user: User = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        del request.session['register_form_data']
        return redirect(reverse('user:register_create'))

    else:
        return redirect('user:register_create')
