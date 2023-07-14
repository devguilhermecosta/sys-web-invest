from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.tests.base_tests import make_fixed_income_product
from parameterized import parameterized
from product.models import ProductFixedIncome


class FixedIncomeEditTests(TestCaseWithLogin):
    url = reverse('product:fixed_income_edit', args=('1',))

    def test_fixed_income_edit_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/renda-fixa/1/editar/')

    def test_fixed_income_edit_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FixedIncomeEditView,
        )

    def test_fixed_income_edit_returns_status_code_302_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/renda-fixa/1/editar/',
            302,
        )

    def test_fixed_income_edit_returns_status_code_404_if_object_not_found(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # get request
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_fixed_income_edit_returns_status_code_200_if_object_found(self) -> None:  # noqa: E501
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

    def test_fixed_income_edit_loads_correct_template(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create product fixed income
        make_fixed_income_product(user=user)

        # get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/pages/fixed_income/fixed_income_edit.html',
        )

    @parameterized.expand([
        ('cdb'),
        ('cdb bb 2035'),
        ('1250'),
        ('2023-07-04'),
        ('2035-01-01'),
        ('no vencimento'),
        ('102% cdi'),
        ('não há'),
        ('cdb muito legal'),
    ])
    def test_fixed_income_edit_loads_correct_content(self, text: str) -> None:  # noqa: E501
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

    @parameterized.expand([
        ('category', 'Campo obrigatório'),
        ('name', 'Campo obrigatório'),
        ('value', 'Campo obrigatório'),
        ('grace_period', 'Campo obrigatório'),
        ('maturity_date', 'Campo obrigatório'),
        ('liquidity', 'Campo obrigatório'),
        ('profitability', 'Campo obrigatório'),
        ('interest_receipt', 'Campo obrigatório'),
    ])
    def test_fixed_income_edit_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create product fixed income
        make_fixed_income_product(user=user)

        # product data
        product_data = {
            field: '',
        }

        # try save the produtct
        response = self.client.post(
            self.url,
            product_data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content,
        )
        self.assertIn(
            'Verifique os dados abaixo',
            content,
        )

    def test_fixed_income_edit_returns_success_messages_if_product_is_saved(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create product fixed income
        make_fixed_income_product(user=user)

        # product data
        # original name = 'cdb bb 2035'
        product_data = {
            'category': 'cdb',
            'name': 'outro cdb qualquer',
            'value': 1250,
            'grace_period': '2023-07-04',
            'maturity_date': '2035-01-01',
            'liquidity': 'no vencimento',
            'profitability': '102% cdi',
            'interest_receipt': 'não há',
            'description': 'cdb muito legal'
        }

        # try save the produtct
        response = self.client.post(
            self.url,
            product_data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Salvo com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/renda-fixa/1/detalhes/',
            302,
        )

        # checks if the data has been changed
        product_changed = ProductFixedIncome.objects.all()
        self.assertEqual(product_changed[0].name, 'outro cdb qualquer')
