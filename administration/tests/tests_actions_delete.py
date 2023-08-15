from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product.models import Action
from product.tests.base_tests import make_action, make_user_action
from administration import views


class ActionsDeleteTests(TestCaseWithLogin):
    url = reverse('admin:action_delete', args=('bbas3',))

    def test_actions_delete_urls_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/painel-de-controle/cadastrar/action/bbas3/deletar/',
        )

    def test_actions_delete_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ActionDelete,
        )

    def test_actions_delete_is_not_allowed_if_the_user_is_not_logged_in(self) -> None:  # noqa: E501
        # make post request without is logged in
        response = self.client.post(self.url, follow=True)

        self.assertRedirects(
            response,
            '/?next=/painel-de-controle/cadastrar/action/bbas3/deletar/',
            302,
        )

    def test_actions_delete_is_not_allowed_if_the_user_is_logged_in_but_is_not_a_staff(self) -> None:  # noqa: E501
        ''' the user is redirected to dashboard '''
        # make login with a common user
        self.make_login()

        # create the action
        make_action('bbas3', 'banco do brasil')

        # make post request
        response = self.client.post(self.url, follow=True)

        self.assertRedirects(
            response,
            '/dashboard/painel-do-usuario/',
            302,
        )

    def test_actions_delete_returns_status_code_404_with_a_common_logged_in_user_if_get_request(self) -> None:  # noqa: E501
        # make login with a common user
        self.make_login()

        # create the action
        make_action('bbas3', 'banco do brasil')

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_actions_delete_returns_status_code_404_with_a_staff_logged_in_user_if_get_request(self) -> None:  # noqa: E501
        # make login with a staff user
        self.make_login(is_staff=True)

        # create the action
        make_action('bbas3', 'banco do brasil')

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_actions_delete_returns_status_code_404_if_the_action_does_not_exists(self) -> None:  # noqa: E501
        # make login with a staff user
        self.make_login(is_staff=True)

        # make post request without an existing action
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_actions_delete_returns_error_message_if_the_action_is_used_by_any_user(self) -> None:  # noqa: E501
        # make login with a staff user
        _, user = self.make_login(is_staff=True)

        # create the action and user_action
        make_user_action(user, 'bbas3', 'banco do brasil')

        # make post request
        response = self.client.post(self.url, follow=True)

        self.assertIn(
            'Este ativo não pode ser deletado, '
            'pois está em uso por algum usuário.',
            response.content.decode('utf-8')
        )
        self.assertRedirects(
            response,
            '/painel-de-controle/cadastrar/acao/',
            302,
        )

    def test_actions_delete_returns_success_message_if_the_action_is_deleted(self) -> None:  # noqa: E501
        # make login with a staff user
        self.make_login(is_staff=True)

        # created the action
        make_action('bbas3', 'banco do brasil')

        # make post request
        response = self.client.post(self.url, follow=True)

        self.assertIn(
            'ativo deletado com sucesso',
            response.content.decode('utf-8')
        )
        self.assertRedirects(
            response,
            '/painel-de-controle/cadastrar/acao/',
            302,
        )

    def test_actions_delete_remove_the_action_from_db_if_the_action_is_deleted(self) -> None:  # noqa: E501
        # make login with a staff user
        self.make_login(is_staff=True)

        # created the action
        make_action('bbas3', 'banco do brasil')

        # checks if the action exists
        actions = Action.objects.filter(code='bbas3')
        self.assertEqual(len(actions), 1)

        # make post request
        self.client.post(self.url, follow=True)

        # checks again if the action exists
        # the length must be zero
        actions = Action.objects.filter(code='bbas3')
        self.assertEqual(len(actions), 0)
