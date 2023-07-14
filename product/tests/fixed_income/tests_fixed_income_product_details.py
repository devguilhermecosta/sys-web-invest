from django.urls import resolve, reverse
from product.tests.base_tests import make_fixed_income_product
from product.views import FixedIncomeDetailsView
from utils.mixins.auth import TestCaseWithLogin
from parameterized import parameterized


class ProductFixedIncomeEdit(TestCaseWithLogin):
    url = reverse('product:fixed_income_details', args=(1,))

    def test_fixed_income_detail_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/renda-fixa/1/detalhes/')

    def test_fixed_income_details_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(response.func.view_class, FixedIncomeDetailsView)

    def test_fixed_income_details_returns_status_code_302_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/renda-fixa/1/detalhes/',
            302,
        )

    def test_fixed_income_details_returns_status_code_404_if_product_dont_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_fixed_income_details_returns_status_code_200_if_product_exists(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # make product fixed income
        make_fixed_income_product(user=user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fixed_income_details_loads_corret_template(self) -> None:
        # make login
        _, user = self.make_login()

        # make product fixed income
        make_fixed_income_product(user=user)

        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'product/pages/fixed_income/product_details.html',
        )

    @parameterized.expand([
        ('editar',),
        ('CDB',),
        ('CDB BB 2035',),
        ('R$ 1250,00',),
        ('04/07/2023',),
        ('01/01/2035',),
        ('no vencimento',),
        ('102% cdi',),
        ('Não Há',),
        ('Cdb muito legal',),
        ('aplicar',),
        ('resgatar',),
        ])
    def test_fixed_income_details_loads_correct_content(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # make product fixed income
        make_fixed_income_product(user=user)

        # get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )
