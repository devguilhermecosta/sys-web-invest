from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.models import FiiHistory
from product.tests.base_tests import make_user_fii, create_profits_history
from parameterized import parameterized


class FIIsProfitsHistoryEditTests(TestCaseWithLogin):
    url = reverse('product:fii_manage_income_receipt_edit', args=(1,))

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
        # create the profits history
        create_profits_history(self.client, self.make_login)

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_profits_history_edit_loads_correct_template(self) -> None:
        # create the profits history
        create_profits_history(self.client, self.make_login)

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
        # create the profits history
        create_profits_history(self.client, self.make_login)

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
        # create the profits history
        create_profits_history(self.client, self.make_login)

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
        # create the profits history
        create_profits_history(self.client, self.make_login)

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
        # create the profits history
        r = create_profits_history(self.client, self.make_login)

        # create the new userfii
        new_user_fii = make_user_fii(r['user'], 1, 1, 'pvbi11', 'desc')

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

    def test_profits_history_edit_returns_status_code_404_if_the_logged_in_user_is_different_from_the_history_owner_user(self) -> None:  # noqa: E501
        # create another user
        another_user = self.create_user(
            username='jhondoe',
            email='jhondoe@email.com',
        )

        # create the UserFII for another_user
        another_userfii = make_user_fii(
            another_user,
            1,
            1,
            'pvbi11',
            'teste',
        )

        # make login with the another_user
        self.make_login(create_user=False, username=another_user)

        # make post request for create the history for another_userfii
        r_post = self.client.post(
            reverse('product:fiis_manage_income_receipt'),
            {
                'user_product_id': another_userfii.id,
                'value': 50,
                'date': '2023-07-02',
            },
            follow=True,
        )

        # checks if the history has been created
        self.assertEqual(
            r_post.content.decode('utf-8'),
            '{"success": "success request"}',
        )

        # get the history id
        another_user_history = FiiHistory.objects.filter(
            userproduct=another_userfii,
            handler='profits',
        )

        # checks if the history_id of another_user is 1
        self.assertEqual(
            another_user_history.first().id,
            1
        )

        # make logout with the another_user
        self.client.logout()

        # create the profits history and make login with user=user
        u = create_profits_history(self.client,
                                   self.make_login,
                                   value=150,
                                   )

        # get the history id of user
        history_id_user = FiiHistory.objects.filter(
            userproduct=u['user_fii'],
            handler='profits'
        )

        # checks if the history_id_user is 2
        self.assertEqual(
            history_id_user.first().id,
            2
        )

        # now i am logged in with the user
        # i will try to edit the history of id 1 whose another_user owns
        response_get = self.client.get(self.url)
        response_post = self.client.post(
            self.url,
            data={
                'user_product_id': u['user_fii'].id,
                'date': '2024-12-31',
                'value': 14,
            },
            follow=True,
            )

        # the status code must be 404
        self.assertEqual(
            response_get.status_code,
            404
        )
        self.assertEqual(
            response_post.status_code,
            404
        )

    def test_profits_history_edit_returns_success_message_if_the_history_has_been_modified(self) -> None:  # noqa: E501
        # create the profits history
        r = create_profits_history(self.client, self.make_login)

        # create the new userfii
        new_user_fii = make_user_fii(r['user'], 1, 1, 'pvbi11', 'desc')

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
