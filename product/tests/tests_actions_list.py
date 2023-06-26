from utils.mixins.auth import TestCaseWithLogin
from django.urls import reverse, resolve
from .action_base import make_action
from product import views
from datetime import date


class ActionsListTests(TestCaseWithLogin):
    url = reverse('product:actions_list')

    def test_actions_list_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/acoes/lista/')

    def test_actions_list_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertEqual(response.func.view_class, views.AllActionsView)

    def test_actions_list_user_is_redirected_to_login_page_if_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/?next=/ativos/acoes/lista/',
            302.
        )

    def test_actions_list_user_access_is_allowed_if_user_is_authenticated(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_actions_list_load_correct_template(self) -> None:
        self.make_login()
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/pages/actions/actions_list.html'
        )

    def test_actions_list_render_only_authenticated_user_actions(self) -> None:
        '''
            this test verifies that the authenticated user's actions
            are not loaded in another user.
        '''
        # create the action
        make_action('bbas3', 'banco do brasil')

        # make login with username 'user'
        self.make_login()

        # buy bbas3 action
        response_actions_buy = self.client.post(
            reverse('product:actions_buy'),
            {
                'code': 'bbas3',
                'quantity': '10',
                'unit_price': '36',
                'date': date.today().strftime('%Y-%m-%d'),
            },
            follow=True,
        )

        # check if the actions has been purchased
        self.assertIn(
            'compra de 10 unidade(s) de BBAS3 realizada com sucesso',
            response_actions_buy.content.decode('utf-8')
            )

        # get request to actions_list url
        response_actions_list = self.client.get(self.url)
        content = response_actions_list.content.decode('utf-8')

        # check if the action BBAS3 is in the actions list
        self.assertIn(
            'bbas3',
            content,
        )
        self.assertIn(
            '10',
            content,
        )

        # make logout with 'user'
        self.client.logout()

        # create the new user with username 'user_2'
        self.create_user(
            with_profile=True,
            username='user_2',
            email='user_2@email.com'
            )

        # make login with user_2
        self.make_login(create_user=False, username='user_2')

        # access actions list
        response_actions_list_user_2 = self.client.get(self.url)
        content_user_2 = response_actions_list_user_2.content.decode('utf-8')

        # checks if the actions list is empty
        self.assertIn('Nenhuma ação até o momento',
                      content_user_2,
                      )
        self.assertNotIn(
            'bbas3',
            content_user_2,
        )
