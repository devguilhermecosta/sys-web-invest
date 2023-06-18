from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from product import views


class ProductActionsTests(TestCase):
    def setUp(self) -> None:
        # create the user
        User.objects.create_user(
            username='user',
            email='email@email.com',
            password='password',
        )
        return super().setUp()

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
        response = self.client.get(
            reverse('product:actions')
        )
        self.assertTemplateUsed(
            response,
            'product/pages/actions.html',
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
        self.client.post(
            reverse('dashboard:home'),
            {
                'user': 'user',
                'password': 'password',
            },
            follow=True,
        )

        # access the dashboard actions
        response = self.client.get(
            reverse('product:actions')
        )

        self.assertEqual(response.status_code, 200)

    def test_actions_loads_correct_content(self) -> None:
        # make login
        self.client.post(
            reverse('dashboard:home'),
            {
                'user': 'user',
                'password': 'password',
            },
            follow=True,
        )

        # access the dashboard actions
        response = self.client.get(
            reverse('product:actions')
        )

        content = response.content.decode('utf-8')

        self.assertIn('minhas ações', content)
        self.assertIn('comprar', content)
        self.assertIn('vender', content)
        self.assertIn('lançar proventos', content)
