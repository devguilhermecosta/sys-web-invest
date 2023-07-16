from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product.views import DirectTreasureApplyView
from product.tests.base_tests import make_direct_treasure
from product.models import DirectTreasure, DirectTreasureHistory


class DirectTreasureApplyTests(TestCaseWithLogin):
    url = reverse('product:direct_treasure_apply', args=(1,))

    def test_direct_treasure_apply_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/tesouro-direto/1/aplicar/',
        )

    def test_direct_treasure_apply_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            DirectTreasureApplyView,
        )

    def test_direct_treasure_apply_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/tesouro-direto/1/aplicar/',
            302,
        )

    def test_direct_treasure_apply_returns_status_code_404_if_get_request(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code, 404
        )

    def test_direct_treasure_apply_returns_status_code_404_if_the_product_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # post request without product
        response = self.client.post(
            self.url,
            {'value': 10},
            follow=True,
            )

        self.assertEqual(
            response.status_code, 404
        )

    def test_direct_treasure_apply_returns_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: E501
        ''' and the user has the product '''
        # make login
        _, user = self.make_login()

        # create the product
        make_direct_treasure(user=user)

        # make post request
        response = self.client.post(
            self.url,
            {'value': 10},
            follow=True,
            )

        self.assertEqual(response.status_code, 200)

    def test_direct_treasure_apply_returns_error_message_if_value_field_is_empty(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the product
        make_direct_treasure(user=user)

        # post request without the value
        response = self.client.post(
            self.url,
            {'value': ''},
            follow=True,
        )

        self.assertIn(
            'Campo obrigatório',
            response.content.decode('utf-8'),
        )
        self.assertRedirects(
            response,
            '/ativos/tesouro-direto/1/detalhes/',
            302,
        )

    def test_direct_treasure_apply_increases_the_product_value(self) -> None:
        # make login
        _, user = self.make_login()

        # create the product with value equal 90
        make_direct_treasure(user=user, value=90)

        # post request without the value equal 10
        self.client.post(
            self.url,
            {'value': 10},
            follow=True,
        )

        # get the product
        product = DirectTreasure.objects.get(
            user=user,
            id=1,
        )

        # checks if the product value is 100
        self.assertEqual(product.value, 100)

    def test_direct_treasure_apply_creates_a_new_history(self) -> None:
        # make login
        _, user = self.make_login()

        # create the product with value equal 90
        make_direct_treasure(user=user, value=90)

        # post request with the value equal 10
        self.client.post(
            self.url,
            {'value': 10},
            follow=True,
        )

        # get the product
        product = DirectTreasure.objects.get(
            user=user,
            id=1,
        )

        # get the history
        history = DirectTreasureHistory.objects.filter(
            product=product
        )

        # checks if the history length is one
        self.assertEqual(len(history), 1)

        # checks the product history
        self.assertEqual(
            history[0].product,
            product,
        )
