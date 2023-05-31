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
        label='nome',
        required=True,
        widget=forms.TextInput(),
        error_messages={
            'required': 'Este campo é obrigatório',
        })
    add_css_class(first_name, 'C-login_input')

    last_name = forms.CharField(
        label='sobrenome',
        required=True,
        widget=forms.TextInput(),
        error_messages={
            'required': 'Este campo é obrigatório',
            })
    add_css_class(last_name, 'C-login_input')

    username = forms.CharField(
        label='usuário',
        required=True,
        widget=forms.TextInput(),
        error_messages={
            'required': 'Este campo é obrigatório',
            })
    add_css_class(username, 'C-login_input')

    email = forms.EmailField(
        label='email',
        required=True,
        widget=forms.EmailInput(),
        error_messages={
            'required': 'Este campo é obrigatório',
            })
    add_css_class(email, 'C-login_input')

    email_repeat = forms.EmailField(
        label='repita seu email',
        required=True,
        widget=forms.EmailInput(),
        error_messages={
            'required': 'Este campo é obrigatório',
            })
    add_css_class(email_repeat, 'C-login_input')

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]

    def clean_email(self):
        data = self.cleaned_data["email"]
        user = User.objects.all()

        for u in user:
            if data == u.email:
                raise ValidationError(
                    'Este e-mail já está cadastrado'
                )

        return data


"""
criar a limpeza para todos os fields;
o e-mail deve ser único;
se o registro não for bem sucedido, uma mensagem de erro deve ser levantada;
se for bem sucedido, a primeira senha do usuário será gerada de forma aleatória
e um e-mail com recuperação de senha será enviado para o usuário definir
uma senha.
No primeiro acesso o usuário deverá criar o perfil.
"""
