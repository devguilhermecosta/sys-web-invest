from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.tests.base_tests import create_profits_history
from product.models import FiiHistory


class FIIReceiptProfitsDeleteHistory(TestCaseWithLogin):
    url = reverse(
        'product:fii_manage_income_receipt_delete', args=(1,)
        )

    def test_fii_profits_receipt_delete_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/fiis/gerenciar-proventos/historico/1/deletar/',
        )

    def test_fii_profits_receipt_delete_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FIIManageIncomeReceiptDeleteHistory,
        )

    def test_fii_profits_receipt_delete_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/fiis/gerenciar-proventos/historico/1/deletar/',
            302,
        )

    def test_fii_profits_receipt_delete_returns_status_code_404_if_get_request(self) -> None:  # noqa: E501
        # make login and create a history
        create_profits_history(self.client, self.make_login)

        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            404
        )

    def test_fii_profits_receipt_delete_returns_status_code_404_if_the_history_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make post request without the history
        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            404
        )

    def test_fii_profits_receipt_delete_remove_the_userfii_profits_history(self) -> None:  # noqa: E501
        # make login and create a history
        new = create_profits_history(
            self.client,
            self.make_login,
            code='brcr11',
            desc='brcr11',
            value=150,
            )

        # checks if the history has been created
        history = FiiHistory.objects.filter(
            userproduct=new['user_fii'],
            handler='profits',
        )

        self.assertEqual(
            len(history),
            1
        )
        self.assertIn(
            'lucros de 1 unidade(s) de brcr11 do usuário user',
            str(history.first()),
        )
        self.assertEqual(
            history.first().total_price,
            150,
        )

        # remove the history
        response = self.client.post(
            self.url
        )

        # checks if the page has been redirect
        self.assertRedirects(
            response,
            '/ativos/fiis/gerenciar-proventos/',
            302,
        )

        # get again the history
        history = FiiHistory.objects.filter(
            userproduct=new['user_fii'],
            handler='profits',
        )

        # checks if the history has been deleted
        self.assertEqual(
            len(history),
            0
        )

# criar um hash para o id de cada produto
# pois podemos deletar produtos de outros
# usuários através do console do Google
