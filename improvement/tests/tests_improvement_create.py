from utils.mixins.auth import TestCaseWithLogin, StaticTestCaseWithLogin
from selenium.webdriver.common.by import By
from django.urls import reverse, resolve
from django.core import mail
from parameterized import parameterized
from .. import views
from ..models import Improvement
import pytest


class ImprovementCreateTests(TestCaseWithLogin):
    url = reverse('improvement:create')

    def test_improvement_create_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/melhorias/')

    def test_improvement_create_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ImprovementCreate,
        )

    def test_improvement_create_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make post request without is logged in
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/?next=/melhorias/',
            302,
        )

    def test_improvement_create_returns_404_if_get_request(self) -> None:
        # make login
        self.make_login()

        # make ger request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    @parameterized.expand([
        ('user_name'),
        ('user_email'),
        ('subject'),
        ('content'),
    ])
    def test_improvement_create_returns_error_message_if_any_field_is_empty(self, field: str) -> None:  # noqa: E501
        # make login
        self.make_login()

        form_data = {
            field: '',
        }

        response = self.client.post(self.url, data=form_data, follow=True)

        self.assertIn(
            'preencha todos os campos do formulário',
            response.content.decode('utf-8'),
        )
        self.assertRedirects(
            response,
            '/dashboard/painel-do-usuario/',
            302,
        )

    def test_improvement_create_returns_success_message_if_all_field_is_ok(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        form_data = {
            'user_name': user.first_name,
            'user_email': user.email,
            'subject': 'my test',
            'content': 'this is a test message',
        }

        response = self.client.post(self.url, data=form_data, follow=True)

        self.assertIn(
            'Solicitação enviada com sucesso',
            response.content.decode('utf-8'),
        )
        self.assertEqual(
            len(mail.outbox),
            1,
        )
        self.assertRedirects(
            response,
            '/melhorias/minha-lista/',
            302,
        )

    def test_improvement_create_creates_a_new_improvement_object(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # checks the Improvement objects before the post request
        improvements = Improvement.objects.all()
        self.assertEqual(len(improvements), 0)

        form_data = {
            'user_name': user.first_name,
            'user_email': user.email,
            'subject': 'my test',
            'content': 'this is a test message',
        }

        # make post request
        self.client.post(self.url, data=form_data, follow=True)

        # checks again the Improvement objects.
        # Now the length must be 1
        improvements = Improvement.objects.all()
        self.assertEqual(len(improvements), 1)


@pytest.mark.functional_test
class ImprovementCreateFunctionalTests(StaticTestCaseWithLogin):
    def test_improvement_create_returns_a_success_message_if_the_email_is_send(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # click on the button to open the form
        self.browser.find_element(
            By.XPATH, '/html/body/main/div/label[1]'
            ).click()

        # insert the subject message and the content message
        # wait 1 secont before to select the element
        self.wait(1)
        subject = self.browser.find_element(By.XPATH, '//*[@id="subject"]')
        subject.send_keys('testing the subject')
        content = self.browser.find_element(By.XPATH, '//*[@id="content"]')
        content.send_keys('testing the content')

        # get the button submit and ckick
        button = self.browser.find_element(
            By.XPATH, '//*[@id="upgrade_box_button"]',
            )
        button.click()

        # get the message from the page
        message = self.browser.find_element(
            By.XPATH, '/html/body/main/section/p',
            )

        # checks the success message
        self.assertIn(
            'Solicitação enviada com sucesso.',
            message.text,
        )

        # checks the mail outbox
        self.assertEqual(
            len(mail.outbox),
            1,
        )
