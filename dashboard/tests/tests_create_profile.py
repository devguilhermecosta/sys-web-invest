from django.test import TestCase
from django.test import Client
from django.urls import reverse, resolve
from dashboard import views
from django.contrib.auth.models import User
from parameterized import parameterized
from dashboard.models import Profile


class CreateProfileTests(TestCase):
    def setUp(self):
        self.user_data = {
            'first_name': 'jhon',
            'last_name': 'dhoe',
            'username': 'jhondoe',
            'password': 'password',
            'email': 'jhon@email.com',
        }
        self.user = User.objects.create_user(**self.user_data)
        self.url = reverse('dashboard:create_profile')
        self.c = Client()

        self.profile_data = {
            'user': self.user,
            'cpf': '11111111111',
            'adress': 'street five',
            'number': '10',
            'city': 'New York City',
            'uf': 'NY',
            'cep': '0000000',
        }
        return super().setUp()

    def test_create_profile_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/dashboard/criar_perfil/')

    def test_create_profile_view_is_correct(self) -> None:
        response = resolve(self.url)
        self.assertEqual(response.func.view_class, views.CreateProfile)

    def make_login(self):
        response = self.c.post(
            reverse('dashboard:home'),
            {
                'user': self.user_data.get('username'),
                'password': self.user_data.get('password'),
            },
            follow=True,
        )
        return response

    def test_create_profile_redirect_to_login_page_if_user_is_not_logged_in(self) -> None:  # noqa: E501
        response = self.c.get(
            reverse('dashboard:create_profile'),
            follow=True,
        )

        self.assertRedirects(
            response,
            '/?next=/dashboard/criar_perfil/',
            302,
        )

    def test_create_profile_load_correct_template(self) -> None:
        # first we make the login
        self.make_login()

        response = self.c.get(self.url)
        self.assertTemplateUsed(response,
                                'dashboard/pages/profile.html',
                                )

    def test_create_profile_get_request_have_status_code_200(self) -> None:
        self.make_login()
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
        self.make_login()

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

    def test_create_profile_loads_the_form_for_create_profile_if_user_does_not_have_a_profile(self) -> None:  # noqa: E501
        self.make_login()

        response = self.c.post(
            reverse('dashboard:home'),
            {
                'user': 'jhondoe',
                'password': 'password'
            },
            follow=True,
        )

        self.assertIn(
            ('Antes de continuarmos, vamos configurar '
             'seu perfil de usuário.'),
            response.content.decode('utf-8')
        )
        self.assertRedirects(
            response,
            reverse('dashboard:create_profile'),
            302,
        )

    def test_create_profile_does_not_loads_the_form_for_create_profile_if_user_have_a_profile(self) -> None:  # noqa: E501
        self.make_login()

        Profile.objects.create(**self.profile_data)

        response = self.c.post(
            reverse('dashboard:home'),
            {
                'user': 'jhondoe',
                'password': 'password'
            },
            follow=True,
        )

        self.assertIn(
            ' login realizado com sucesso',
            response.content.decode('utf-8')
        )
        self.assertRedirects(
            response,
            reverse('dashboard:user_dashboard'),
            302,
        )

    def test_create_profile_redirect_to_user_dashboard_if_user_have_a_profile(self) -> None:  # noqa: E501
        # create the user profile
        Profile.objects.create(**self.profile_data)

        # make login
        self.c.post(
            reverse('dashboard:home'),
            {
                'user': 'jhondoe',
                'password': 'password',
            },
            follow=True,
        )

        # make get request in create profile page
        response = self.c.get(
            reverse('dashboard:create_profile'),
            follow=True,
        )

        self.assertRedirects(
            response,
            '/dashboard/',
            302,
        )

    @parameterized.expand([
        ('cpf', 'Campo obrigatório'),
        ('adress', 'Campo obrigatório'),
        ('number', 'Campo obrigatório'),
        ('city', 'Campo obrigatório'),
        ('uf', 'Campo obrigatório'),
        ('cep', 'Campo obrigatório'),
    ])
    def test_create_profile_returns_required_field_if_field_length_less_then_igual_zero(self, field, message) -> None:  # noqa: E501:
        # set field profile data
        self.profile_data[field] = ''

        # make login
        self.make_login()

        # try create profile
        response = self.c.post(
            reverse('dashboard:create_profile'),
            data=self.profile_data,
            follow=True,
        )
        self.assertIn(message, response.content.decode('utf-8'))

    def test_create_profile_returns_error_message_if_cpf_is_invalid(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # set profile_data
        self.profile_data['cpf'] = '111.111.111-11'

        # try create profile
        response = self.c.post(
            reverse('dashboard:create_profile'),
            data=self.profile_data,
            follow=True,
        )

        self.assertIn('CPF inválido', response.content.decode('utf-8'))

    def test_create_profile_returns_error_message_if_cpf_length_less_then_11(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # set profile_data
        self.profile_data['cpf'] = '111.111.111'

        # try create profile
        response = self.c.post(
            reverse('dashboard:create_profile'),
            data=self.profile_data,
            follow=True,
        )

        self.assertIn('CPF inválido', response.content.decode('utf-8'))

    def test_create_profile_returns_a_new_profile_if_all_ok(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # set profile_data with a valid cpf
        self.profile_data['cpf'] = '616.451.320-05'

        # try create profile
        response = self.c.post(
            reverse('dashboard:create_profile'),
            data=self.profile_data,
            follow=True,
        )

        self.assertIn(
            'Perfil criado com sucesso',
            response.content.decode('utf-8'),
            )
        self.assertRedirects(
            response,
            reverse('dashboard:user_dashboard'),
            302,
        )

    def test_create_profile_returns_error_message_if_cpf_is_already_in_use(self) -> None:  # noqa: E501
        self.fail('O código está funcionando, mas o teste não')
