from django.test import TestCase
from django.test import Client
from django.urls import reverse, resolve
from dashboard import views
from parameterized import parameterized


class CreateProfileTests(TestCase):
    def setUp(self):
        self.url = reverse('dashboard:create_profile')
        self.c = Client()
        return super().setUp()

    def test_create_profile_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/dashboard/criar_perfil/')

    def test_create_profile_view_is_correct(self) -> None:
        response = resolve(self.url)
        self.assertEqual(response.func.view_class, views.CreateProfile)

    def test_create_profile_load_correct_template(self) -> None:
        response = self.c.get(self.url)
        self.assertTemplateUsed(response,
                                'dashboard/pages/profile.html',
                                )

    def test_create_profile_get_request_have_status_code_200(self) -> None:
        response = self.c.get(self.url)
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        ('cpf'),
        ('endereço'),
        ('número'),
        ('cidade'),
        ('estado'),
        ('cep'),
    ])
    def test_create_profile_get_request_load_correct_content(self, label) -> None:  # noqa: E501
        response = self.c.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            label,
            content,
        )
        self.assertIn(
            'finalizar',
            content
        )
        self.fail(
            ('Continuar a partir daqui. '
             'Criar a lógica para ser direcionado para o form '
             'de cadastro de perfil se o usuário não tiver '
             'um perfil cadastrado. '
             'Criar a validação do formulário de cadastro '
             'de perfil. '
             'Colocar todos os forms e um único template.')
        )
