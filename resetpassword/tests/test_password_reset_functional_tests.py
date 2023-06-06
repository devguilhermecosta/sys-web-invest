from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from . import (
    password_reset_confirm_url_name,
    password_reset_url_name
)
from utils.browser.selenium import make_chrome_browser
from selenium.webdriver.common.by import By


class PasswordResetFuncionalTests(StaticLiveServerTestCase):
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
        self.user.save()
        return super().setUp()

    def test_password_reset_change_user_password_succesfully(self) -> None:
        # 1) Calling the reset password view with get
        # This is not necessaty, but, it's good for test
        response_get = self.client.get(
            reverse(password_reset_url_name)
        )
        self.assertEqual(response_get.status_code, 200)

        # 2) Then we post the response with the email
        # If not used with 'email', the status code
        # we will 200, but, it's necessary 302 redirect
        # Then, i check if status code is 302
        # Then i check if the email was sent
        response_post = self.client.post(
            reverse(password_reset_url_name), {
                'email': self.user_data['email'],
            },
            )
        self.assertEqual(response_post.status_code, 302)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            'Redefinição de senha em testserver',
            mail.outbox[0].subject,
            )

        # 3) Then i get the 'uid' and 'token'
        uid: str = response_post.context['uid']
        token: str = response_post.context['token']

        # 4) Now we make a get reverse using the uid and token
        # So i simulate the user by clicking on password reset
        # link sent in the email
        response_url_reset_get = self.client.get(
            reverse(password_reset_confirm_url_name,
                    kwargs={
                        'uidb64': uid,
                        'token': token,
                    }),
            follow=True,
        )
        self.assertEqual(
            response_url_reset_get.status_code,
            200,
            )

        response_url_reset_get = self.client.post(
            reverse(password_reset_confirm_url_name,
                    kwargs={
                        'uidb64': uid,
                        'token': token,
                    }),
            {
                'new_password1': 'NHYU123',
                'new_password2': 'NHYU123',
            }
        )

        # 5) Now we continue with selenium, because the other
        # means do not work
        url_redefinition_password = reverse(password_reset_confirm_url_name,
                                            kwargs={
                                                'uidb64': uid,
                                                'token': token,
                                                },
                                            )
        browser = make_chrome_browser()
        browser.get(self.live_server_url + url_redefinition_password)
        input_new_password1 = browser.find_element(By.ID, 'id_new_password1')
        input_new_password2 = browser.find_element(By.ID, 'id_new_password2')
        form = browser.find_element(By.CLASS_NAME, 'C-form_register_form')
        new_password: str = 'Password123'
        input_new_password1.send_keys(new_password)
        input_new_password2.send_keys(new_password)
        form.submit()

        # 6) Checking if the password has been reset
        user = User.objects.get(id=self.user.id)
        password_changed: bool = user.check_password(new_password)
        message_succes = browser.find_element(By.CLASS_NAME, 'message_success')
        self.assertTrue(password_changed)
        self.assertEqual(
            message_succes.text,
            'Sua senha foi alterada com sucesso.'
        )

        # quit de broser
        browser.quit()
        self.fail(
            'testar as mensagens de erro durante a recuperação de senha. '
            'testar as mesanges usando métodos sem follow. '
            'registrar que, usando follow temos acesso às messages, '
            'e sem follow temos acesso aos kwargs (uid e token). '
            'registrar todo o processo de teste de recuperação de senha. '
            )
