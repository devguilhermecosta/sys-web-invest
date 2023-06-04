from django.test import TestCase
from django.urls import reverse, resolve, ResolverMatch
from resetpassword import views
from . import (
    password_reset_complete_url_name,
    password_reset_confirm_url_name,
    password_reset_done_url_name,
    password_reset_url_name
)


class PasswordResetViewsTests(TestCase):
    def test_password_reset_loads_correct_view(self) -> None:
        request: ResolverMatch = resolve(
            reverse(password_reset_url_name),
        )
        self.assertEqual(request.func.view_class, views.PasswordReset)

    def test_password_reset_done_loads_correct_view(self) -> None:
        request: ResolverMatch = resolve(
            reverse(password_reset_done_url_name),
        )
        self.assertEqual(request.func.view_class, views.PasswordResetDone)

    def test_password_reset_confirm_loads_correct_view(self) -> None:
        request: ResolverMatch = resolve(
            reverse(password_reset_confirm_url_name,
                    args=('mDx', 'aBcd123'))
        )
        self.assertEqual(request.func.view_class, views.PasswordResetConfirm)

    def test_password_reset_complete_loads_correct_view(self) -> None:
        request: ResolverMatch = resolve(
            reverse(password_reset_complete_url_name),
        )
        self.assertEqual(request.func.view_class, views.PasswordResetComplete)
