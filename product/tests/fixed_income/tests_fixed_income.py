from utils.mixins.auth import TestCaseWithLogin
from django.urls import reverse, resolve
from ...views.fixed_income import FixedIncomeView
from product.tests.base_tests import make_fixed_income_product
from product.models import ProductFixedIncome
from parameterized import parameterized


class FixedIncomeTests(TestCaseWithLogin):
    url = reverse('product:fixed_income')

    def test_fixed_income_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/renda-fixa/')

    def test_fixed_income_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(response.func.view_class, FixedIncomeView)

    def test_fixed_income_returns_status_code_302_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/renda-fixa/',
            302,
        )

    def test_fixed_income_returns_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fixed_income_returns_status_code_405_if_not_get_request(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_fixed_income_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'product/pages/fixed_income/fixed_income.html',
        )

    def test_fixed_income_loads_no_registered_product_if_user_has_no_products(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.get(self.url)

        self.assertIn(
            'nenhum produto cadastrado',
            response.content.decode('utf-8'),
        )

    @parameterized.expand([
        ('cdb bb 2035'),
        ('R$ 1250,00'),
        ('01/01/2035'),
    ])
    def test_fixed_income_loads_correct_content_if_user_has_products(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create object
        make_fixed_income_product(user=user)

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        # get queryset
        queryset = ProductFixedIncome.objects.filter(
            user=user
        )

        self.assertIn(
            text,
            content
        )
        self.assertEqual(len(queryset), 1)

    def test_fixed_income_loads_just_products_of_authenticated_user(self) -> None:  # noqa: E501
        self.fail('continuar daqui')
