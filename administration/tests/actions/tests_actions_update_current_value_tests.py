import pytest
from django.urls import resolve, reverse
from selenium.webdriver.common.by import By

from administration import views
from product.models import Action
from product.tests.base_tests import make_action
from utils.mixins.auth import StaticTestCaseWithLogin, TestCaseWithLogin


class ActionsCurrentValueUpdateTests(TestCaseWithLogin):
    url = reverse('admin:update_actions_prices')

    def test_actions_update_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/painel-de-controle/atualizar/precos/acoes/',
        )

    def test_actions_update_uses_correct_view(self) -> None:
        response = resolve(self.url)

        self.assertIs(
            response.func.view_class,
            views.ActionsUpdateLastCloseView,
        )

    def test_actions_update_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without is logged in
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/?next=/painel-de-controle/atualizar/precos/acoes/',
            302,
        )

    def test_actions_update_is_not_allowed_if_the_user_logged_in_is_not_staff(self) -> None:  # noqa: E501
        # make login with a common user
        self.make_login()

        # make get request a common user (not user staff)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_actions_update_is_allowed_if_the_user_is_authenticated_and_the_user_is_staff(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_actions_update_loads_the_correct_template(self) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'administration/pages/update_prices.html',
        )

    def test_actions_update_loads_the_correct_content(self) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request
        response = self.client.get(self.url)

        self.assertIn(
            'Atualizar valores',
            response.content.decode('utf-8'),
        )

    def test_actions_update_update_the_last_close_property_from_all_actions(self) -> None:  # noqa: E501
        # make login
        self.make_login(is_staff=True)

        # create the action
        make_action('bbas3', 'banco do brasil')

        # checks the action last_close property
        a = Action.objects.get(code='bbas3')
        self.assertEqual(a.last_close, 1)

        # make post request
        self.client.post(self.url, follow=True)

        # checks again the las_close property
        a = Action.objects.get(code='bbas3')
        self.assertTrue(a.last_close > 1)

    def test_actions_update_render_the_success_response(self) -> None:  # noqa: E501
        # make login
        self.make_login(is_staff=True)

        # create the action
        make_action('bbas3', 'banco do brasil')

        # make post request
        response = self.client.post(self.url, follow=True)

        self.assertIn(
            '1 ativos foram atualizados. '
            '0 ativos não puderam ser atualizados. '
            'Ativos que não foram atualizados: [].',
            response.content.decode('utf-8')
        )
        self.assertRedirects(
            response,
            self.url,
            302,
        )


@pytest.mark.functional_test
class ActionsCurrentValueUpdateFunctionalTests(StaticTestCaseWithLogin):
    """ it is necessary the Brapi API for this tests """

    url = reverse('admin:update_actions_prices')

    def test_actions_update_update_the_last_close_property_from_all_actions(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # create the action
        make_action('bbas3', 'banco do brasil')

        # checks the action last_close property
        a = Action.objects.get(code='bbas3')
        self.assertEqual(a.last_close, 1)
        self.assertTrue(a.last_close == 1)

        # access the page for update
        self.browser.get(self.live_server_url + self.url)

        # click on the button of form for update the
        # last_close property of the actions
        button = self.browser.find_element(By.XPATH, '//*[@id="btn-update"]')
        button.click()

        # checks again the last_close property
        a = Action.objects.get(code='bbas3')
        self.assertTrue(a.last_close > 1)

    def test_actions_update_render_the_success_message(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # create the action
        make_action('bbas3', 'banco do brasil')

        # access the page for update
        self.browser.get(self.live_server_url + self.url)

        # click on the button of form for update the
        # last_close property of the actions
        button = self.browser.find_element(By.XPATH, '//*[@id="btn-update"]')
        button.click()

        # get the main element
        main = self.browser.find_element(By.XPATH, '/html/body/main')

        # checks the success message
        self.assertIn(
            '1 ativos foram atualizados. '
            '0 ativos não puderam ser atualizados. '
            'Ativos que não foram atualizados: []. Erros: [],',
            main.text,
        )
