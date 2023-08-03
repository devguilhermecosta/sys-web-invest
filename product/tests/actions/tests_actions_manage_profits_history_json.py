from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product.tests.base_tests import (
    create_actions_history,
    make_user_action,
    )
from product import views


class ActionManageProfitsHistoryJsonTests(TestCaseWithLogin):
    url = reverse('product:action_history_json')

    def test_actions_manage_profits_history_json_url_is_correct(self) -> None:  # noqa: E501
        self.assertEqual(
            self.url,
            '/ativos/acoes/gerenciar-proventos/historico/json/',
        )

    def test_actions_manage_profits_history_json_uses_correct_view(self) -> None:  # noqa: E501
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ActionsManageProfitsHistoryView,
        )

    def test_actions_manage_profits_history_json_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without make login
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/acoes/gerenciar-proventos/historico/json/',
            302,
        )

    def test_actions_manage_profits_history_json_returns_status_code_200_if_use_is_authenticated(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make get request
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_actions_manage_profits_history_json_returns_status_code_404_if_post_request(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make post request
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_actions_manage_profits_history_json_returns_a_json_response_with_the_profits_history(self) -> None:  # noqa: E501
        # make login and create a new history
        create_actions_history(self.client, self.make_login)

        # make get request
        response = self.client.get(self.url)

        self.assertIn(
            '{"data": [{"date": "2023-07-02", "product": '
            '"bbas3", "handler": "dividends", "tax": 0, '
            '"gross_value": 10.0, "final_value": 10.0, '
            '"history_id": 1}]}',
            response.content.decode('utf-8')
        )

    def test_actions_manage_profits_history_returns_a_json_response_with_correct_data_only_from_the_logged_in_user(self) -> None:  # noqa: E501
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
            'bbas3',
            'banco do brasil',
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

        # make get request with another_user
        response_another_user = self.client.get(self.url)

        expected_another_user_content = (
            '{"data": [{"date": "2023-07-02", "product": '
            '"bbas3", "handler": "dividends", "tax": 1.0, '
            '"gross_value": 10.0, "final_value": 9.0, '
            '"history_id": 1}]}'
        )

        # checks if the response for another_user is correct
        self.assertIn(
            expected_another_user_content,
            response_another_user.content.decode('utf-8')
        )

        # make logout with the another_user
        self.client.logout()

        #########

        # make login with user=user
        _, user = self.make_login()

        # make the user action
        user_action = make_user_action(
            user,
            1,
            1,
            'sanp4',
            'sanepar',
        )

        # make post request for save the profits
        self.client.post(
            reverse('product:actions_manage_profits'),
            {
                'userproduct': user_action.id,
                'handler': 'jscp',
                'date': '2024-12-31',
                'tax_and_irpf': 0,
                'total_price': 580,
            },
            follow=True,
        )

        # make get request with user=user
        response = self.client.get(self.url)

        # checks if the content is correct
        self.assertIn(
            '{"data": [{"date": "2024-12-31", "product": "sanp4", '
            '"handler": "jscp", "tax": 0, "gross_value": 580.0, '
            '"final_value": 580.0, "history_id": 2}]}',
            response.content.decode('utf-8')
        )

        # checks if the content of another_user is not in the user's response
        self.assertNotIn(
            expected_another_user_content,
            response.content.decode('utf-8'),
        )
