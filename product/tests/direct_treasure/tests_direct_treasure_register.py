from utils.mixins.auth import TestCaseWithLogin
from django.urls import reverse, resolve
from product.views import DirectTreasureRegisterView
from product.models import DirectTreasure
from parameterized import parameterized


class DirectTreasureRegisterTests(TestCaseWithLogin):
    url = reverse('product:direct_treasure_register')

    def test_direct_treasure_register_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/tesouro-direto/registrar/',
        )

    def test_direct_treasure_register_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            DirectTreasureRegisterView,
        )

    def test_direct_treasure_register_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/tesouro-direto/registrar/',
            302,
        )

    def test_direct_treasure_register_is_allowed_if_user_is_authenticated(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_direct_treasure_register_loads_correct_template(self) -> None:
        self.make_login()
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'product/pages/direct_treasure/register.html',
        )

    @parameterized.expand([
        ('nome'),
        ('categoria'),
        ('recebimento de juros'),
        ('rentabilidade'),
        ('vencimento'),
        ('valor'),
        ('descrição'),
    ])
    def test_direct_treasure_register_loads_correct_content(self, text: str) -> None:  # noqa:E 501
        # make login
        self.make_login()

        # make request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )

    @parameterized.expand([
        ('name', 'Campo obrigatório'),
        ('category', 'Campo obrigatório'),
        ('interest_receipt', 'Campo obrigatório'),
        ('profitability', 'Campo obrigatório'),
        ('maturity_date', 'Campo obrigatório'),
        ('value', 'Campo obrigatório'),
    ])
    def test_direct_treasure_register_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        self.make_login()

        # register data
        register_data = {
            field: '',
        }

        # make post request
        response = self.client.post(
            self.url,
            register_data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/tesouro-direto/registrar/',
            302,
        )

    def test_direct_treasure_register_returns_success_message_if_a_new_object_is_created(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # registar data
        register_data = {
            'user': user,
            'name': 'tesouro prefixado 2024',
            'category': 'selic',
            'interest_receipt': 'não há',
            'profitability': '10% a.a',
            'maturity_date': '2024-12-31',
            'value': 1000,
            'description': '',
        }

        # make post request
        response = self.client.post(
            self.url,
            register_data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Aplicação criada com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/tesouro-direto/',
            302,
        )

    def test_direct_treasure_register_creates_a_new_object(self) -> None:
        # make login
        _, user = self.make_login()

        # registar data
        register_data = {
            'user': user,
            'name': 'tesouro prefixado 2024',
            'category': 'selic',
            'interest_receipt': 'não há',
            'profitability': '10% a.a',
            'maturity_date': '2024-12-31',
            'value': 1000,
            'description': '',
        }

        # make post request
        self.client.post(
            self.url,
            register_data,
            follow=True,
        )

        # get queryset
        products = DirectTreasure.objects.filter(
            user=user
        )

        self.assertEqual(
            len(products),
            1
        )
        self.assertEqual(
            products.first().name,
            'tesouro prefixado 2024',
        )
