from unittest import TestCase
from utils.password.generate_password import create_password


class GeberatePasswordTests(TestCase):
    def test_generate_password_return_a_password_with_20_chars(self):
        password: str = create_password()
        self.assertEqual(len(password), 20)

    def test_generate_password_is_string_object(self):
        password: str = create_password()
        self.assertTrue(isinstance(password, str))

    def test_generate_password_remove_double_and_single_quotes(self):
        password: str = create_password()
        self.assertNotIn('"', password)
        self.assertNotIn("'", password)
