from django.test import TestCase
from django.http import HttpResponse
from django.urls import reverse, resolve, ResolverMatch
from django.contrib.auth.models import User
from parameterized import parameterized
from user.views import UserRegister


class UserRegisterFormTests(TestCase):
    def setUp(self, *args, **kwargs):
        self.user_register_data: dict = {
            'first_name': 'fname',
            'last_name': 'lname',
            'username': 'username',
            'email': 'email@email.com',
            'email_repeat': 'email@email.com',
        }
        return super().setUp(*args, **kwargs)

    def make_post_request(self, **kwargs) -> HttpResponse:
        data: dict = kwargs.pop('data', {})
        request: HttpResponse = self.client.post(
            reverse('user:register_create'),
            data=data if data else self.user_register_data,
            follow=True,
        )
        return request

    def test_user_form_register_url_is_correct(self) -> None:
        url: str = reverse('user:register_create')
        self.assertEqual(url, '/usuario/registrar/register_create/')

    def test_user_form_register_view_func_is_correct(self) -> None:
        request: ResolverMatch = resolve(
            reverse('user:register_create'),
        )
        self.assertEqual(request.func.view_class, UserRegister)

    def test_user_form_register_status_code_should_be_302_redirect(self) -> None:  # noqa: E501
        request: HttpResponse = self.client.post(
            reverse('user:register_create'),
            data=self.user_register_data,
        )
        self.assertEqual(request.status_code, 302)

    def test_user_form_register_status_code_should_be_200_if_follow(self) -> None:  # noqa: E501
        request: HttpResponse = self.make_post_request()
        self.assertEqual(request.status_code, 200)

    @parameterized.expand([
        ('first_name', 'Campo obrigatório'),
        ('last_name', 'Campo obrigatório'),
        ('username', 'Campo obrigatório'),
        ('email', 'Campo obrigatório'),
        ('email_repeat', 'Campo obrigatório'),
    ])
    def test_user_form_register_required_all_fields(self, field, message):
        self.user_register_data[field] = ''
        request: HttpResponse = self.make_post_request()
        content: str = request.content.decode('utf-8')

        self.assertIn(message, content)

    @parameterized.expand([
        ('first_name', 'O nome deve ter entre 3 e 128 caracteres'),
        ('last_name', 'O sobrenome deve ter entre 3 e 128 caracteres'),
        ('username', 'O Usuário deve ter entre 4 e 128 caracteres'),
    ])
    def test_user_form_register_fields_has_min_length(self,
                                                      field,
                                                      message,
                                                      ) -> None:
        self.user_register_data[field] = 'a'

        request: HttpResponse = self.make_post_request()
        content: str = request.content.decode('utf-8')

        self.assertIn(message, content)

    @parameterized.expand([
        ('first_name', 'O nome deve ter entre 3 e 128 caracteres'),
        ('last_name', 'O sobrenome deve ter entre 3 e 128 caracteres'),
        ('username', 'O Usuário deve ter entre 4 e 128 caracteres'),
    ])
    def test_user_form_register_fields_has_max_length(self,
                                                      field,
                                                      message,
                                                      ) -> None:
        self.user_register_data[field] = 129 * 'a'

        request: HttpResponse = self.make_post_request()
        content: str = request.content.decode('utf-8')

        self.assertIn(message, content)

    def test_user_form_register_returns_email_should_be_equal_if_email_and_email_repeat_are_diferents(self) -> None:  # noqa: E501
        self.user_register_data['email'] = 'email@email.com'
        self.user_register_data['email_repeat'] = 'anotheremail@email.com'

        request: HttpResponse = self.make_post_request()
        content: str = request.content.decode('utf-8')

        self.assertIn('Os e-mails precisam ser iguais', content)

    def test_user_form_register_returns_username_exists_if_this_exists(self) -> None:  # noqa: E501
        user_data: dict = {
            'first_name': 'another jhon',
            'last_name': 'another doe',
            'username': 'jhondoe',
        }
        user: User = User.objects.create(**user_data)
        user.save()

        # same user that above
        request: HttpResponse = self.make_post_request(data=user_data)
        content: str = request.content.decode('utf-8')

        self.assertIn('Usuário já cadastrado', content)

    def test_user_form_register_returns_email_exists_if_this_exists(self) -> None:  # noqa: E501
        user_data: dict = {
            'first_name': 'jhon',
            'last_name': 'dhoe',
            'username': 'jhondoe',
            'email': 'jhon@email.com'
        }
        user: User = User.objects.create(**user_data)
        user.save()

        # same email and user that above
        request: HttpResponse = self.make_post_request(data=user_data)
        content: str = request.content.decode('utf-8')

        self.assertIn('Este e-mail já está em uso', content)
