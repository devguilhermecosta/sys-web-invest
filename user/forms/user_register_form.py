from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def add_placeholder(field, placeholder):
    f = field.widget.attrs['placeholder'] = placeholder
    return f


def add_css_class(field, class_name):
    f = field.widget.attrs['class'] = class_name
    return f


class UserFormRegister(forms.ModelForm):
    first_name = forms.CharField(
        min_length=3,
        max_length=128,
        label='nome',
        error_messages={
            'required': 'Campo obrigatório',
        },
        )
    add_css_class(first_name, 'C-login_input')

    last_name = forms.CharField(
        min_length=3,
        max_length=128,
        label='sobrenome',
        error_messages={
            'required': 'Campo obrigatório',
        },
        )
    add_css_class(last_name, 'C-login_input')

    username = forms.CharField(
        min_length=4,
        max_length=128,
        label='usuário',
        error_messages={
            'required': 'Campo obrigatório',
        },
        )
    add_css_class(username, 'C-login_input')

    email = forms.CharField(
        label='email',
        widget=forms.EmailInput(),
        error_messages={
            'required': 'Campo obrigatório',
        },
        )
    add_css_class(email, 'C-login_input')

    email_repeat = forms.CharField(
        label='repita seu email',
        widget=forms.EmailInput(),
        error_messages={
            'required': 'Campo obrigatório',
        },
        )
    add_css_class(email_repeat, 'C-login_input')

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

    def clean_first_name(self):
        f_name = self.cleaned_data["first_name"]

        if len(f_name) < 3 or len(f_name) > 128:
            raise ValidationError(
                ('O nome deve ter entre 3 e 128 caracteres'),
                code='min_max_length'
            )
        return f_name

    def clean_last_name(self):
        l_name = self.cleaned_data["last_name"]

        if len(l_name) < 3 or len(l_name) > 128:
            raise ValidationError(
                ('O sobrenome deve ter entre 3 e 128 caracteres'),
                code='min_max_length'
            )
        return l_name

    def clean_username(self):
        username = self.cleaned_data["username"]
        username_exists = User.objects.filter(username=username).exists()

        if len(username) < 4 or len(username) > 128:
            raise ValidationError(
                ('O Usuário deve ter entre 4 e 128 caracteres'),
                code='min_max_length',
            )

        if username_exists:
            raise ValidationError(
                ('Usuário já cadastrado'),
                code='invalid',
            )
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise ValidationError(
                ('Este e-mail já está em uso'),
                code='invalid',
            )
        return email

    def clean(self, **kwargs) -> Dict[str, Any]:
        super_clean = super().clean()
        email = self.cleaned_data.get('email')
        email_repeat = self.cleaned_data.get('email_repeat')

        if email is not None and email != email_repeat:
            message = 'Os e-mails precisam ser iguais'
            raise ValidationError(
                {
                    'email': message,
                    'email_repeat': message,
                },
                code='invalid',
            )
        return super_clean
