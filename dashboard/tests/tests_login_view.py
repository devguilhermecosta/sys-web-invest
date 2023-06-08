from django.test import TestCase
from django.test import Client
from django.urls import reverse
from parameterized import parameterized


class LoginViewTests(TestCase):
    def setUp(self):
        self.user_data = {
            'user': 'user',
            'password': 'password',
        }
        return super().setUp()

    @parameterized.expand([
        ('user', 'Campo obrigatório'),
        ('password', 'Campo obrigatório'),
    ])
    def test_login_form_returns_message_error_if_fields_length_igual_zero(self, field, message) -> None:  # noqa: E501
        self.user_data[field] = ''
        c = Client()

        response = c.post(
            reverse('dashboard:home'),
            data=self.user_data,
            follow=True,
        )

        self.assertIn(message, response.content.decode('utf-8'))
        self.fail(
            'continuar a partir daqui. '
            'Testar a url, view, status_code, etc.'
            )
