from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.models import DirectTreasureHistory
from product.tests.base_tests import make_direct_treasure
from parameterized import parameterized


class DirectTreasureHistoryEditTests(TestCaseWithLogin):
    url = reverse(
        'product:direct_treasure_history_edit',
        kwargs={
            'history_id': 1,
            'product_id': 1,
        },
        )

    def test_direct_treasure_history_edit_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/tesouro-direto/1/historico/1/editar/',
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
            '/?next=/ativos/tesouro-direto/1/historico/1/editar/',
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
        _, user = self.make_login()

        # create a history
        make_direct_treasure(user=user, value=10)

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/partials/_dt_and_fi_default_form.html',
        )

    @parameterized.expand([
        'movimentação',
        'data',
        'taxas e impostos',
        'valor',
        'salvar',
    ])
    def test_direct_treasure_history_edit_loads_correct_content(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history
        make_direct_treasure(user=user, value=10)

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )

    @parameterized.expand([
        'aplicação',
        'resgate',
        'recebimento de juros',
    ])
    def test_direct_treasure_history_edit_loads_all_options_if_interest_receipt_property_is_different_from_NÃO_HÁ(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history with interest_receipt=semestral
        make_direct_treasure(user=user, value=10, interest_receipt='semestral')

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )

    def test_direct_treasure_history_edit_does_not_loads_the_PROFITS_option_from_state_property_if_the_interest_receipt_is_NÃO_HÁ(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history with interest_receipt=não há
        make_direct_treasure(user=user, value=10, interest_receipt='não há')

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn('aplicação', content)
        self.assertIn('resgate', content)
        self.assertNotIn('recebimento de juros', content)

    @parameterized.expand([
        ('state', 'Campo obrigatório'),
        ('date', 'Campo obrigatório'),
        ('value', 'Campo obrigatório'),
    ])
    def test_direct_treasure_history_edit_loads_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history
        make_direct_treasure(user=user, value=10)

        # data
        data = {
            field: ''
        }

        # make post request
        response = self.client.post(
            self.url,
            data,
            follow=True,
            )
        content = response.content.decode('utf-8')
        ...

        self.assertIn(
            message,
            content,
        )
        self.assertRedirects(
            response,
            self.url,
            302,
        )

    def test_direct_treasure_history_edit_changes_the_history_if_all_data_is_ok(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history
        make_direct_treasure(user=user,
                             tax=1,
                             profits_value=10,
                             value=10,
                             )

        # data
        data = {
            'state': 'redeem',
            'date': '2023-07-02',
            'tax_and_irpf': 12,
            'value': 150,
        }

        # make post request
        self.client.post(
            self.url,
            data,
            follow=True,
            )

        # get the history
        history = DirectTreasureHistory.objects.get(pk=1)

        # checks if the data has been changed
        self.assertEqual(history.tax_and_irpf, -12)
        self.assertEqual(history.value, -150)
        self.assertEqual(history.state, 'redeem')

    def test_direct_treasure_history_edit_returns_success_message_if_the_history_has_been_changed(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history
        make_direct_treasure(user=user,
                             tax=1,
                             profits_value=10,
                             value=10,
                             )

        # data
        data = {
            'state': 'redeem',
            'date': '2023-07-02',
            'tax_and_irpf': 12,
            'value': 150,
        }

        # make post request
        response = self.client.post(
            self.url,
            data,
            follow=True,
            )

        self.assertIn(
            'histórico salvo com sucesso',
            response.content.decode('utf-8'),
        )
        self.assertRedirects(
            response,
            reverse('product:direct_treasure_history', args=(1,)),
            302,
        )
