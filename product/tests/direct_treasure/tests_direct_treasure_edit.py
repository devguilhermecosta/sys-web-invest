from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product.views import DirectTreasureEditView
from product.tests.base_tests import make_direct_treasure
from product.models import DirectTreasure
from parameterized import parameterized


class DirectTreasureEditTests(TestCaseWithLogin):
    url = reverse('product:direct_treasure_edit', args=(1,))

    def test_direct_treasure_edit_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/tesouro-direto/1/editar/',
        )

    def test_direct_treasure_edit_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            DirectTreasureEditView,
        )

    def test_direct_treasure_edit_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/tesouro-direto/1/editar/',
            302,
        )

    def test_direct_treasure_edit_is_allowed_if_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a new product
        make_direct_treasure(user=user)

        # get request
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code, 200,
        )

    def test_direct_treasure_edit_returns_status_code_404_if_product_not_exists(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # post request without create the product
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code, 404,
        )

    def test_direct_treasure_edit_loads_correct_template(self) -> None:
        # make login
        _, user = self.make_login()

        # create a new product
        make_direct_treasure(user=user)

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/partials/_dt_and_fi_default_form.html',
        )

    @parameterized.expand([
        ('tesouro ipca+ 2024'),
        ('ipca'),
        ('não há'),
        ('ipca + 4,9% a.a'),
        ('2024-12-31'),
        ('tesouro ipca sem pagamento de juros'),
    ])
    def test_direct_treasure_edit_loads_correct_content(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a new product
        make_direct_treasure(user=user)

        # make get request
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
        ('maturity_date', 'Campo obrigatório'),
        ('profitability', 'Campo obrigatório'),
        ('value', 'Campo obrigatório'),
    ])
    def test_direct_treasure_edit_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a new product
        make_direct_treasure(user=user)

        # form data
        form_data = {
            field: '',
        }

        # make post request
        response = self.client.post(
            self.url,
            form_data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/tesouro-direto/1/editar/',
            302,
        )

    def test_direct_treasure_edit_returns_success_message_if_the_product_is_saved(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a new product
        make_direct_treasure(user=user)

        # form data
        form_data = {
            'name': 'novo nome',
            'category': 'ipca',
            'interest_receipt': 'semestral',
            'maturity_date': '2030-12-31',
            'profitability': '8.0% a.a',
        }

        # make post request
        response = self.client.post(
            self.url,
            form_data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Salvo com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/tesouro-direto/1/detalhes/',
            302,
        )

    def test_direct_treasure_edit_modified_the_product_edited(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a new product
        make_direct_treasure(user=user)

        # form data
        form_data = {
            'name': 'novo nome',
            'category': 'ipca',
            'interest_receipt': 'semestral',
            'maturity_date': '2030-12-31',
            'profitability': '8.0% a.a',
        }

        # make post request
        self.client.post(
            self.url,
            form_data,
            follow=True,
            )

        # get the product
        product = DirectTreasure.objects.get(
            user=user,
            pk=1,
        )

        # checks if the data has been modified
        self.assertEqual(
            product.name,
            form_data['name'],
        )
        self.assertEqual(
            product.category,
            form_data['category'],
        )
