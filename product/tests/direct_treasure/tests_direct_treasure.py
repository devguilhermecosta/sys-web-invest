from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product.views import DirectTreasureView
from product.tests.base_tests import make_direct_treasure


class DirectTreasureTests(TestCaseWithLogin):
    url = reverse('product:direct_treasure')

    def test_direct_treasure_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/tesouro-direto/')

    def test_direct_treasure_uses_corret_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(response.func.view_class, DirectTreasureView)

    def test_direct_treasure_is_not_allowed_if_user_is_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/tesouro-direto/',
            302,
        )

    def test_direct_treasure_is_allowed_if_user_is_authenticated(self) -> None:
        self.make_login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_direct_treasure_returns_status_code_405_if_post_request(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_direct_treasure_loads_correct_template(self) -> None:
        self.make_login()
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'product/pages/direct_treasure/direct_treasure.html'
        )

    def test_direct_treasure_loads_correct_content_if_the_user_dont_have_products(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            'nenhum produto cadastrado',
            content,
        )

    def test_direct_treasure_loads_correct_content_if_the_user_has_products(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a new product
        make_direct_treasure(user=user)

        # get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            'tesouro ipca+ 2024',
            content,
        )

    def test_direct_treasure_loads_just_authenticated_user_products(self) -> None:  # noqa: E501
        # create the any user
        any_user = self.create_user(True,
                                    username='anyuser',
                                    email='anyuser@email.com',
                                    )

        # create two products for anyuser
        make_direct_treasure(user=any_user)
        make_direct_treasure(user=any_user)

        # make login
        _, user = self.make_login()

        # create a new product for correct user
        make_direct_treasure(user=user)

        # get request
        response = self.client.get(self.url)

        # get product queryset
        products = response.context['products']

        # the products length should be 1
        self.assertEqual(len(products), 1)
