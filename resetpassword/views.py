from django.contrib.auth import views
from django.contrib import messages
from .forms.reset_password import (
    PasswordResetCustomForm,
    SetPasswordCustomForm,
    )


class PasswordReset(views.PasswordResetView):
    template_name = 'resetpassword/pages/password_reset.html'
    form_class = PasswordResetCustomForm


class PasswordResetDone(views.PasswordResetDoneView):
    template_name = 'resetpassword/pages/password_reset.html'

    def get(self, *args, **kwargs):
        super_get = super().get(*args, **kwargs)
        messages.success(
            self.request,
            (
                'Você receberá as instruções necessárias para a redefinição '
                'de sua senha. Se você não receber o e-mail de recuperação de '
                'senha, por favor, verifique se digitou o e-mail correto e '
                'verifique seu spam.')
        )
        return super_get


class PasswordResetConfirm(views.PasswordResetConfirmView):
    template_name = 'resetpassword/pages/password_reset_confirm.html'
    form_class = SetPasswordCustomForm


class PasswordResetComplete(views.PasswordResetCompleteView):
    template_name = 'resetpassword/pages/password_reset_confirm.html'

    def get(self, *args, **kwargs):
        super_get = super().get(*args, **kwargs)
        messages.success(
            self.request,
            'Sua senha foi alterada com sucesso.'
        )
        return super_get
