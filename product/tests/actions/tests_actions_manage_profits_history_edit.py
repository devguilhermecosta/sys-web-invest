from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.models import ActionHistory
from product.tests.base_tests import (
    make_user_action,
    create_actions_history,
)
from parameterized import parameterized


class ActionManageProfitsHistoryDeleteTests(TestCaseWithLogin):
    url = reverse('product:action_manage_profits_edit', args=(1,))

    def test_actions_manage_profits_edit_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/acoes/gerenciar-proventos/historico/1/editar/',
        )

    def test_actions_manage_profits_edit_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ActionsManageProfitsHistoryEditView,
        )

    def test_actions_manage_profits_edit_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/?next=/ativos/acoes/gerenciar-proventos/historico/1/editar/',
            302,
        )

    def test_actions_manage_profits_edit_returns_404_if_the_product_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make get request without an existing product
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_actions_manage_profits_edit_returns_404_if_the_product_belongs_to_another_user(self) -> None:  # noqa: E501
        # create another user
        another_user = self.create_user(
            username='jhondoe',
            email='jhondoe@email.com',
        )

        # create the UserAction for another_user
        another_useraction = make_user_action(
            another_user,
            'sanp4',
            'sanepar',
        )

        # make login with the another_user
        self.make_login(create_user=False, username=another_user)

        # make post request for create the history for another_useraction
        r_post = self.client.post(
            reverse('product:actions_manage_profits'),
            {
                'userproduct': another_useraction.id,
                'handler': 'dividends',
                'date': '2023-07-02',
                'tax_and_irpf': 1,
                'unit_price': 10,
            },
            follow=True,
        )

        # checks if the history has been created
        self.assertIn(
            '{"data": "success request"}',
            r_post.content.decode('utf-8'),
        )

        # get the history id
        another_user_history = ActionHistory.objects.filter(
            userproduct=another_useraction,
        )

        # checks if the history_id of another_user is 1
        self.assertEqual(another_user_history.first().id, 1)

        # make logout with the another_user
        self.client.logout()

        # make login with user
        self.make_login()

        # now i am logged in with the user
        # i will try to edit the history of id 1 whose another_user owns
        response = self.client.get(self.url)

        # the status code must be 404
        self.assertEqual(response.status_code, 404)

    def test_actions_manage_profits_edit_returns_status_code_200_if_the_history_exists(self) -> None:  # noqa: E501
        # create a history and make login
        create_actions_history(self.client, self.make_login)

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_actions_manage_profits_edit_loads_correct_template(self) -> None:  # noqa: E501
        # create a history and make login
        create_actions_history(self.client, self.make_login)

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/pages/actions/actions_profits.html'
        )

    @parameterized.expand([
        ('editar rendimento'),
        ('salvar'),
        ('BBAS3'),
        ('dividendos'),
        ('2023-08-01'),
        ('10.00'),
        ('150.00'),
    ])
    def test_actions_manage_profits_edit_loads_correct_content(self, text: str) -> None:  # noqa: E501
        # create a history and make login
        create_actions_history(self.client,
                               self.make_login,
                               code='bbas3',
                               date='2023-08-01',
                               handler='dividends',
                               tax_and_irpf=10,
                               gross_value=150,
                               )

        # make get request
        response = self.client.get(self.url)

        self.assertIn(
            text,
            response.content.decode('utf-8'),
        )

    def test_actions_manage_profits_edit_post_request_returns_404_if_the_product_belongs_to_another_user(self) -> None:  # noqa: E501
        # create another user
        another_user = self.create_user(
            username='jhondoe',
            email='jhondoe@email.com',
        )

        # create the UserAction for another_user
        another_useraction = make_user_action(
            another_user,
            'sanp4',
            'sanepar',
        )

        # make login with the another_user
        self.make_login(create_user=False, username=another_user)

        # make post request for create the history for another_useraction
        r_post = self.client.post(
            reverse('product:actions_manage_profits'),
            {
                'userproduct': another_useraction.id,
                'handler': 'dividends',
                'date': '2023-07-02',
                'tax_and_irpf': 1,
                'unit_price': 10,
            },
            follow=True,
        )

        # checks if the history has been created
        self.assertIn(
            '{"data": "success request"}',
            r_post.content.decode('utf-8'),
        )

        # get the history id
        another_user_history = ActionHistory.objects.filter(
            userproduct=another_useraction,
        )

        # checks if the history_id of another_user is 1
        self.assertEqual(another_user_history.first().id, 1)

        # make logout with the another_user
        self.client.logout()

        # make login with user
        self.make_login()

        # now i am logged in with the user
        # i will try to edit the history of id 1 whose another_user owns
        response = self.client.post(self.url)

        # the status code must be 404
        self.assertEqual(response.status_code, 404)

    @parameterized.expand([
        ('user_product_id', 'selecione uma ação'),
        ('profits_type', 'campo obrigatório'),
        ('date', 'campo obrigatório'),
        ('unit_price', 'campo obrigatório'),
    ])
    def test_actions_manage_profits_edit_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # create the useraction and make login
        create_actions_history(self.client,
                               self.make_login,
                               )

        # history data
        history_data = {
            field: '',
        }

        # make post request
        response = self.client.post(
            self.url,
            history_data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content,
        )

    @parameterized.expand([
        ('userproduct', '---', 'selecione uma ação'),
        ('handler', '---', 'selecione um tipo de rendimento'),
        ('date', '00-00-0000', 'Informe uma data válida'),
        ('unit_price', 'abc', 'Informe um número'),
    ])
    def test_actions_manage_profits_edit_returns_error_messages_if_any_field_has_invalid_data(self, field: str, value: str, message: str) -> None:  # noqa: E501
        # create the useraction and make login
        create_actions_history(self.client,
                               self.make_login,
                               )

        # history data
        history_data = {
            field: value,
        }

        # make post request
        response = self.client.post(
            self.url,
            history_data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content,
        )

    def test_actions_manage_profits_edit_returns_success_message_if_the_form_data_is_ok(self) -> None:  # noqa: E501
        # create the useraction and make login
        u = create_actions_history(self.client,
                                   self.make_login,
                                   )

        # create one more useraction
        new_useraction = make_user_action(u['user'],
                                          'cash3',
                                          'meliuz',
                                          )

        # history data
        history_data = {
            'userproduct': new_useraction.id,
            'handler': 'renting',
            'date': '2023-08-01',
            'unit_price': 1000,
        }

        # make post request
        response = self.client.post(
            self.url,
            history_data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'rendimento salvo com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/acoes/gerenciar-proventos/',
            302,
        )

    def test_actions_manage_profits_edit_modify_the_edited_history(self) -> None:  # noqa: E501
        # create the useraction and make login
        u = create_actions_history(self.client,
                                   self.make_login,
                                   )

        # create one more useraction
        new_useraction = make_user_action(u['user'],
                                          'cash3',
                                          'meliuz',
                                          )

        # history data
        history_data = {
            'userproduct': new_useraction.id,
            'handler': 'renting',
            'date': '2023-08-01',
            'unit_price': 1000,
        }

        # make post request
        self.client.post(
            self.url,
            history_data,
            follow=True,
        )

        # get the edited action history
        history_queryset = ActionHistory.objects.all()
        history = history_queryset.first()

        self.assertEqual(
            history.userproduct,
            new_useraction,
        )
        self.assertEqual(
            history.handler,
            'renting',
        )
        self.assertEqual(
            str(history.date),
            '2023-08-01',
        )
        self.assertEqual(
            history.get_final_value(),
            1000,
        )
