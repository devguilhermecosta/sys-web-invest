from django.test import TestCase
from django.contrib.auth.models import User
from utils.tokens.token_generate import account_activation_token


class TokenGenerateTests(TestCase):
    def setUp(self) -> None:
        self.user_data = {
            'first_name': 'fname',
            'last_name': 'name',
            'username': 'username',
            'password': 'password',
        }
        self.user = User.objects.create(**self.user_data)
        return super().setUp()

    def test_token_genarate_returns_a_string_token(self) -> None:
        token: str = account_activation_token.make_token(self.user)
        self.assertTrue(isinstance(token, str))

    def test_token_genarate_returns_a_token_length_equal_39(self) -> None:
        token: str = account_activation_token.make_token(self.user)
        self.assertEqual(len(token), 39)

    def test_token_genarate_returns_is_unic(self) -> None:
        self.user_data.update({'username': 'anotheruser'})
        user_2 = User.objects.create(**self.user_data)
        toke_1 = account_activation_token.make_token(self.user)
        token_2 = account_activation_token.make_token(user_2)
        self.assertFalse(toke_1 == token_2)
