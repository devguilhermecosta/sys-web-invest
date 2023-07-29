from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.tests.base_tests import make_user_fii


class FIIsProfitsHistoryEditTests(TestCaseWithLogin):
    url = reverse('product:fii_manage_income_receipt_edit', args=(1,))

    def test_fiis_profits_history_edit_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/fiis/gerenciar-proventos/historico/1/editar/',
        )

    def test_fiis_profits_history_edit_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FIIManageIncomeReceiptEditHistory,
        )

    def test_fiis_profits_history_edit_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/fiis/gerenciar-proventos/historico/1/editar/',
            302,
        )

    def test_fiis_profits_history_edit_returns_status_code_404_if_the_history_not_exists(self) -> None:  # noqa: E501
        self.make_login()

        # make get request without the product
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_fiis_profits_history_returns_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the user fii
        make_user_fii(user, 1, 1, 'mxrf11', 'maxi renda')

        # add a profits
        self.client.post(
            reverse('product:fiis_manage_income_receipt'),
            {
                'user_product_id': 1,
                'value': 10,
                'date': '2023-07-02',
            },
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
