from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product.views import FIIsView
from product.tests.base_tests import create_profits_history
from parameterized import parameterized


class FIIsTests(TestCaseWithLogin):
    url = reverse('product:fiis')

    def test_fiis_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/fiis/')

    def test_fiis_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertEqual(response.func.view_class, FIIsView)

    def test_fiis_get_request_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/fiis/',
            302,
        )

    def test_fiis_get_request_returns_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fiis_returns_status_code_405_if_not_get_request(self) -> None:
        # make login
        self.make_login()

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_fiis_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'product/pages/fiis/fiis.html',
        )

    @parameterized.expand([
        ('meus FIIs'),
        ('comprar'),
        ('vender'),
        ('gerenciar proventos'),
    ])
    def test_fiis_loads_correct_content(self, text) -> None:
        # make login
        self.make_login()

        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(text, content)

    @parameterized.expand([
        ('Aplicação total'),
        ('Total recebido em proventos'),
        ('R$ 200,00'),
    ])
    def test_fiis_loads_the_summary_of_investments(self, text: str) -> None:
        # make login and create a user_fii and a user history profits
        create_profits_history(
            self.client,
            self.make_login,
            value_aplication=100,
            profits_value=200,
        )

        # make get request
        response = self.client.get(self.url)

        self.assertIn(
            text,
            response.content.decode('utf-8'),
        )
