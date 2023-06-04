from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponse
from . import (
    password_reset_complete_url_name,
    password_reset_confirm_url_name,
    password_reset_done_url_name,
    password_reset_url_name
)


class PasswordResetTemplatesTests(TestCase):
    def test_password_reset_loads_correct_template(self) -> None:
        response: HttpResponse = self.client.get(
            reverse(password_reset_url_name)
        )
        self.assertTemplateUsed(
            response,
            'resetpassword/pages/password_reset.html'
        )

    def test_password_reset_done_loads_correct_template(self) -> None:
        response: HttpResponse = self.client.get(
            reverse(password_reset_done_url_name)
        )
        self.assertTemplateUsed(
            response,
            'resetpassword/pages/password_reset_done.html'

        )

    def test_password_reset_confirm_loads_correct_template(self) -> None:
        response: HttpResponse = self.client.get(
            reverse(password_reset_confirm_url_name,
                    args=('mDx', 'aBcd1234'))
        )
        self.assertTemplateUsed(
            response,
            'resetpassword/pages/password_reset_confirm.html'
        )

    def test_password_reset_complete_loads_correct_template(self) -> None:
        response: HttpResponse = self.client.get(
            reverse(password_reset_complete_url_name)
        )
        self.assertTemplateUsed(
            response,
            'resetpassword/pages/password_reset_complet.html',
        )
