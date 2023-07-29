from utils.mixins.auth import TestCaseWithLogin
from django.urls import reverse, resolve
from product import views
from product.tests.base_tests import make_user_fii


class FIISProfitsHistoryTests(TestCaseWithLogin):
    url = reverse('product:fii_history_json')

    def test_fiis_profits_history_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/fiis/gerenciar-proventos/historico/json/'
        )

    def test_fiis_profits_history_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertEqual(
            response.func.view_class,
            views.FIIManageIncomeReceiptHistory,
        )

    def test_fiis_profits_history_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/fiis/gerenciar-proventos/historico/json/',
            302,
        )

    def test_fiis_profits_history_is_allowed_if_user_is_authenticated(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_fiis_profits_history_returns_status_code_404_if_not_get_request(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_fiis_profits_history_returns_a_json_response_with_correct_data(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # make the user fii
        user_fii = make_user_fii(
            user=user,
            qty=1,
            unit_price=10,
            code='mxrf11',
            desc='maxi renda',
        )

        # data
        data = {
            'user_product_id': user_fii.pk,
            'date': '2023-07-02',
            'value': 4.96,
        }

        # make post request for save the profits
        self.client.post(
            reverse('product:fiis_manage_income'),
            data=data,
        )

        # make get request
        response = self.client.get(self.url)

        self.assertIn(
            ('{"data": [{"date": "2023-07-02", '
             '"history_id": 1, "product": "mxrf11", '
             '"value": 4.96, "handler": "profits"}]}'
             ),
            response.content.decode('utf-8')
        )
