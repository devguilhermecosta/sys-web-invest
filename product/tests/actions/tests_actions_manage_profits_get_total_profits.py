from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.tests.base_tests import (
    create_actions_history,
    make_user_action,
)


class ActionsProfitsGetTotalProfitsTests(TestCaseWithLogin):
    url = reverse('product:action_total_profits_json')

    def test_actions_total_profits_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/acoes/gerenciar-proventos/total-recebido/json/',
        )

    def test_actions_total_profits_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ActionsGetTotalProfitsView,
        )

    def test_actions_total_profits_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        # get request without the user is logged in
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/?next=/ativos/acoes/gerenciar-proventos/total-recebido/json/',
            302,
        )

    def test_actions_total_profits_returns_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_actions_total_profits_returns_status_code_404_if_post_request(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # post request
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_actions_total_profits_returns_a_json_response_with_total_received_in_profits(self) -> None:  # noqa: E501
        # create the action profits history and make login
        create_actions_history(self.client,
                               self.make_login,
                               gross_value=10000,
                               )

        # get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            '{"value": "10000.00"}',
            content
        )

    def test_actions_total_profits_returns_a_json_response_with_total_received_in_profits_only_of_the_logged_in_user(self) -> None:  # noqa: E501
        # create another user
        another_user = self.create_user(
            username='jhondoe',
            email='jhondoe@email.com',
        )

        # create the UserAction for another_user
        another_useraction = make_user_action(another_user,
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
                'total_price': 1500,
            },
            follow=True,
        )

        # checks if the history has been created
        self.assertIn(
            '{"data": "success request"}',
            r_post.content.decode('utf-8'),
        )

        # make logout
        self.client.logout()

        # create the action profits history and make login
        create_actions_history(self.client,
                               self.make_login,
                               gross_value=1500,
                               )

        # get request with user=user
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        # the total value must be 1500, not 3000
        self.assertIn(
            '{"value": "1500.00"}',
            content
        )
