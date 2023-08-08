from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.tests.base_tests import make_fixed_income_product
from product.models import FixedIncomeHistory
from parameterized import parameterized


class FixedIncomeHistoryEditTests(TestCaseWithLogin):
    url = reverse(
        'product:fixed_income_history_edit',
        kwargs={'product_id': 1, 'history_id': 1},
        )

    def test_fixed_income_history_edit_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/renda-fixa/1/historico/1/editar/',
        )

    def test_fixed_income_history_edit_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertEqual(
            response.func.view_class,
            views.FixedIncomeHistoryEditView,
        )

    def test_fixed_income_history_edit_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/renda-fixa/1/historico/1/editar/',
            302,
        )

    def test_fixed_income_history_edit_returns_status_code_404_if_the_history_does_not_exists(self) -> None:  # noqa: E501
        self.make_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_fixed_income_history_edit_returns_status_code_404_if_the_history_belongs_to_another_user(self) -> None:  # noqa: E501
        # create a user
        another_user = self.create_user(username='jhondoe',
                                        email='jhon@email.com',
                                        )

        # create the history with an apply history
        make_fixed_income_product(user=another_user, value=10)

        # make login with user=user
        self.make_login()

        # tries to edit history belonging to another user
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_fixed_income_history_edit_returns_status_code_200_if_the_history_exists_and_belongs_to_logged_in_user(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history
        make_fixed_income_product(user=user, value=10)

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_fixed_income_history_edit_loads_correct_template(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history
        make_fixed_income_product(user=user, value=10)

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/partials/_dt_and_fi_history_edit.html',
        )

    @parameterized.expand([
        'apply',
        'redeem',
        'profits',
        '2023-07-02',
        '10.00',
        'editar histórico',
        'salvar',
    ])
    def test_fixed_income_history_edit_loads_correct_content(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history
        make_fixed_income_product(user=user,
                                  value=10,
                                  interest_receipt='semestral',
                                  )

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )

    def test_fixed_income_history_edit_does_not_loads_the_PROFITS_state_select_if_the_interest_receipt_property_is_NÃO_HÁ(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history
        make_fixed_income_product(user=user,
                                  value=10,
                                  interest_receipt='não há',
                                  )

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertNotIn(
            'profits',
            content,
        )
        self.assertIn(
            'apply',
            content,
        )
        self.assertIn(
            'redeem',
            content,
        )

    @parameterized.expand([
        ('state', 'Campo obrigatório'),
        ('date', 'Campo obrigatório'),
        ('value', 'Campo obrigatório'),
    ])
    def test_fixed_income_history_edit_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history
        make_fixed_income_product(user=user, value=10)

        # data
        data = {
            field: '',
        }

        # make post request
        response = self.client.post(
            self.url,
            data=data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content,
        )
        self.assertRedirects(
            response,
            self.url,
            302,
        )

    def test_fixed_income_history_edit_save_the_history_if_the_form_is_ok(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history
        make_fixed_income_product(user=user, value=10)

        # data
        first_data = {
            'state': 'redeem',
            'date': '2025-01-14',
            'tax_and_irpf': 10,
            'value': 100,
        }

        # make post request
        first_request = self.client.post(
            self.url,
            data=first_data,
            follow=True,
            )

        # get the history
        history = FixedIncomeHistory.objects.get(pk=1)

        # checks if the history information is correct.
        # value is negative when the state is 'redeem'.
        # tax_and_irpf is always negative.
        self.assertEqual(history.state, 'redeem')
        self.assertEqual(str(history.date), '2025-01-14')
        self.assertEqual(history.value, -100.00)
        self.assertEqual(history.tax_and_irpf, -10.00)
        self.assertRedirects(
            first_request,
            reverse('product:fixed_income_history', args=(1,)),
            302,
        )

        # data
        second_data = {
            'state': 'profits',
            'date': '2030-09-10',
            'tax_and_irpf': 15,
            'value': 100,
        }

        # makes a new post request to check if the data changes
        second_request = self.client.post(
            self.url,
            data=second_data,
            follow=True,
            )

        # get the history
        history = FixedIncomeHistory.objects.get(pk=1)

        # checks if the history information is correct.
        # now the value must be positive.
        # tax_and_irpf is always negative.
        self.assertEqual(history.state, 'profits')
        self.assertEqual(str(history.date), '2030-09-10')
        self.assertEqual(history.value, 100.00)
        self.assertEqual(history.tax_and_irpf, -15.00)
        self.assertRedirects(
            second_request,
            reverse('product:fixed_income_history', args=(1,)),
            302,
        )

    def test_fixed_income_history_edit_render_the_success_message_if_the_history_is_saved(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a history
        make_fixed_income_product(user=user, value=10)

        # data
        data = {
            'state': 'redeem',
            'date': '2025-01-14',
            'tax_and_irpf': 10,
            'value': 100,
        }

        # make post request
        request = self.client.post(
            self.url,
            data=data,
            follow=True,
            )
        content = request.content.decode('utf-8')

        self.assertIn(
            'histórico salvo com sucesso',
            content,
        )
