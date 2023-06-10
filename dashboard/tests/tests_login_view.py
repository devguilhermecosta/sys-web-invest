from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from dashboard.models import Profile
from parameterized import parameterized


class LoginViewTests(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'jhondoe',
            'email': 'jhon@email.com',
            'password': 'jhon123',
        }

        self.c = Client()
        return super().setUp()

    @parameterized.expand([
        ('user', 'Campo obrigatório'),
        ('password', 'Campo obrigatório'),
    ])
    def test_login_view_returns_message_error_if_fields_length_igual_zero(self, field, message) -> None:  # noqa: E501
        self.user_data[field] = ''
        c = Client()

        response = c.post(
            reverse('dashboard:home'),
            data=self.user_data,
            follow=True,
        )

        self.assertIn(message, response.content.decode('utf-8'))
        self.assertRedirects(response, '/', 302)

    def test_login_view_returns_invalid_user_if_the_credentials_are_incorrects(self) -> None:  # noqa: E501
        response = self.c.post(
            reverse('dashboard:home'),
            {
                'user': self.user_data['username'],
                'password': 'any',
            },
            follow=True,
        )
        self.assertIn(
            'Usuário ou senha incorretos',
            response.content.decode('utf-8'),
        )
        self.assertRedirects(response, '/', 302)

    def test_login_view_returns_login_succesfully_if_credentials_are_correct_and_user_i_activate(self) -> None:  # noqa: E501
        '''
            This test create a new user and make login,
            however, the user need have a profile.
        '''

        user = User.objects.create_user(
            **self.user_data
        )

        Profile.objects.create(user=user)

        response = self.c.post(
            reverse('dashboard:home'),
            {
                'user': self.user_data['username'],
                'password': self.user_data['password'],
            },
            follow=True,
        )

        self.assertIn('login realizado com sucesso',
                      response.content.decode('utf-8'),
                      )
        self.assertRedirects(response,
                             reverse('dashboard:user_dashboard'),
                             302,
                             )
