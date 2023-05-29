from django.test import TestCase
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from dashboard import views


class DashboardTests(TestCase):
    def test_url_home_is_correct(self) -> None:
        url: str = reverse('dashboard:home')
        self.assertEqual(url, '/')

    def test_home_view_is_correct(self) -> None:
        url: str = reverse('dashboard:home')
        response: ResolverMatch = resolve(url)
        self.assertEqual(response.func.view_class, views.HomeView)

    def test_home_load_correct_template(self) -> None:
        url: str = reverse('dashboard:home')
        response: HttpResponse = self.client.get(url)
        self.assertTemplateUsed(response, 'dashboard/pages/home.html')

    def test_home_load_form_for_sign_in_or_sign_up(self) -> None:
        url: str = reverse('dashboard:home')
        response: HttpResponse = self.client.get(url)
        content: str = response.content.decode('utf-8')
        self.assertIn('usuário', content)
        self.assertIn('senha', content)
        self.assertIn('esqueci minha senha', content)
        self.assertIn('entrar', content)
        self.assertIn('registrar', content)
