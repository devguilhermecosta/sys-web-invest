from django.urls import reverse, resolve
from product import views
from utils.mixins.auth import TestCaseWithLogin


class ProductActionsTests(TestCaseWithLogin):
    def test_actions_url_is_correct(self) -> None:
        url = reverse('product:actions')
        self.assertEqual(url,
                         '/ativos/acoes/',
                         )

    def test_actions_class_view_is_correct(self) -> None:
        response = resolve(
            reverse('product:actions')
        )
        self.assertEqual(
            response.func.view_class,
            views.ActionsView,
        )

    def test_actions_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        response = self.client.get(
            reverse('product:actions')
        )

        self.assertTemplateUsed(
            response,
            'product/pages/actions/actions.html',
            )

    def test_actions_is_redirected_if_user_not_logged_in(self) -> None:
        response = self.client.get(
            reverse('product:actions')
        )
        self.assertRedirects(
            response,
            '/?next=/ativos/acoes/',
            302,
        )

    def test_actions_status_code_200_if_user_is_logged_in(self) -> None:
        # make login
        self.make_login()

        # access the dashboard actions
        response = self.client.get(
            reverse('product:actions')
        )

        self.assertEqual(response.status_code, 200)

    def test_actions_loads_correct_content(self) -> None:
        # make login
        self.make_login()

        # access the dashboard actions
        response = self.client.get(
            reverse('product:actions')
        )

        content = response.content.decode('utf-8')

        self.assertIn('minhas ações', content)
        self.assertIn('comprar', content)
        self.assertIn('vender', content)
        self.assertIn('lançar proventos', content)
