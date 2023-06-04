# flake8: noqa
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
    def test_password_reset_status_code_200(self) -> None:
        response: HttpResponse = self.client.get(
            reverse(password_reset_url_name)
        )
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_status_code_200(self) -> None:
        response: HttpResponse = self.client.get(
            reverse(password_reset_done_url_name)
        )
        self.assertEqual(response.status_code, 200)

    def test_password_reset_confirm_status_code_200(self) -> None:
        response: HttpResponse = self.client.get(
            reverse(password_reset_confirm_url_name,
                    args=('mDx', 'aBcd1234'))
        )
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_status_code_200(self) -> None:
        response: HttpResponse = self.client.get(
            reverse(password_reset_complete_url_name)
        )
        self.assertEqual(response.status_code, 200)
