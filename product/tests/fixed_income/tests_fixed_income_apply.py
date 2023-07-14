from utils.mixins.auth import TestCaseWithLogin
from django.urls import reverse, resolve
from product.tests.base_tests import make_fixed_income_product
from product.views import FixedIncomeApplyView
from product.models import ProductFixedIncome
from product.models import FixedIncomeHistory


class FixedIncomeApplyTests(TestCaseWithLogin):
    url = reverse('product:fixed_income_apply', args=(1,))

    def test_fixed_income_apply_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/renda-fixa/1/aplicar/')

    def test_fixed_income_apply_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(response.func.view_class, FixedIncomeApplyView)

    def test_fixed_income_apply_returns_status_code_302_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/renda-fixa/1/aplicar/',
            302,
        )

    def test_fixed_income_apply_get_request_returns_status_code_404(self) -> None:  # noqa: E501
        self.make_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_fixed_income_apply_returns_status_code_404_if_product_not_exists(self) -> None:  # noqa: E501
        self.make_login()

        # request without product
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_fixed_income_apply_returns_error_message_if_value_field_is_empty(self) -> None:  # noqa: E501
        _, user = self.make_login()

        # create a product fixed income
        make_fixed_income_product(user=user)

        response = self.client.post(
            self.url,
            {
                'value': '',
            },
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Campo obrigatório',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/renda-fixa/1/detalhes/',
            302,
        )

    def test_fixed_income_apply_returns_success_message_value_field_is_ok(self) -> None:  # noqa: E501
        _, user = self.make_login()

        # create a product fixed income
        make_fixed_income_product(user=user)

        response = self.client.post(
            self.url,
            {
                'value': 10,
            },
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Aplicação realizada com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/renda-fixa/1/detalhes/',
            302,
        )

    def test_fixed_income_apply_increases_the_value_of_the_object(self) -> None:  # noqa: E501
        _, user = self.make_login()

        # create a product fixed income with value iqual 10
        make_fixed_income_product(user=user, value=10)

        # apply plus 90 into value
        self.client.post(
            self.url,
            {
                'value': 90,
            },
            follow=True,
            )

        # get object
        product = ProductFixedIncome.objects.get(id=1)

        # checks if the value is 100
        self.assertEqual(product.value, 100)

    def test_fixed_income_apply_creates_a_history(self) -> None:  # noqa: E501
        _, user = self.make_login()

        # create a product fixed income
        product = make_fixed_income_product(user=user)

        # apply
        self.client.post(
            self.url,
            {'value': 10},
            follow=True,
            )

        # get history
        history = FixedIncomeHistory.objects.filter(
            product=product,
        )

        # cheks if the history has been created
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0].value, 10)
        self.assertEqual(history[0].state, 'apply')
        self.fail('criar a opção de receber juros')
