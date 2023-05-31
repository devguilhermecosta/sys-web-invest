from django.test import TestCase
from parameterized import parameterized


class UserRegisterFormTests(TestCase):
    def setUp(self, *args, **kwargs):
        self.user_register_data: dict = {
            'first_name': 'fname',
            'last_name': 'lname',
            'username': 'username',
            'email': 'email@email.com',
            'password': 'password',
            'password_repeat': 'password2',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('first_name', 'Este campo é obrigatório'),
        ('last_name', 'Este campo é obrigatório'),
        ('username', 'Este campo é obrigatório'),
        ('email', 'Este campo é obrigatório'),
        ('password', 'Este campo é obrigatório'),
        ('password_repeat', 'Este campo é obrigatório'),
    ])
    def test_user_form_register_required_all_fields(self):
        ...
