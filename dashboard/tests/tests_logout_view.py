from django.urls import resolve, reverse

from dashboard.views import LogoutView
from utils.mixins.auth import TestCaseWithLogin


class LogoutViewTests(TestCaseWithLogin):
    url = reverse('dashboard:logout')

    def test_logout_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/logout/'
        )

    def test_logout_loads_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(response.func.view_class, LogoutView)

    def test_logout_returns_status_code_405_if_get_request(self) -> None:
        ''' 405 - method not allowed '''
        response = self.client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 405)

    def test_logout_returns_message_warning_if_logout_succesfully(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.post(self.url, follow=True)

        self.assertRedirects(
            response,
            '/',
            302,
        )
        self.assertIn(
            'Logout realizado com sucesso',
            response.content.decode('utf-8')
        )
