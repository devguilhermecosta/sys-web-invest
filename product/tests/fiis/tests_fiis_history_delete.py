from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.models import FiiHistory
from product.tests.base_tests import make_user_fii


class FiisHistoryDeleteTests(TestCaseWithLogin):
    url = reverse(
        'product:fiis_history_delete',
        kwargs={
            'p_id': 1,
            'h_id': 1,
        })

    def test_fiis_history_delete_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/fiis/1/historico/1/deletar/',
            302,
        )

    def test_fiis_history_delete_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FiisHistoryDeleteView,
        )

    def test_fiis_history_delete_returns_status_code_404_if_get_request(self) -> None:  # noqa: E501
        # make get request
        self.make_login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_fiis_history_delete_returns_status_code_302_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make post request whiout is logged in
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/fiis/1/historico/1/deletar/',
            302,
            )

    def test_fiis_history_delete_returns_status_code_404_if_the_history_does_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make post request whiout an existing history
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_fiis_history_delete_returns_status_code_404_if_the_history_belogns_to_another_user(self) -> None:  # noqa: E501
        # create the another user
        another_user = self.create_user(username='jhon',
                                        email='jhon@email.com',
                                        )

        # create the history
        p = make_user_fii(user=another_user,
                          code='mxrf11',
                          desc='maxi renda',
                          create_history=True,
                          )

        # checks if the history has been created
        history = FiiHistory.objects.filter(userproduct=p)
        self.assertEqual(len(history), 1)

        # make login with user=user
        self.make_login()

        # tries delete the history that belongs to another_user
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_fiis_history_delete_remove_the_history_from_data_base(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the history
        p = make_user_fii(user=user,
                          code='mxrf11',
                          desc='maxi renda',
                          create_history=True,
                          )

        # checks if the history has been created
        history = FiiHistory.objects.filter(userproduct=p)
        self.assertEqual(len(history), 1)

        # make post request
        self.client.post(self.url)

        # checks if the history exists
        # the length must be zero
        history = FiiHistory.objects.filter(userproduct=p)
        self.assertEqual(len(history), 0)

    def test_fiis_history_delete_returns_success_message_if_the_history_is_removed_from_data_base(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the history
        make_user_fii(user=user,
                      code='mxrf11',
                      desc='maxi renda',
                      create_history=True,
                      )

        # make post request
        response = self.client.post(self.url, follow=True)

        self.assertIn(
            'histórico deletado com sucesso',
            response.content.decode('utf-8'),
        )

        self.assertRedirects(
            response,
            '/ativos/fiis/mxrf11/',
            302,
        )
