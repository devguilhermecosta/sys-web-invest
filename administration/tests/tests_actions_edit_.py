from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from .. import views


class ActionEditTests(TestCaseWithLogin):
    reverse('admin:actions_edit', args=(1,))

    def test_actions_edit_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/cadastrar/acao/mxrf11/editar/',
        )

    def test_actions_edit_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ActionEdit,
        )

    def test_actions_edit_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without make login
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/?next=/painel-de-controle/cadastrar/acao/mxrf11/editar/',
            302,
        )
