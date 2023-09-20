from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from administration import views
from product.models import Action
from product.tests.base_tests import make_action
from unittest.mock import patch


class ActionsAutoRegisterTests(TestCaseWithLogin):
    url = reverse('admin:action_auto_register')

    def test_actions_auto_register_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/painel-de-controle/cadastrar/auto/acoes/',
        )

    def test_actions_auto_register_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ActionAutoRegister,
        )

    def test_actions_auto_register_returns_status_code_404_if_get_request(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_actions_auto_register_returns_status_code_302_if_the_user_is_not_logged_in(self) -> None:  # noqa: E501
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/?next=/painel-de-controle/cadastrar/auto/acoes/',
            302,
        )

    def test_actions_auto_register_returns_status_code_404_if_the_user_logged_in_is_not_staff(self) -> None:  # noqa: E501
        self.make_login(is_staff=False)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_actions_auto_register_returns_status_code_200_if_the_user_logged_in_is_staff(self) -> None:  # noqa: E501
        self.make_login(is_staff=True)
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_actions_auto_register_creates_several_new_objects(self) -> None:
        # checks the Action length before the update
        all_actions = Action.objects.all()
        self.assertEqual(len(all_actions), 0)

        # update the data base
        self.make_login(is_staff=True)
        self.client.post(self.url, follow=True)

        # checks again the Action length
        all_actions = Action.objects.all()
        self.assertTrue(len(all_actions) > 100)

    def test_actions_auto_register_does_not_register_the_same_registered_action(self) -> None:  # noqa: E501
        # create a new action
        make_action('bbas3', 'banco do brasil')

        # checks if the BBAS3 exists and checks this length
        action = Action.objects.filter(code='bbas3')
        self.assertTrue(action.exists())
        self.assertEqual(len(action), 1)

        # update the data base
        self.make_login(is_staff=True)
        self.client.post(self.url, follow=True)

        # checks again if the BBAS3 exists and checks this length.
        # the length property must be one.
        action = Action.objects.filter(code='bbas3')
        self.assertTrue(action.exists())
        self.assertEqual(len(action), 1)

    def test_actions_auto_register_does_not_register_the_fiis(self) -> None:  # noqa: E501
        # update the data base
        self.make_login(is_staff=True)
        self.client.post(self.url, follow=True)

        # checks if the mxrf11 and xpml11 exists from Action DB.
        # the MXRF11 and XPML11 are a FII.
        query_1 = Action.objects.filter(code='mxrf11')
        query_2 = Action.objects.filter(code='xpml11')
        self.assertFalse(query_1.exists())
        self.assertFalse(query_2.exists())

        # checks if the bbas3 exists from Action DB
        # the BBAS3 must be exists because this is a stock
        query_3 = Action.objects.filter(code='bbas3')
        self.assertTrue(query_3.exists())

    def test_actions_auto_register_returns_success_message_if_ok(self) -> None:  # noqa: E501
        # update the data base
        self.make_login(is_staff=True)
        response = self.client.post(self.url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn(
            'ações registradas com sucesso',
            content,
        )

    def test_actions_auto_register_returns_error_message_if_any_error_occurs(self) -> None:  # noqa: E501
        # create an incorrect url to make request
        new_url = 'https://brapi.dev/api/quote/list/my_error'

        with patch('administration.views.products.base_view.auto_register.AutoRegister.resp',  # noqa: E501
                   new=new_url):

            # tries update the data base
            self.make_login(is_staff=True)
            response = self.client.post(self.url, follow=True)
            content = response.content.decode('utf-8')

            self.assertIn(
                'Erro ao atualizar a lista de ativos.',
                content,
            )
            self.assertRedirects(
                response,
                '/painel-de-controle/cadastrar/acao/',
                302,
            )
