from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.models import ActionHistory
from product.tests.base_tests import create_actions_history, make_user_action


class ActionManageProfitsHistoryDeleteTests(TestCaseWithLogin):
    url = reverse('product:action_manage_profits_delete', args=(1,))

    def test_actions_manage_income_history_delete_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/acoes/gerenciar-proventos/historico/1/deletar/',
        )

    def test_actions_manage_income_history_delete_uses_correct_view(self) -> None:  # noqa: E501
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ActionsManageProfitsHistoryDeleteView,
        )

    def test_actions_manage_income_history_delete_returns_status_code_404_if_get_request(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make get request
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_actions_manage_income_history_delete_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make post request without logged in
        response = self.client.post(self.url)

        self.assertRedirects(
            response,
            '/?next=/ativos/acoes/gerenciar-proventos/historico/1/deletar/',
            302,
        )

    def test_actions_manage_income_history_delete_returns_404_if_the_history_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make post request without an existing history
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_actions_manage_income_history_delete_returns_404_if_the_history_does_not_belong_to_the_logged_in_user(self) -> None:  # noqa: E501
        # create another user
        another_user = self.create_user(
            username='jhondoe',
            email='jhondoe@email.com',
        )

        # create the UserAction for another_user
        another_useraction = make_user_action(
            another_user,
            1,
            1,
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
                'total_price': 10,
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

        # create the profits history and make login with user=user
        u = create_actions_history(self.client,
                                   self.make_login,
                                   profits_value=150,
                                   )

        # get the history id of user
        history_id_user = ActionHistory.objects.filter(
            userproduct=u['user_action'],
        )

        # checks if the history_id_user is 2
        self.assertEqual(history_id_user.first().id, 2)

        # now i am logged in with the user
        # i will try to delete the history of id 1 whose another_user owns
        response = self.client.post(self.url)

        # the status code must be 404
        self.assertEqual(response.status_code, 404)

    def test_actions_manage_income_history_delete_returns_a_json_response_it_the_history_is_deleted(self) -> None:  # noqa: E501
        # create a new history and make login
        u = create_actions_history(self.client, self.make_login)

        # checks if the history has been created
        history = ActionHistory.objects.filter(userproduct=u['user_action'])
        self.assertEqual(len(history), 1)
        self.assertEqual(history.first().id, 1)

        # make post request for delete the history
        response = self.client.post(self.url)

        history = ActionHistory.objects.filter(userproduct=u['user_action'])
        self.assertEqual(len(history), 0)
        self.assertRedirects(
            response,
            '/ativos/acoes/gerenciar-proventos/',
            302,
        )
