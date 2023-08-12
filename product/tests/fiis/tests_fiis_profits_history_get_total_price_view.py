from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.tests.base_tests import (
    create_profits_history,
    make_user_fii,
    )


class ProfitsHistoryGetTotalPriceTests(TestCaseWithLogin):
    url = reverse('product:fii_total_profits_json')

    def test_profits_history_get_total_price_url_is_correct(self) -> None:  # noqa: E501
        self.assertEqual(
            self.url,
            '/ativos/fiis/gerenciar-proventos/total-recebido/json/',
        )

    def test_profits_history_get_total_price_uses_correct_view(self) -> None:  # noqa: E501
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.GetTotalProfitsView,
        )

    def test_profits_history_get_total_price_is_not_allowed_if_user_is_not_authenticate(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/fiis/gerenciar-proventos/total-recebido/json/',
            302,
        )

    def test_profits_history_get_total_price_returns_status_code_200_if_user_is_authenticate(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_profits_history_get_total_price_returns_404_if_not_get_request(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.post(self.url)

        self.assertEqual(
            response.status_code,
            404,
        )

    def test_profits_history_get_total_price_returns_a_json_response_with_the_total_profits_received(self) -> None:  # noqa: E501
        # create the profits history
        create_profits_history(self.client, self.make_login)

        # make get request
        response = self.client.get(self.url)

        self.assertIn(
            '{"value": "10.00"}',
            response.content.decode('utf-8'),
        )

    def test_profits_history_get_total_price_returns_a_json_response_with_the_total_profits_received_just_of_the_user_authenticated(self) -> None:  # noqa: E501
        # create another user
        another_user = self.create_user(
            username='jhondoe',
            email='jhondoe@email.com',
        )

        # create the UserFII for another_user
        another_userfii = make_user_fii(
            another_user,
            'pvbi11',
            'teste',
        )

        # make login with the another_user
        self.make_login(create_user=False, username=another_user)

        # make post request for create the history for another_userfii
        # with the value of 50
        r_post = self.client.post(
            reverse('product:fiis_manage_income_receipt'),
            {
                'userproduct': another_userfii.id,
                'total_price': 50,
                'date': '2023-07-02',
            },
            follow=True,
        )

        # checks if the history has been created
        self.assertEqual(
            r_post.content.decode('utf-8'),
            '{"success": "success request"}',
        )

        # make get request for get the total value
        r_get = self.client.get(self.url)

        # checks if the value is 50
        self.assertEqual(
            r_get.content.decode('utf-8'),
            '{"value": "50.00"}',
        )

        # make logout with the another_user
        self.client.logout()

        # create the profits history and make login with user=user
        create_profits_history(self.client,
                               self.make_login,
                               profits_value=150,
                               )

        # make get request with the user logged in
        response = self.client.get(self.url)

        # the response must be 'value: 150'
        self.assertIn(
            '{"value": "150.00"}',
            response.content.decode('utf-8'),
        )
