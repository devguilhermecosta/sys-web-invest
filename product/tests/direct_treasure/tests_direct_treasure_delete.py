from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.models import DirectTreasure
from product.tests.base_tests import make_direct_treasure


class DirectTreasureDeleteTests(TestCaseWithLogin):
    url = reverse('product:direct_treasure_delete', args=(1,))

    def test_direct_treasure_delete_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/tesouro-direto/1/deletar/',
        )

    def test_direct_treasure_delete_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.DirectTreasureDeleteView,
        )

    def test_direct_treasure_delete_returns_status_code_404_if_get_request(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_direct_treasure_delete_returns_status_code_302_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make post request without is logged in
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/tesouro-direto/1/deletar/',
            302,
        )

    def test_direct_treasure_delete_returns_status_code_404_if_the_product_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make post request without an existing product
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_direct_treasure_delete_returns_status_code_404_if_the_product_belongs_to_another_user(self) -> None:  # noqa: E501
        # create the another_user
        another_user = self.create_user(username='jhondoe',
                                        email='jhon@email.com',
                                        )

        # create the direct treasure product
        make_direct_treasure(user=another_user)

        # checks if the product exists
        product = DirectTreasure.objects.filter(
            user=another_user
        )
        self.assertEqual(len(product), 1)

        # make login with user=user
        self.make_login()

        # tries delete the product that belongs to another_user
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_direct_treasure_delete_remove_the_product_from_data_base(self) -> None:  # noqa: E501
        # make login with user=user
        _, user = self.make_login()

        # create the product
        make_direct_treasure(user=user)

        # checks if the product exists
        product = DirectTreasure.objects.filter(
            user=user
        )
        self.assertEqual(len(product), 1)

        # make post request
        self.client.post(self.url)

        # checks again if the product exists
        product = DirectTreasure.objects.filter(
            user=user
        )
        self.assertEqual(len(product), 0)

    def test_direct_treasure_delete_returns_success_message_if_the_product_is_removed_from_data_base(self) -> None:  # noqa: E501
        # make login with user=user
        _, user = self.make_login()

        # create the product
        make_direct_treasure(user=user)

        # make post request
        response = self.client.post(self.url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn(
            'ativo deletado com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/tesouro-direto/',
            302,
        )
