from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.tests.base_tests import make_direct_treasure
from product.models import DirectTreasureHistory
from parameterized import parameterized


class DirectTreasureProfitsReceiptTests(TestCaseWithLogin):
    url = reverse(
        'product:direct_treasure_profits_receipt',
        args=(1,),
        )

    def test_direct_treasure_profits_receipt_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/tesouro-direto/1/receber-juros/',
        )

    def test_direct_treasure_profits_receipt_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.DirectTreasureProfitsReceiptView,
        )

    def test_direct_treasure_profits_receipt_returns_status_code_302_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/tesouro-direto/1/receber-juros/',
            302,
        )

    def test_direct_treasure_profits_receipt_returns_status_code_404_if_the_product_not_exists(self) -> None:  # noqa: E501
        self.make_login()

        # make get request without an existing product
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_direct_treasure_profits_receipt_returns_status_code_404_if_the_product_belongs_to_another_user(self) -> None:  # noqa: E501
        # create the another_user
        another_user = self.create_user(username='jhondoe',
                                        email='jhon@email.com',
                                        )

        # create the product for another_user
        make_direct_treasure(user=another_user)

        # make login with user=user
        self.make_login()

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_direct_treasure_profits_receipt_returns_status_code_200_if_the_product_exists(self) -> None:  # noqa: E501
        # make login with user=user
        _, user = self.make_login()

        # create the product
        make_direct_treasure(user=user)

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_direct_treasure_profits_receipt_loads_correct_template(self) -> None:  # noqa: E501
        # make login with user=user
        _, user = self.make_login()

        # create the product
        make_direct_treasure(user=user)

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/partials/_dt_and_fi_default_form.html',
            )

    @parameterized.expand([
        'TESOURO SELIC 2035',
        'data',
        'valor',
        'receber',
    ])
    def test_direct_treasure_profits_receipt_loads_correct_content(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the direct treasure product
        make_direct_treasure(user=user,
                             name='tesouro selic 2035',
                             )

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )

    @parameterized.expand([
        ('date', 'Campo obrigatório'),
        ('value', 'Campo obrigatório'),
    ])
    def test_direct_treasure_profits_receipt_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the direct treasure product
        make_direct_treasure(user=user,
                             name='tesouro selic 2035',
                             )

        # data
        data = {
            field: '',
        }

        # make post request
        response = self.client.post(
            self.url,
            data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/tesouro-direto/1/receber-juros/',
            302,
        )

    def test_direct_treasure_profits_receipt_returns_create_a_new_history(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the direct treasure product
        make_direct_treasure(user=user,
                             name='tesouro selic 2035',
                             )

        # data
        data = {
            'date': '2023-07-02',
            'value': 100,
            'tax_and_irpf': 10,
        }

        # make post request
        self.client.post(
            self.url,
            data,
            follow=True,
            )

        # get the history
        history = DirectTreasureHistory.objects.filter(
            state='profits',
        )

        self.assertEqual(
            str(history.first().date),
            '2023-07-02',
        )
        self.assertEqual(
            history.first().state,
            'profits',
        )
        self.assertEqual(
            history.first().get_final_value(),
            90.00,
        )
        self.assertEqual(
            history.first().tax_and_irpf,
            -10.00,
        )

    def test_direct_treasure_profits_receipt_returns_success_message(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the direct treasure product
        make_direct_treasure(user=user,
                             name='tesouro selic 2035',
                             )

        # data
        data = {
            'date': '2023-07-02',
            'value': 100,
            'tax_and_irpf': 10,
        }

        # make post request
        response = self.client.post(
            self.url,
            data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Recebimento de juros salvo com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/tesouro-direto/1/detalhes/',
            302,
        )
