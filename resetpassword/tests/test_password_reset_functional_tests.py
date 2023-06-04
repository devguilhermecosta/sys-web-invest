from django.test import TestCase
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms.forms import Form
from django.core import mail
from resetpassword.forms import reset_password
from resetpassword import views
from django.conf import settings

from . import (
    password_reset_complete_url_name,
    password_reset_confirm_url_name,
    password_reset_done_url_name,
    password_reset_url_name
)


#  testar o content de cada view


class PasswordResetFuncionalTests(TestCase):
    """
        This test entire set of views required for
        password recovery.
        This is a long test.
    """
    def setUp(self) -> None:
        self.user_data: dict = {
            'first_name': 'Jhon',
            'last_name': 'Dhoe',
            'username': 'jhondoe',
            'email': 'jhon@email.com',
            'password': 'Jhon123@',
        }
        self.user: User = User.objects.create(**self.user_data)
        return super().setUp()

    def test_password_reset_functional_test(self) -> None:
        # 1) Calling the reset password view
        response = self.client.get(
            reverse(password_reset_url_name)
        )

        post = self.client.post(
            reverse(password_reset_url_name), {
                'email': self.user_data['email'],
            })
        ...
        