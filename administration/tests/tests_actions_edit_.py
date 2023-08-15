from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from .. import views
from product.tests.base_tests import make_action
from product.models import Action
from parameterized import parameterized


class ActionEditTests(TestCaseWithLogin):
    url = reverse('admin:action_edit', args=('bbas3',))

    def test_actions_edit_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/painel-de-controle/cadastrar/acao/bbas3/editar/',
        )

    def test_actions_edit_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ActionEdit,
        )

    def test_actions_edit_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without make login
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/?next=/painel-de-controle/cadastrar/acao/bbas3/editar/',
            302,
        )

    def test_actions_edit_is_not_allowed_if_the_user_is_logged_in_but_is_not_a_staff(self) -> None:  # noqa: E501
        # make login with a common user
        self.make_login()

        # make get request
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/dashboard/painel-do-usuario/',
            302,
        )

    def test_actions_edit_returns_status_code_404_if_the_action_does_not_exists(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request without an existing action
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_actions_edit_returns_status_code_200_if_the_user_is_logged_in_and_is_a_staff(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the action
        make_action('bbas3', 'banco do brasil')

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_actions_edit_loads_correct_template(self) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the action
        make_action('bbas3', 'banco do brasil')

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'administration/pages/product_register.html',
        )

    @parameterized.expand([
        '/painel-de-controle/cadastrar/acao/',  # link back to page
        'banco do brasil',
        'bbas3',
        '00.000.000/0001-91',
        'salvar',
    ])
    def test_actions_edit_loads_correct_content(self, text: str) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the action
        make_action('bbas3', 'banco do brasil', '00.000.000/0001-91')

        # make get request
        response = self.client.get(self.url)

        self.assertIn(
            text,
            response.content.decode('utf-8'),
        )

    # post request

    @parameterized.expand([
        ('code', 'O código deve ter 5 caracteres'),
        ('description', 'A descrição deve ter pelo menos 3 caracteres'),
        ('cnpj', 'CNPJ inválido'),
    ])
    def test_actions_edit_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the action
        make_action('bbas3', 'banco do brasil', '00.000.000/0001-91')

        # action edit data
        data = {
            field: '',
        }

        # make post request
        response = self.client.post(
            self.url,
            data,
            follow=True,
            )

        self.assertIn(
            message,
            response.content.decode('utf-8'),
        )
        self.assertRedirects(
            response,
            self.url,
            302,
        )

    @parameterized.expand([
        ('code', 'sanb4', 'Este código já está em uso'),
        ('cnpj', '90.400.888/0001-42', 'Este CNPJ já está em uso'),
    ])
    def test_actions_edit_returns_error_messages_if_the_code_and_the_cnpj_is_already_in_use(self, field: str, value: str, message: str) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the first action
        make_action('bbas3', 'banco do brasil', '00.000.000/0001-91')

        # create the second action
        make_action('sanb4', 'banco santander', '90.400.888/0001-42')

        # action edit data
        data = {
            field: value,
        }

        # tries edit the bbas3 with the same data that sanb4
        response = self.client.post(
            self.url,
            data,
            follow=True,
            )

        self.assertIn(
            message,
            response.content.decode('utf-8'),
        )
        self.assertRedirects(
            response,
            self.url,
            302,
        )

    def test_actions_edit_returns_error_message_if_the_cnpj_is_invalid(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the action
        make_action('bbas3', 'banco do brasil', '00.000.000/0001-91')

        # tries edit the action with a invalid cnpj
        response = self.client.post(
            self.url,
            {
                'cnpj': '00.000.000/0000-00',
            },
            follow=True,
            )

        self.assertIn(
            'CNPJ inválido',
            response.content.decode('utf-8'),
        )
        self.assertRedirects(
            response,
            self.url,
            302,
        )

    def test_actions_edit_returns_success_message_if_all_field_is_ok(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the action
        make_action('bbas3', 'banco do brasil', '00.000.000/0001-91')

        # make post request
        response = self.client.post(
            self.url,
            {
                'code': 'sanb4',
                'description': 'banco santander',
                'cnpj': '90.400.888/0001-42',
            },
            follow=True,
            )

        self.assertIn(
            'salvo com sucesso',
            response.content.decode('utf-8'),
        )
        self.assertRedirects(
            response,
            '/painel-de-controle/cadastrar/acao/',
            302,
        )

    def test_actions_edit_changes_the_action_data_if_all_field_is_ok(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the action
        make_action('bbas3', 'banco do brasil', '00.000.000/0001-91')

        # make post request
        self.client.post(
            self.url,
            {
                'code': 'sanb4',
                'description': 'banco santander',
                'cnpj': '90.400.888/0001-42',
            },
            follow=True,
            )

        # checks if the actions data has been changed
        action = Action.objects.first()
        self.assertEqual(action.code, 'sanb4')
        self.assertEqual(action.description, 'banco santander')
        self.assertEqual(action.cnpj, '90.400.888/0001-42')
