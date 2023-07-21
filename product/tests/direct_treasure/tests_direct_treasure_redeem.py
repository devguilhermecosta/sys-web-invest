from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product.views import DirectTreasureRedeemView
from product.tests.base_tests import make_direct_treasure
from product.models import DirectTreasure


class DirectTreasureRedeemTests(TestCaseWithLogin):
    url = reverse('product:direct_treasure_redeem', args=(1,))

    def test_direct_treasure_redeem_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/tesouro-direto/1/resgatar/',
        )

    def test_direct_treasure_redeem_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            DirectTreasureRedeemView,
        )

    def test_direct_treasure_redeem_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make post request without logged in
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/tesouro-direto/1/resgatar/',
            302,
        )

    def test_direct_treasure_returns_status_code_404_if_the_product_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make post request without the product
        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_direct_treasure_returns_status_code_404_if_get_request(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the product
        make_direct_treasure(user=user)

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_direct_treasure_returns_error_message_if_the_value_field_is_empty(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the product
        make_direct_treasure(user=user)

        # make post request without the value
        response = self.client.post(
            self.url,
            {'value': ''},
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Campo obrigatório',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/tesouro-direto/1/detalhes/',
            302,
        )

    def test_direct_treasure_returns_error_message_if_the_value_field_is_bigger_than_the_product_value(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the product with value equal 100
        make_direct_treasure(user=user, value=100)

        # checks if the product value is 100
        obj = DirectTreasure.objects.get(pk=1)
        self.assertEqual(obj.value, 100)

        # try to redeem a value bigger than 100
        response = self.client.post(
            self.url,
            {'value': 101},
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Saldo insuficiente para resgate',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/tesouro-direto/1/detalhes/',
            302,
        )

    def test_direct_treasure_modify_the_product_value_if_all_is_ok(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the product with value equal 100
        make_direct_treasure(user=user, value=100)

        # checks if the product value is 100
        obj = DirectTreasure.objects.get(pk=1)
        self.assertEqual(obj.value, 100)

        # try to redeem a value equal to 100
        response = self.client.post(
            self.url,
            {'value': 100},
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Resgate realizado com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/tesouro-direto/1/detalhes/',
            302,
        )

        # checks if the value of the product has decreased
        product = DirectTreasure.objects.get(pk=1)
        self.assertEqual(
            product.value,
            0,
        )
