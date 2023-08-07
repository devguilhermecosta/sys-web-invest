from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.tests.base_tests import make_direct_treasure
from product.models import DirectTreasureHistory


class DirectTreasureHistoryDelete(TestCaseWithLogin):
    url = reverse(
        'product:direct_treasure_history_delete',
        kwargs={
            'product_id': 1,
            'history_id': 1,
        })

    def test_direct_treasure_history_delete_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/tesouro-direto/1/historico/1/deletar/',
        )

    def test_direct_treasure_history_delete_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.DirectTreasureHistoryDeleteView,
        )

    def test_direct_treasure_history_delete_returns_302_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/tesouro-direto/1/historico/1/deletar/',
            302,
        )

    def test_direct_treasure_history_delete_returns_404_if_get_request(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_direct_treasure_history_delete_returns_404_if_the_history_does_not_exists(self) -> None:  # noqa: E501
        self.make_login()

        # make post request without an existing history
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_direct_treasure_history_delete_returns_404_if_the_history_belongs_to_another_user(self) -> None:  # noqa: E501
        # create the another_user
        another_user = self.create_user(
            username='jhondoe',
            email='jhon@email.com',
        )

        # create the history for another_user
        make_direct_treasure(user=another_user,
                             tax=1,
                             profits_value=1,
                             )

        # make login with user=user
        self.make_login()

        # make post request using the id that belongs to another_user
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_direct_treasure_history_delete_remove_the_history_from_data_base(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history
        product = make_direct_treasure(user=user,
                                       tax=1,
                                       profits_value=12,
                                       )

        # checks if the history exists
        history = DirectTreasureHistory.objects.filter(
            product=product,
        )
        # the history length must be 2 because
        # when the product is create by
        # make_direct_treause function,
        # automatically a history apply is created
        self.assertEqual(len(history), 2)
        self.assertEqual(history.first().tax_and_irpf, -1)
        self.assertEqual(history.first().value, 12)

        # make post request
        self.client.post(self.url)

        # checks again if the history exists
        history = DirectTreasureHistory.objects.filter(
            product=product,
        )
        # the history length must be 1
        self.assertEqual(len(history), 1)

    def test_direct_treasure_history_delete_returns_success_message_if_the_history_is_deleted(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history
        make_direct_treasure(user=user,
                             tax=1,
                             profits_value=12,
                             )

        # make post request
        response = self.client.post(self.url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn(
            'histórico deletado com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/tesouro-direto/1/historico/',
            302,
        )
