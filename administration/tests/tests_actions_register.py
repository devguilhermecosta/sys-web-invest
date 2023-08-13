from django.urls import resolve, reverse
from parameterized import parameterized

from utils.mixins.auth import TestCaseWithLogin

from .. import views


class ActionsRegisterTests(TestCaseWithLogin):
    url = reverse('admin:action_register')

    def test_action_register_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/painel-de-controle/cadastrar/acao/',
        )

    def test_action_register_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ActionRegister,
        )

    def test_action_register_returns_status_code_302_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without begins logged in
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/painel-de-controle/cadastrar/acao/',
            302,
        )

    def test_action_register_redirects_the_page_to_dashboard_if_the_user_is_not_staff(self) -> None:  # noqa: E501
        # make login with a common user
        self.make_login()

        # make get request without begins logged in
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/dashboard/painel-do-usuario/',
            302,
        )

    def test_action_register_returns_status_code_200_if_the_user_is_staff(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_action_register_loads_correct_template(self) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'administration/pages/product_register.html',
        )

    @parameterized.expand([
        'Registrar nova Ação',
        'código',
        'descrição',
        'cnpj',
        'registrar',
    ])
    def test_action_register_loads_correct_content(self, text: str) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )

    def test_action_register_loads_the_registered_actions(self, text: str) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        self.fail('continuar daqui')
