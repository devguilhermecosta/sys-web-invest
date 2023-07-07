from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.tests.base_tests import make_fixed_income_product
from parameterized import parameterized


class FixedIncomeApplyTests(TestCaseWithLogin):
    url = reverse('product:fixed_income_apply', args=('1',))

    def test_fixed_income_apply_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/renda-fixa/1/aplicar/')

    def test_fixed_income_apply_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FixedIncomeApplyView,
        )

    def test_fixed_income_apply_returns_status_code_302_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/renda-fixa/1/aplicar/',
            302,
        )

    def test_fixed_income_apply_returns_status_code_404_if_object_not_found(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # get request
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_fixed_income_apply_returns_status_code_200_if_object_found(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create product fixed income
        make_fixed_income_product(user=user)

        # get request
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_fixed_income_apply_loads_correct_template(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create product fixed income
        make_fixed_income_product(user=user)

        # get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/pages/fixed_income/product_details.html',
        )

    @parameterized.expand([
        ('cdb'),
        ('cdb bb 2035'),
        ('1250'),
        ('04/07/2024'),
        ('01/01/2035'),
        ('no vencimento'),
        ('102% cdi'),
        ('não há'),
        ('cdb muito legal'),
    ])
    def test_fixed_income_apply_loads_correct_content(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create product fixed income
        make_fixed_income_product(user=user)

        # get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )
        self.fail('continuar daqui')
