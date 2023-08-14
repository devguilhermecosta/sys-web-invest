from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from .. import views


class ActionEditTests(TestCaseWithLogin):
    reverse('admin:actions_edit', args=(1,))

    def test_actions_edit_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/cadastrar/acao/1/editar/',
        )

    def test_actions_edit_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ActionEdit,
        )
