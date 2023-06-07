from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from . import (
    password_reset_confirm_url_name,
    password_reset_url_name
)
from utils.browser.selenium import make_chrome_browser
from selenium.webdriver.common.by import By
import pytest


@pytest.mark.functional_test
class ResetPasswordFunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        # Simulate a client
        self.c = Client()

        # Making a chrome browser with Selenium
        self.browser = make_chrome_browser()

        # Creating a new User
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

    def tearDown(self) -> None:
        # Quiting a chrome browser
        self.browser.quit()
        return super().tearDown()

    def test_password_reset_change_user_password_succesfully(self) -> None:
        # 1) Sending password recovery email
        response_post = self.client.post(
            reverse(password_reset_url_name), {
                'email': self.user_data['email'],
            },
            )

        # 2) Checking if the password recovery email was sent
        self.assertIn(
            'Redefinição de senha em testserver',
            mail.outbox[0].subject,
            )

        # 3) Then i get the 'uid' and 'token'
        uid: str = response_post.context['uid']
        token: str = response_post.context['token']

        # 4) Now we make a new url password recovery with uid and token
        url_redefinition_password = reverse(password_reset_confirm_url_name,
                                            kwargs={
                                                'uidb64': uid,
                                                'token': token,
                                                },
                                            )

        # Continue with Selenium
        # 5) making a get request using the url above
        self.browser.get(self.live_server_url + url_redefinition_password)

        # 6) Getting the input password and form
        input_new_password1 = self.browser.find_element(By.ID,
                                                        'id_new_password1',
                                                        )
        input_new_password2 = self.browser.find_element(By.ID,
                                                        'id_new_password2',
                                                        )
        form = self.browser.find_element(By.CLASS_NAME, 'C-form_register_form')

        # 7) Setting the new password and making form submit
        new_password: str = 'Password123'
        input_new_password1.send_keys(new_password)
        input_new_password2.send_keys(new_password)
        form.submit()

        # 8) Checking if the password has been reset
        user = User.objects.get(id=self.user.id)
        password_changed: bool = user.check_password(new_password)
        message_succes = self.browser.find_element(By.CLASS_NAME,
                                                   'message_success',
                                                   )
        self.assertTrue(password_changed)
        self.assertEqual(
            message_succes.text,
            'Sua senha foi alterada com sucesso.'
        )
