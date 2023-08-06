from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.tests.base_tests import make_direct_treasure


class DirectTreasureHistoryEditTests(TestCaseWithLogin):
    url = reverse('product:direct_treasure_history_edit', args=(1,))

    def test_direct_treasure_history_edit_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/tesouro-direto/historico/1/editar/',
        )

    def test_direct_treasure_history_edit_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.DirectTreasureHistoryEditView,
        )

    def test_direct_treasure_history_edit_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/tesouro-direto/historico/1/editar/',
            302,
        )

    def test_direct_treasure_history_edit_is_allowed_if_the_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create an direct treasure product
        make_direct_treasure(user=user, value=10)

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_direct_treasure_history_edit_returns_404_if_the_history_not_exists(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # make get request without an existing product
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_direct_treasure_history_edit_returns_404_if_the_history_belongs_to_another_user(self) -> None:  # noqa: E501
        # create a user
        another_user = self.create_user(username='jhondoe',
                                        email='jhon@email.com',
                                        )

        # make a history for another_user
        make_direct_treasure(user=another_user, value=10)

        # make login with user=user
        self.make_login()

        # tries get the history of the another_user
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_direct_treasure_history_edit_loads_correct_template(self) -> None:
        ...
