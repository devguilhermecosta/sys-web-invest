from django.urls import resolve, reverse

from product.tests.base_tests import make_fixed_income_product
from product.views import FixedIncomeHistoryView
from utils.mixins.auth import TestCaseWithLogin
from parameterized import parameterized


class ProductFixedIncomeHistoryTests(TestCaseWithLogin):
    url = reverse('product:fixed_income_history', args=(1,))

    def test_fixed_income_history_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/renda-fixa/1/historico/')

    def test_fixed_income_history_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(response.func.view_class, FixedIncomeHistoryView)

    def test_fixed_income_history_returns_status_code_302_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/renda-fixa/1/historico/',
            302,
        )

    def test_fixed_income_history_returns_404_if_product_dont_exists(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_fixed_income_history_returns_405_if_post_request(self) -> None:
        self.make_login()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_fixed_income_history_returns_status_code_200(self) -> None:
        '''
            the status code must be 200 if user is authenticated and
            the product exists.
        '''
        _, user = self.make_login()

        # make the product fixed income, but this no has a history
        make_fixed_income_product(user=user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_fixed_income_history_loads_correct_template(self) -> None:
        _, user = self.make_login()
        make_fixed_income_product(user=user)
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/partials/_history_dt_and_fi.html',
        )

    @parameterized.expand([
        ('cdb bb 2035'),
        ('valor atual'),
        ('R$ 2900,00'),
        ('R$ -100,00'),
        ('R$ 1000,00'),
        ('aplicação'),
        ('resgate'),
        ('editar'),
        ('deletar'),
    ])
    def test_fixed_income_history_loads_correct_content(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the product fixed income
        make_fixed_income_product(user=user, value=2000)

        # apply the value
        self.client.post(
            reverse('product:fixed_income_apply', args=(1,)),
            {
                'date': '2023-07-02',
                'value': 1000
            },
            follow=True,
        )

        # redeem the value
        self.client.post(
            reverse('product:fixed_income_redeem', args=(1,)),
            {
                'date': '2023-08-01',
                'value': 100,
            },
            follow=True
        )

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )

    def test_fixed_income_history_loads_total_received_in_profits_if_the_product_interest_receipt_property_is_other_than_NÃO_HÁ(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the product fixed income and the apply history
        make_fixed_income_product(user=user,
                                  value=2000,
                                  interest_receipt='mensal',
                                  )

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            'total recebido em juros: R$',
            content,
        )

    def test_fixed_income_history_does_not_loads_total_received_in_profits_if_the_product_interest_receipt_property_is_NÃO_HÁ(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the product fixed income and the apply history
        make_fixed_income_product(user=user,
                                  value=2000,
                                  interest_receipt='não há',
                                  )

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertNotIn(
            'total recebido em juros: R$',
            content,
        )
