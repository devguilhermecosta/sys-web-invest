from django.test import TestCase
from django.urls import reverse
from . import (
    password_reset_complete_url_name,
    password_reset_confirm_url_name,
    password_reset_done_url_name,
    password_reset_url_name
)


class ResetPasswordUrlsTests(TestCase):
    def test_password_reset_url_is_correct(self) -> None:
        url: str = reverse(password_reset_url_name)
        self.assertEqual(url, '/password/password_reset/')

    def test_password_reset_done_urls_is_correct(self) -> None:
        url: str = reverse(password_reset_done_url_name)
        self.assertEqual(url, '/password/password_reset/done/')

    def test_password_reset_confirm_url_is_correct(self) -> None:
        url: str = reverse(password_reset_confirm_url_name,
                           args=('mDx', 'aBty12357'))
        self.assertEqual(url, '/password/reset/mDx/aBty12357/')

    def test_password_reset_complet_url_is_correct(self) -> None:
        url: str = reverse(password_reset_complete_url_name)
        self.assertEqual(url, '/password/reset/done/')
