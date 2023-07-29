from django.urls import reverse, resolve
from django.http import HttpResponse
from django.contrib.auth.models import User
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.tests.base_tests import make_user_fii
from parameterized import parameterized


class FIIsProfitsHistoryEditTests(TestCaseWithLogin):
    url = reverse('product:fii_manage_income_receipt_edit', args=(1,))

    def create_profits_history(self, user: User) -> HttpResponse:
        # create the user fii
        make_user_fii(user, 1, 1, 'mxrf11', 'maxi renda')

        # add a profits
        response = self.client.post(
            reverse('product:fiis_manage_income_receipt'),
            {
                'user_product_id': 1,
                'value': 10,
                'date': '2023-07-02',
            },
            follow=True,
        )

        return response

    def test_fiis_profits_history_edit_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/fiis/gerenciar-proventos/historico/1/editar/',
        )

    def test_fiis_profits_history_edit_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FIIManageIncomeReceiptEditHistory,
        )

    def test_fiis_profits_history_edit_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/fiis/gerenciar-proventos/historico/1/editar/',
            302,
        )

    def test_fiis_profits_history_edit_returns_status_code_404_if_the_history_not_exists(self) -> None:  # noqa: E501
        self.make_login()

        # make get request without the product
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_fiis_profits_history_returns_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the profits history
        self.create_profits_history(user)

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_profits_history_edit_loads_correct_template(self) -> None:
        # make login
        _, user = self.make_login()

        # create the profits history
        self.create_profits_history(user)

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/pages/fiis/fiis_profits.html',
        )

    @parameterized.expand([
        ('editar'),
        ('salvar'),
        ('fii'),
        ('data'),
        ('valor'),
        ('MXRF11'),
        ('2023-07-02'),
        ('10.00'),
    ])
    def test_profits_history_edit_loads_correct_content(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the profits history
        self.create_profits_history(user)

        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )

    @parameterized.expand([
        ('user_product_id', 'Selecione um produto'),
        ('date', 'Campo obrigatório'),
        ('value', 'Campo obrigatório'),
    ])
    def test_profits_history_edit_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the profits history
        self.create_profits_history(user)

        # history data
        history_data = {
            field: '',
        }

        # make post request
        response = self.client.post(
            self.url,
            data=history_data,
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

    @parameterized.expand([
        ('user_product_id', 1, ''),
        ('date', '00-00-00', 'Informe uma data válida'),
        ('value', 10, ''),
    ])
    def test_profits_history_edit_returns_error_message_if_data_has_a_invalid_format(self, field: str, value: str | int, message: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the profits history
        self.create_profits_history(user)

        # history data
        history_data = {
            field: value,
        }

        # make post request
        response = self.client.post(
            self.url,
            data=history_data,
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

    def test_profits_history_edit_modify_the_history_if_the_form_is_ok(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the profits history
        self.create_profits_history(user)

        # create the new userfii
        new_user_fii = make_user_fii(user, 1, 1, 'pvbi11', 'desc')

        # create the profit for the new userfii
        self.client.post(
            reverse('product:fiis_manage_income_receipt'),
            {
                'user_product_id': new_user_fii.id,
                'value': 10,
                'date': '2023-07-02',
            }
            )

        # history data
        history_data = {
            'user_product_id': new_user_fii.id,
            'date': '2024-12-31',
            'value': 14,
        }

        # make post request
        self.client.post(
            self.url,
            data=history_data,
            follow=True,
            )

        # get the history
        history = new_user_fii.get_partial_history('profits')

        self.assertEqual(
            history[0].userproduct,
            new_user_fii,
        )
        self.assertEqual(
            str(history[0].date),
            '2024-12-31',
        )
        self.assertEqual(
            history[0].total_price,
            14,
        )

    def test_profits_history_edit_returns_success_message_if_the_history_has_been_modified(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the profits history
        self.create_profits_history(user)

        # create the new userfii
        new_user_fii = make_user_fii(user, 1, 1, 'pvbi11', 'desc')

        # create the profit for the new userfii
        self.client.post(
            reverse('product:fiis_manage_income_receipt'),
            {
                'user_product_id': new_user_fii.id,
                'value': 10,
                'date': '2023-07-02',
            }
            )

        # history data
        history_data = {
            'user_product_id': new_user_fii.id,
            'date': '2024-12-31',
            'value': 14,
        }

        # make post request
        response = self.client.post(
            self.url,
            data=history_data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            'salvo com sucesso',
            content,
            )
        self.assertRedirects(
            response,
            '/ativos/fiis/gerenciar-proventos/',
            302,
        )
