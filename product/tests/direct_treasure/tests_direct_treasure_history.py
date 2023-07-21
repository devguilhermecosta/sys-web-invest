from django.urls import resolve, reverse
from parameterized import parameterized

from product.tests.base_tests import make_direct_treasure
from product.views import DirectTreasureHistoryView
from utils.mixins.auth import TestCaseWithLogin


class DirectTreasureHistoryTests(TestCaseWithLogin):
    url = reverse('product:direct_treasure_history', args=(1,))

    def test_direct_treasure_history_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/tesouro-direto/1/historico/',
        )

    def test_direct_treasure_history_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            DirectTreasureHistoryView,
        )

    def test_direct_treasure_history_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without logged in
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/?next=/ativos/tesouro-direto/1/historico/',
            302,
        )

    def test_direct_treasure_history_returns_status_code_404_if_the_product_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make get request without the product
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_direct_treasure_history_returns_status_code_200_if_the_product_exists(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the product
        make_direct_treasure(user=user)

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_direct_treasure_history_loads_correct_template(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the product
        make_direct_treasure(user=user)

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/partials/_history_dt_&_fi.html'
        )

    @parameterized.expand([
        ('tesouro ipca 2024'),
        ('R$ 100,00'),
        ('R$ 50,00'),
        ('aplicação'),
        ('resgate'),
        ('valor atual: R$ 50,00'),
    ])
    def test_direct_treasure_history_loads_correct_content(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the product
        make_direct_treasure(user=user,
                             name='tesouro ipca 2024',
                             value=0,
                             )

        # apply a value
        self.client.post(
            reverse('product:direct_treasure_apply', args=(1,)),
            {'value': 100},
            follow=True
        )

        # redeem a value
        self.client.post(
            reverse('product:direct_treasure_redeem', args=(1,)),
            {'value': 50},
            follow=True
        )

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text, content
        )
        self.fail('criar os tests de histórico nos demais scripts. '
                  'criar botões para voltar a página dentro dos detalhes.'
                  )
