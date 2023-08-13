from utils.mixins.auth import TestCaseWithLogin
from django.urls import reverse, resolve
from .. import views


class ActionsRegisterTests(TestCaseWithLogin):
    url = reverse('admin:action_register')

    def test_action_register_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/painel-de-controle/cadastrar/acao/',
        )

    def test_action_register_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ActionRegister,
        )


# organizar as views das ações e fiis
