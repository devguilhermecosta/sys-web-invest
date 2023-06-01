from django.test import TestCase
from django.http import HttpResponse
from django.urls import reverse
from parameterized import parameterized


class UserRegisterFormTests(TestCase):
    def setUp(self, *args, **kwargs):
        self.user_register_data: dict = {
            'first_name': 'fname',
            'last_name': 'lname',
            'username': 'username',
            'email': 'email',
            'password': 'password',
            'password_repeat': 'password',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('first_name', 'Campo obrigatório'),
        ('last_name', 'Campo obrigatório'),
        ('username', 'Campo obrigatório'),
        ('email', 'Campo obrigatório'),
        ('password', 'Campo obrigatório'),
        ('password_repeat', 'Campo obrigatório'),
    ])
    def test_user_form_register_required_all_fields(self, field, message):
        self.user_register_data[field] = ''
        response: HttpResponse = self.client.post(
            reverse('user:register_create'),
            data=self.user_register_data,
            follow=True,
        )
        content: str = response.content.decode('utf-8')

        self.assertIn(message, content)
        self.fail('testar tudo o que foi criado até agora')
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
