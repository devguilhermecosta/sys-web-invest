from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from dashboard import views
from utils.mixins.auth import TestCaseWithLogin


class DashboardTests(TestCaseWithLogin):
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
        self.make_login()

        response = self.client.get(
            reverse('dashboard:user_dashboard')
        )

        self.assertEqual(response.status_code, 200)

    def test_dashboard_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        response: HttpResponse = self.client.get(
            reverse('dashboard:user_dashboard')
        )

        self.assertTemplateUsed(response, 'dashboard/pages/dashboard.html')

    def test_dashboard_loads_correct_content(self) -> None:
        # make login
        self.make_login()

        response: HttpResponse = self.client.get(
            reverse('dashboard:user_dashboard')
        )

        content = response.content.decode('utf-8')

        self.assertIn(
            'meus investimentos',
            content,
        )
        self.fail('testar o valor total investido em cada categoria de ativo')
