from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.models import UserAction, ActionHistory
from product.tests.base_tests import make_user_action
from parameterized import parameterized


class ActionsManageIncomeTests(TestCaseWithLogin):
    url = reverse('product:actions_manage_profits')

    def test_actions_manage_profits_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/acoes/gerenciar-proventos/',
        )

    def test_actions_manage_profits_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ActionsManageProfitsView,
        )

    def test_actions_manage_profits_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without being logged in
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/acoes/gerenciar-proventos/',
            302,
        )

    def test_actions_manage_profits_returns_status_code_200_if_the_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_actions_manage_profits_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/pages/actions/actions_profits.html',
        )

    @parameterized.expand([
        ('ação'),
        ('tipo de rendimento'),
        ('dividendos'),
        ('jscp'),
        ('remuneração'),
        ('aluguel'),
        ('data'),
        ('taxas e irpf'),
        ('valor recebido'),
        ('lançar rendimento'),
        ('salvar'),
    ])
    def test_actions_manage_profits_loads_correct_content(self, text: str) -> None:  # noqa: E501
        self.make_login()

        response = self.client.get(self.url)

        self.assertIn(
            text,
            response.content.decode('utf-8')
        )

    def test_actions_manage_profits_user_product_id_field_loads_only_the_actions_of_the_logged_in_user(self) -> None:  # noqa: E501
        # create a new user
        another_user = self.create_user(username='anotheruser',
                                        email='anotheruser@email.com',
                                        )

        # create the user_action for another_user
        make_user_action(another_user,
                         1,
                         1,
                         'sanp4',
                         'sanepar',
                         )

        # checks if the sanp4 has been created
        user_action_another_user = UserAction.objects.filter(
            user=another_user,
        )
        self.assertEqual(len(user_action_another_user), 1)

        # make login with user=user
        _, user = self.make_login()

        # create the user_action for user
        make_user_action(user,
                         1,
                         1,
                         'bbas3',
                         'banco do brasil',
                         )

        # checks if the bbas3 has been created
        user_action_user = UserAction.objects.filter(
            user=user,
        )
        self.assertEqual(len(user_action_user), 1)

        # make get request with user=user
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        # checks if the bbas3 is in content
        self.assertIn(
            'bbas3',
            content,
        )

        # checks if the sanp4 is not in content
        self.assertNotIn(
            'sanp4',
            content
        )

    @parameterized.expand([
        ('user_product_id', 'selecione uma ação'),
        ('profits_type', 'selecione um tipo de rendimento'),
        ('date', 'campo obrigatório'),
        ('total_price', 'campo obrigatório'),
        ]
    )
    def test_actions_manage_profits_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        self.make_login()

        # profits data
        profits_data = {
            field: '',
        }

        # make post request
        response = self.client.post(
            self.url,
            profits_data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content
        )

    @parameterized.expand([
        ('user_product_id', '---', 'selecione uma ação'),
        ('date', '20-01-01', 'Informe uma data válida'),
        ]
    )
    def test_actions_manage_profits_returns_error_messages_if_any_field_has_invalid_data(self, field: str, value: str, message: str) -> None:  # noqa: E501
        # make login
        self.make_login()

        # profits data
        profits_data = {
            field: value,
        }

        # make post request
        response = self.client.post(
            self.url,
            profits_data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content
        )

    def test_actions_manage_profits_returns_404_if_user_action_id_belongs_to_another_user(self) -> None:  # noqa: E501
        # create a new user
        another_user = self.create_user(username='anotheruser',
                                        email='anotheruser@email.com',
                                        )

        # create the user_action for another_user
        another_user_action = make_user_action(another_user,
                                               1,
                                               1,
                                               'sanp4',
                                               'sanepar',
                                               )

        # checks if the sanp4 has been created
        user_action_another_user = UserAction.objects.filter(
            user=another_user,
        )
        self.assertEqual(len(user_action_another_user), 1)

        # make login with user=user
        self.make_login()

        # profits data with the id of another user
        profits_data = {
            'user_product_id': another_user_action.id,
            'profits_type': 'jscp',
            'date': '2023-07-02',
            'tax_and_irpf': 2.78,
            'total_price': 50,
        }

        # make post request
        response = self.client.post(
            self.url,
            profits_data,
            follow=True,
        )

        self.assertEqual(response.status_code, 404)

    def test_actions_manage_profits_create_a_new_history_profits_if_all_field_is_ok(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a user_action
        user_action = make_user_action(user,
                                       1,
                                       1,
                                       'bbas3',
                                       'banco do brasil',
                                       )

        # profits data
        profits_data = {
            'user_product_id': user_action.id,
            'profits_type': 'jscp',
            'date': '2023-07-02',
            'tax_and_irpf': 2.78,
            'total_price': 50,
        }

        # make post request
        response = self.client.post(
            self.url,
            profits_data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        # checks if the history has been create
        history = ActionHistory.objects.filter(
            userproduct=user_action,
            handler='jscp',
        )

        self.assertEqual(len(history), 1)
        self.assertEqual(
            history.first().handler,
            'jscp',
        )
        self.assertIn(
            'rendimento para bbas3 lançado com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/acoes/gerenciar-proventos/',
            302,
        )
