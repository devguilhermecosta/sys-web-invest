from utils.mixins.auth import TestCaseWithLogin
from django.urls import reverse, resolve
from product.views import DirectTreasureDetailsView
from product.tests.base_tests import make_direct_treasure
from parameterized import parameterized


class DirectTreasureDetailsTests(TestCaseWithLogin):
    url = reverse('product:direct_treasure_details', args=(1,))

    def test_direct_treasure_details_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/tesouro-direto/1/detalhes/',
        )

    def test_direct_treasure_details_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            DirectTreasureDetailsView,
        )

    def test_direct_treasure_details_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/tesouro-direto/1/detalhes/',
            302,
        )

    def test_direct_treasure_details_returns_status_code_404_if_not_get_request(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make post request
        response = self.client.post(self.url)
        self.assertEqual(
            response.status_code, 404
        )

    def test_direct_treasure_details_returns_status_code_404_if_the_product_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make get request without the product
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code, 404,
        )

    def test_direct_treasure_details_is_allowed_if_user_is_authenticated(self) -> None:  # noqa: E501
        """ and if the product exists """
        # make login
        _, user = self.make_login()

        # create a new product
        make_direct_treasure(user=user)

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code, 200
        )

    def test_direct_treasure_details_loads_correct_template(self) -> None:
        # make login
        _, user = self.make_login()

        # create the new product
        make_direct_treasure(user=user)

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/partials/_dt_and_fi_details.html',
        )

    @parameterized.expand([
        ('editar'),
        ('histórico'),
        ('TESOURO IPCA+ 2024'),
        ('IPCA'),
        ('Não Há'),
        ('ipca + 4,9% a.a.'),
        ('31/12/2024'),
        ('R$ 1500,00'),
        ('Tesouro ipca sem pagamento de juros'),
    ])
    def test_direct_treasure_details_loads_correct_content(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the new product
        make_direct_treasure(user=user, value=1500)

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )
