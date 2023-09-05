from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from . import (
    password_reset_confirm_url_name,
    password_reset_url_name
)


'''
It's not possible to abstract the get and post requests into
separate methods, as the tests did not work.
'''


class PasswordResetCompletTests(TestCase):
    def setUp(self) -> None:
        # Simulate a client
        self.c = Client()

        # Creating a new user
        self.user_data: dict = {
            'first_name': 'Jhon',
            'last_name': 'Dhoe',
            'username': 'jhondoe',
            'email': 'jhon@email.com',
            'password': 'Jhon123@',
        }
        self.user: User = User.objects.create(**self.user_data)
        self.user.save()
        return super().setUp()

    def test_password_reset_returns_campo_obrigatório_if_not_email(self) -> None:  # noqa: E501
        '''When the user tries to recover the password
        without informing the email, an exception
        is raised'''
        response = self.c.post(
            reverse(password_reset_url_name),
            {
                'email': '',
            }
        )
        content = response.content.decode('utf-8')
        self.assertIn('Campo obrigatório', content)

    def test_password_reset_returns_a_message_error_if_user_not_found(self) -> None:  # noqa: E501
        '''If user not found by email, a message error is raised'''
        response = self.client.post(
            reverse(password_reset_url_name),
            {
                'email': 'jhondoe@email.com',
            }
        )
        content = response.content.decode('utf-8')
        self.assertIn(
            'Nenhum usuário cadastrado com este e-mail',
            content,
        )

    def test_password_reset_status_code_302_if_email_ok(self) -> None:
        '''This test checks of the url was redirected.
        Check destination url and the status code.'''
        response = self.c.post(
            reverse(password_reset_url_name),
            {
                'email': self.user.email,
            },
            follow=True,
        )
        self.assertEqual(
            response.redirect_chain[0][1], 302
        )
        self.assertEqual(
            response.redirect_chain[0][0],
            '/password/password_reset/done/'
        )

    def test_password_reset_returns_a_success_message_if_email_swas_sent(self) -> None:  # noqa: E501
        response = self.c.post(
            reverse(password_reset_url_name),
            {
                'email': self.user.email,
            },
            follow=True,
        )
        content = response.content.decode('utf-8')
        self.assertIn(
            (
                'Você receberá as instruções necessárias para '
                'a redefinição de sua senha. Se você não receber '
                'o e-mail de recuperação de senha, por favor, '
                'verifique se digitou o e-mail correto e verifique '
                'seu spam.'
                ),
            content,
        )

    def make_uid_and_token(self) -> str:
        response = self.c.post(
            reverse(password_reset_url_name),
            {
                'email': self.user.email,
            },
        )
        uid = response.context['uid']
        token = response.context['token']
        return uid, token

    def test_password_reset_password_recovery_url_is_correct(self) -> None:
        '''This test check the url that was sent in
        the email. The url hides the token'''
        uid, token = self.make_uid_and_token()
        response_url_get = self.c.get(
            reverse(
                password_reset_confirm_url_name,
                kwargs={
                    'uidb64': uid,
                    'token': token,
                }),
            )

        self.assertEqual(
            response_url_get.url,
            '/password/reset/MQ/set-password/',
        )

    def test_password_reset_returns_error_messages_if_new_password_is_incorrect(self) -> None:  # noqa: E501
        '''
        You need to use the url generated in the get request with
        argument (path) for the post request because of the token.

        Must return error message if:
        - password length is less then 8 chars,
        - password doesn't have at least an uppercase letter,
        a lowercase letter, and a number'''
        uid, token = self.make_uid_and_token()

        response_url_get = self.client.get(
            reverse(
                password_reset_confirm_url_name,
                kwargs={
                    'uidb64': uid,
                    'token': token,
                }),
        )
        response_url_post = self.client.post(
                response_url_get.url,
                {
                    'new_password1': 'abc',
                    'new_password2': 'abdd',
                }
                )

        content = response_url_post.content.decode('utf-8')
        self.assertIn('A senha precisa ter pelo menos 8 catacteres',
                      content
                      )
        self.assertIn('Pelo menos uma letra maíscula', content)
        self.assertIn('Pelo menos uma letra minúscula', content)
        self.assertIn('Pelo menos um número.', content)

    def test_password_reset_returns_error_message_if_passwords_are_different(self) -> None:  # noqa: E501
        '''
        You need to use the url generated in the get request with
        argument (path) for the post request because of the token.
        Returns "The passwords must be equal." '''
        uid, token = self.make_uid_and_token()

        response_url_post = self.client.get(
            reverse(
                password_reset_confirm_url_name,
                kwargs={
                    'uidb64': uid,
                    'token': token,
                }),
        )

        response_url_post = self.client.post(
                response_url_post.url,
                {
                    'new_password1': 'Abcd123456',
                    'new_password2': 'Abcd12345678',
                }
                )

        content = response_url_post.content.decode('utf-8')
        self.assertIn('As senhas precisam ser iguais.', content)

    def test_password_reset_returns_message_success_if_password_is_changed_succesfully(self) -> None:  # noqa: E501
        '''
        You need to use the url generated in the get request with
        argument (path) for the post request because of the token.
        It's necessary to uses follow=True for message success test.
        '''
        uid, token = self.make_uid_and_token()

        response_url_post = self.client.get(
            reverse(
                password_reset_confirm_url_name,
                kwargs={
                    'uidb64': uid,
                    'token': token,
                }),
        )

        new_password = 'Abcd123456'
        response_url_post = self.client.post(
                response_url_post.url,
                {
                    'new_password1': new_password,
                    'new_password2': new_password,
                },
                follow=True,
                )

        user = User.objects.first()

        content = response_url_post.content.decode('utf-8')
        self.assertIn('Sua senha foi alterada com sucesso.', content)
        self.assertTrue(user.check_password(new_password))
