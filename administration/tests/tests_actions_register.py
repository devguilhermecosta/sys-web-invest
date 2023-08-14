from django.urls import resolve, reverse
from parameterized import parameterized
from utils.mixins.auth import TestCaseWithLogin
from .. import views
from product.tests.base_tests import make_action_in_batch, make_action
from product.models import Action


class ActionsRegisterTests(TestCaseWithLogin):
    url = reverse('admin:action_register')

    def test_action_register_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/painel-de-controle/cadastrar/acao/',
        )

    def test_action_register_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ActionRegister,
        )

    def test_action_register_returns_status_code_302_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without begins logged in
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/painel-de-controle/cadastrar/acao/',
            302,
        )

    def test_action_register_redirects_the_page_to_dashboard_if_the_user_is_not_staff(self) -> None:  # noqa: E501
        # make login with a common user
        self.make_login()

        # make get request without begins logged in
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/dashboard/painel-do-usuario/',
            302,
        )

    def test_action_register_returns_status_code_200_if_the_user_is_staff(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_action_register_loads_correct_template(self) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'administration/pages/product_register.html',
        )

    @parameterized.expand([
        'Registrar nova Ação',
        'código',
        'descrição',
        'cnpj',
        'registrar',
        'editar',
        'deletar',
    ])
    def test_action_register_loads_correct_content(self, text: str) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # create an action
        make_action('bbas3', 'banco do brasil')

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )

    @parameterized.expand([
        'bbas3',
        'banco do brasil',
        '00.000.000/0001-91',
    ])
    def test_action_register_loads_the_registered_actions(self, text: str) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the 5 actions in batch
        make_action_in_batch(5)

        # create a individual action
        make_action('bbas3', 'banco do brasil', cnpj='00.000.000/0001-91')

        # make get request
        response = self.client.get(self.url)
        context = response.context
        content = response.content.decode('utf-8')

        # checks the actions context
        self.assertEqual(
            len(context['products']),
            6,
        )
        self.assertIn(
            text,
            content,
        )

    @parameterized.expand([
        ('code', 'Campo obrigatório'),
        ('description', 'Campo obrigatório'),
        ('cnpj', 'Campo obrigatório'),
    ])
    def test_action_register_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login with user staff
        self.make_login(is_staff=True)

        # action data
        data = {
            field: '',
        }

        # make post request
        response = self.client.post(
            self.url,
            data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content,
        )
        self.assertRedirects(
            response,
            self.url,
            302,
        )

    @parameterized.expand([
        ('code', '123', 'O código deve ter 5 caracteres'),
        ('description', '', 'A descrição deve ter pelo menos 3 caracteres'),
        ('cnpj', '00.000.000/0001', 'Cnpj inválido'),
    ])
    def test_action_register_returns_error_messages_if_any_field_is_invalid(self, field: str, value: str, message: str) -> None:  # noqa: E501
        # make login with user staff
        self.make_login(is_staff=True)

        # action data
        data = {
            field: value,
        }

        # make post request
        response = self.client.post(
            self.url,
            data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content,
        )
        self.assertRedirects(
            response,
            self.url,
            302,
        )

    @parameterized.expand([
        ('code', 'bbas3', 'Ação já registrada'),
        ('description', 'banco do brasil', ''),
        ('cnpj', '00.000.000/0001-91', 'CNPJ já registrado'),
    ])
    def test_action_register_returns_error_messages_if_any_data_is_already_in_use(self, field: str, value: str, message: str) -> None:  # noqa: E501
        # make login with user staff
        self.make_login(is_staff=True)

        # create an action
        make_action('bbas3', 'banco do brasil', '00.000.000/0001-91')

        # action data
        data = {
            field: value,
        }

        # make post request
        response = self.client.post(
            self.url,
            data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content,
        )
        self.assertRedirects(
            response,
            self.url,
            302,
        )

    def test_action_register_returns_success_message_if_all_fields_is_ok(self) -> None:  # noqa: E501
        # make login with user staff
        self.make_login(is_staff=True)

        # action data
        data = {
            'code': 'bbas3',
            'description': 'banco do brasil',
            'cnpj': '00.000.000/0001-91',
        }

        # make post request
        response = self.client.post(
            self.url,
            data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Ação criada com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            self.url,
            302,
        )

    def test_action_register_creates_a_new_action_object_if_all_field_is_ok(self) -> None:  # noqa: E501
        # make login with user staff
        self.make_login(is_staff=True)

        # action data
        data = {
            'code': 'bbas3',
            'description': 'banco do brasil',
            'cnpj': '00.000.000/0001-91',
        }

        # make post request
        self.client.post(
            self.url,
            data,
            follow=True,
        )

        actions = Action.objects.all()

        self.assertEqual(len(actions), 1)
