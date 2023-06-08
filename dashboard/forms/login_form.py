from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    user = forms.CharField(
        required=False,
        label='usuário',
        widget=forms.TextInput(
            attrs={
                'class': 'C-login_input',
            }
        )
    )
    password = forms.CharField(
        required=False,
        label='senha',
        widget=forms.PasswordInput(
            attrs={
                'class': 'C-login_input',
            }
        )
    )

    def clean_user(self):
        user = self.cleaned_data['user']

        if not user or len(user) <= 0:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )
        return user

    def clean_password(self):
        password = self.cleaned_data['password']

        if not password or len(password) <= 0:
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )
