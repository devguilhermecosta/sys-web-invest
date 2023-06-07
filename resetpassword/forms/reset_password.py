from django.contrib.auth.forms import PasswordResetForm
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from user.forms.user_register_form import strong_password


class PasswordResetCustomForm(PasswordResetForm):
    email = forms.CharField(
        required=True,
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'C-login_input',
            }
        ),
        error_messages={
            'required': 'Campo obrigatório',
        }
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()

        if not user:
            raise ValidationError(
                ('Nenhum usuário cadastrado com este e-mail'),
                code='invalid'
            )
        return email


class SetPasswordCustomForm(forms.Form):
    new_password1 = forms.CharField(
        label='nova senha',
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'C-login_input',
                }
            ),
        strip=False,
        help_text=(
            'A senha precisa ter pelo menos 8 digitos',
            ),
    )
    new_password2 = forms.CharField(
        label='repita a senha',
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'autocomplete': 'new-password',
                'class': 'C-login_input',
                }
            ),
        validators=[strong_password, ]
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                ('As senhas precisam ser iguais.'),
                code='invalid',
            )
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
