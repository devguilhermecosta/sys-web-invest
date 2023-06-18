from django.test import TestCase
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from django.contrib.auth.models import User
from dashboard import views


class DashboardTests(TestCase):
    def setUp(self) -> None:
        # create user
        User.objects.create_user(
            username='user',
            email='email@email.com',
            password='password',
        )
        return super().setUp()

    def test_url_dashboard_is_correct(self) -> None:
        url: str = reverse('dashboard:user_dashboard')
        self.assertEqual(url, '/dashboard/painel-do-usuario/')

    def test_dashboard_view_is_correct(self) -> None:
        url: str = reverse('dashboard:user_dashboard')
        response: ResolverMatch = resolve(url)
        self.assertEqual(response.func.view_class, views.DashboardView)

    def test_dashboard_will_be_redirected_if_user_not_logged_in(self) -> None:
        response = self.client.get(
            reverse('dashboard:user_dashboard')
        )
        self.assertRedirects(
            response,
            '/?next=/dashboard/painel-do-usuario/',
            302
        )

    def test_dashboard_status_code_200_if_user_logged_in(self) -> None:
        # make login
        self.client.post(
            reverse('dashboard:home'),
            {
                'user': 'user',
                'password': 'password',
            },
            follow=True,
        )

        response = self.client.get(
            reverse('dashboard:user_dashboard')
        )

        self.assertEqual(response.status_code, 200)

    def test_dashboard_loads_correct_template(self) -> None:
        # make login
        self.client.post(
            reverse('dashboard:home'),
            {
                'user': 'user',
                'password': 'password',
            },
            follow=True,
        )

        response: HttpResponse = self.client.get(
            reverse('dashboard:user_dashboard')
        )

        self.assertTemplateUsed(response, 'dashboard/pages/dashboard.html')

    def test_dashboard_loads_correct_content(self) -> None:
        # make login
        self.client.post(
            reverse('dashboard:home'),
            {
                'user': 'user',
                'password': 'password',
            },
            follow=True,
        )

        response: HttpResponse = self.client.get(
            reverse('dashboard:user_dashboard')
        )

        content = response.content.decode('utf-8')

        self.assertIn(
            'meus investimentos',
            content,
        )
