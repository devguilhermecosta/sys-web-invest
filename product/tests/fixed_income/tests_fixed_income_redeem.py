from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product.views.fixed_income import FixedIncomeRedeemView
from product.tests.base_tests import make_fixed_income_product
from product.models import ProductFixedIncome, FixedIncomeHistory
from parameterized import parameterized


class FixedIncomeRedeemTests(TestCaseWithLogin):
    url = reverse('product:fixed_income_redeem', args=(1,))

    def test_fixed_income_redeem_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/renda-fixa/1/resgatar/')

    def test_fixed_income_redeem_uses_corret_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(response.func.view_class, FixedIncomeRedeemView)

    def test_fixed_income_redeem_returns_status_code_302_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/renda-fixa/1/resgatar/',
            302,
        )

    def test_fixed_income_redeem_returns_status_code_404_if_not_post_request(self) -> None:  # noqa: E501
        _, user = self.make_login()

        make_fixed_income_product(user=user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_fixed_income_redeem_returns_status_code_404_if_product_not_exists(self) -> None:  # noqa: E501
        self.make_login()

        # make post request without registered product
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    @parameterized.expand([
        ('date', 'Campo obrigatório'),
        ('value', 'Campo obrigatório'),
    ])
    def test_fixed_income_redeem_returns_error_message_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the fixed income product
        make_fixed_income_product(user=user)

        # data
        data = {
            field: '',
        }

        # make post request without value
        response = self.client.post(
            self.url,
            data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            field,
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/renda-fixa/1/detalhes/',
            302,
        )

    def test_fixed_income_redeem_returns_error_message_if_value_field_is_biger_then_product_value(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the fixed income product with value equal 100
        make_fixed_income_product(user=user, value=100)

        # make post request with value 101
        response = self.client.post(
            self.url,
            {
                'date': '2023-07-02',
                'value': 101,
            },
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Saldo insuficiente para resgate',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/renda-fixa/1/detalhes/',
            302,
        )

    def test_fixed_income_redeem_returns_success_message_if_value_field_is_ok(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the fixed income product
        make_fixed_income_product(user=user, value=10)

        # make post request with value equal 10
        response = self.client.post(
            self.url,
            {
                'date': '2023-07-02',
                'value': 10,
            },
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Resgate realizado com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/renda-fixa/1/detalhes/',
            302,
        )

    def test_fixed_income_redeem_decreases_the_value_of_the_object_if_form_is_ok(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the product fixed income with value equal 100
        make_fixed_income_product(user=user, value=100)

        # make post request with value 99
        self.client.post(
            self.url,
            {
                'date': '2023-07-02',
                'value': 99,
            },
            follow=True,
        )

        # get object
        product = ProductFixedIncome.objects.get(id=1)

        # checks if the product value is 1
        self.assertEqual(product.get_current_value(), 1)

    def test_fixed_income_redeem_creates_a_history(self) -> None:
        # make login
        _, user = self.make_login()

        # create the product fixed income
        product = make_fixed_income_product(user=user, value=100)

        # make post request with value 100
        self.client.post(
            self.url,
            {
                'date': '2023-07-02',
                'value': 100,
            },
            follow=True,
        )

        # get history
        history = FixedIncomeHistory.objects.filter(
            product=product,
        )

        # cheks if the history has been created.
        # the history length is 2 because when the product
        # is created by the make_fixed_income_product function
        # the apply() method is called.
        self.assertEqual(len(history), 2)
        self.assertEqual(history[1].get_final_value(), -100)
        self.assertEqual(history[1].state, 'redeem')
