from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from re import compile


def strong_password(password: str) -> None:
    regex = compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            [
                'A senha precisa ter pelo menos 8 catacteres.',
                'Pelo menos uma letra maíscula.',
                'Pelo menos uma letra minúscula.',
                'Pelo menos um número.',
            ],
            code='invalid',
        )


def add_placeholder(field, placeholder):
    f = field.widget.attrs['placeholder'] = placeholder
    return f


def add_css_class(field, class_name):
    f = field.widget.attrs['class'] = class_name
    return f


class UserFormRegister(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    first_name = forms.CharField(
        required=False,
        label='nome',
        error_messages={
            'required': 'Campo obrigatório',
        },
        )
    add_css_class(first_name, 'C-login_input')

    last_name = forms.CharField(
        required=False,
        label='sobrenome',
        )
    add_css_class(last_name, 'C-login_input')

    username = forms.CharField(
        required=False,
        label='usuário',
        )
    add_css_class(username, 'C-login_input')

    email = forms.CharField(
        required=False,
        label='email',
        widget=forms.EmailInput(),
        )
    add_css_class(email, 'C-login_input')

    email_repeat = forms.CharField(
        required=False,
        label='repita seu email',
        widget=forms.EmailInput(),
        )
    add_css_class(email_repeat, 'C-login_input')

    password = forms.CharField(
        required=False,
        label='senha',
        widget=forms.PasswordInput(),
        validators=[strong_password, ],
        )
    add_css_class(password, 'C-login_input')

    password_repeat = forms.CharField(
        required=False,
        label='repita senha',
        widget=forms.PasswordInput(),
        )
    add_css_class(password_repeat, 'C-login_input')

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

        if not f_name:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )

        if len(f_name) < 3 or len(f_name) > 128:
            raise ValidationError(
                ('O nome deve ter entre 3 e 128 caracteres'),
                code='min_max_length'
            )
        return f_name

    def clean_last_name(self):
        l_name = self.cleaned_data["last_name"]

        if not l_name:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )

        if len(l_name) < 3 or len(l_name) > 128:
            raise ValidationError(
                ('O sobrenome deve ter entre 3 e 128 caracteres'),
                code='min_max_length'
            )
        return l_name

    def clean_username(self):
        username = self.cleaned_data["username"]
        username_exists = User.objects.filter(username=username).exists()

        if not username:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )

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

        if not email:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )

        if email_exists:
            raise ValidationError(
                ('Este e-mail já está em uso'),
                code='invalid',
            )
        return email

    def clean_email_repeat(self):
        email_repeat = self.cleaned_data["email_repeat"]

        if not email_repeat:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )
        return email_repeat

    def clean_password(self):
        password = self.cleaned_data["password"]

        if not password:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )
        return password

    def clean_password_repeat(self):
        password_repeat = self.cleaned_data["password_repeat"]

        if not password_repeat:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )
        return password_repeat

    def clean(self, **kwargs) -> Dict[str, Any]:
        super_clean = super().clean()
        email = self.cleaned_data.get('email')
        email_repeat = self.cleaned_data.get('email_repeat')
        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')

        if email is not None and email != email_repeat:
            message = 'Os e-mails precisam ser iguais'
            raise ValidationError(
                {
                    'email': message,
                    'email_repeat': message,
                },
                code='invalid',
            )

        if password is not None and password != password_repeat:
            message = 'As senhas precisam ser iguais'
            raise ValidationError(
                {
                    'password': message,
                    'password_repeat': message,
                },
                code='invalid',
            )
        return super_clean
