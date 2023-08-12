from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.tests.base_tests import (
    create_profits_history,
    make_user_fii,
    )
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

    def test_fii_profits_receipt_delete_returns_status_code_404_if_the_logged_in_user_is_different_from_the_history_owner_user(self) -> None:  # noqa: E501
        # create another user
        another_user = self.create_user(
            username='jhondoe',
            email='jhondoe@email.com',
        )

        # create the UserFII for another_user
        another_userfii = make_user_fii(another_user,
                                        'pvbi11',
                                        'teste',
                                        )

        # make login with the another_user
        self.make_login(create_user=False, username=another_user)

        # make post request for create the history for another_userfii
        r_post = self.client.post(
            reverse('product:fiis_manage_income_receipt'),
            {
                'userproduct': another_userfii.id,
                'total_price': 50,
                'date': '2023-07-02',
            },
            follow=True,
        )

        # checks if the history has been created
        self.assertEqual(
            r_post.content.decode('utf-8'),
            '{"success": "success request"}',
        )

        # get the history id
        another_user_history = FiiHistory.objects.filter(
            userproduct=another_userfii,
            handler='profits',
        )

        # checks if the history_id of another_user is 1
        self.assertEqual(
            another_user_history.first().id,
            1
        )

        # make logout with the another_user
        self.client.logout()

        # create the profits history and make login with user=user
        u = create_profits_history(self.client,
                                   self.make_login,
                                   profits_value=150,
                                   )

        # get the history id of user
        history_id_user = FiiHistory.objects.filter(
            userproduct=u['user_fii'],
            handler='profits'
        )

        # checks if the history_id_user is 2
        self.assertEqual(
            history_id_user.first().id,
            2
        )

        # now i am logged in with the user
        # i will try to delete the history of id 1 whose another_user owns
        response = self.client.post(self.url)

        # the status code must be 404
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
            profits_value=150,
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
