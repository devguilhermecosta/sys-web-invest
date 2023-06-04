from django.test import TestCase
from django.urls import reverse, resolve, ResolverMatch
from django.http import HttpResponse
from user import views


class UserRegisterTests(TestCase):
    def test_url_user_register_is_correct(self) -> None:
        url: str = reverse('user:register')
        self.assertEqual(url, '/usuario/registrar/')

    def test_user_register_load_correct_view(self) -> None:
        url: str = reverse('user:register')
        response: ResolverMatch = resolve(url)
        self.assertEqual(
            response.func.view_class,
            views.UserRegister
            )

    def test_user_register_load_correct_template(self) -> None:
        url: str = reverse('user:register')
        response: HttpResponse = self.client.get(url)
        self.assertTemplateUsed(response, 'user/pages/register.html')
