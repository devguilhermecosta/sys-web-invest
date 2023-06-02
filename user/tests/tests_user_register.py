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


"""
se for bem sucedido, a primeira senha do usuário será gerada
de forma aleatória
e um e-mail com recuperação de senha será enviado para o usuário
definiruma senha.
No primeiro acesso o usuário deverá criar o perfil.
modificar o CSS da animação do form para um JS.
Talvez ao invés de modificar o css, mudar o min_lenght
e max_length para ser validado no clean_field, e não
nos atributos na declaração de cada field.
"""
