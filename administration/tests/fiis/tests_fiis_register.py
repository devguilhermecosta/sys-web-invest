from django.urls import resolve, reverse
from parameterized import parameterized

from product.models import FII
from product.tests.base_tests import make_fii, make_fii_in_batch
from utils.mixins.auth import TestCaseWithLogin

from administration import views


class FIIsRegisterTests(TestCaseWithLogin):
    url = reverse('admin:fii_register')

    def test_fii_register_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/painel-de-controle/cadastrar/fii/',
        )

    def test_fii_register_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FIIRegister,
        )

    def test_fii_register_returns_status_code_302_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without begins logged in
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/painel-de-controle/cadastrar/fii/',
            302,
        )

    def test_fii_register_redirects_the_page_to_dashboard_if_the_user_is_not_staff(self) -> None:  # noqa: E501
        # make login with a common user
        self.make_login()

        # make get request without begins logged in
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/dashboard/painel-do-usuario/',
            302,
        )

    def test_fii_register_returns_status_code_200_if_the_user_is_staff(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fii_register_loads_correct_template(self) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'administration/pages/product_register.html',
        )

    @parameterized.expand([
        'Registrar novo FII',
        'código',
        'descrição',
        'cnpj',
        'registrar',
        'editar',
        'deletar',
    ])
    def test_fii_register_loads_correct_content(self, text: str) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # create an action
        make_fii('mxrf11', 'maxi renda')

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )

    def test_fii_register_loads_default_message_if_no_registered_product(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request without an registered product
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            'nenhum produto cadastrado',
            content,
        )

    @parameterized.expand([
        'mxrf11',
        'maxi renda',
        '97.521.225/0001-25',
    ])
    def test_fii_register_loads_the_registered_fiis(self, text: str) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the 5 fiis in batch
        make_fii_in_batch(5)

        # create a individual fii
        make_fii('mxrf11', 'maxi renda', cnpj='97.521.225/0001-25')

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
        ('code', 'O código deve ter 6 caracteres'),
        ('description', 'A descrição deve ter pelo menos 3 caracteres'),
        ('cnpj', 'CNPJ inválido'),
    ])
    def test_fii_register_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
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
        ('code', '123', 'O código deve ter 6 caracteres'),
        ('description', '', 'A descrição deve ter pelo menos 3 caracteres'),
        ('cnpj', '97.521.225/0001', 'CNPJ inválido'),
    ])
    def test_fii_register_returns_error_messages_if_any_field_is_invalid(self, field: str, value: str, message: str) -> None:  # noqa: E501
        # make login with user staff
        self.make_login(is_staff=True)

        # fii data
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
        ('code', 'mxrf11', 'Este código já está em uso'),
        ('description', 'maxi renda', ''),
        ('cnpj', '97.521.225/0001-25', 'Este CNPJ já está em uso'),
    ])
    def test_fii_register_returns_error_messages_if_any_data_is_already_in_use(self, field: str, value: str, message: str) -> None:  # noqa: E501
        # make login with user staff
        self.make_login(is_staff=True)

        # create an fii
        make_fii('mxrf11', 'maxi renda', '97.521.225/0001-25')

        # fii data
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

    def test_fii_register_returns_success_message_if_all_fields_is_ok(self) -> None:  # noqa: E501
        # make login with user staff
        self.make_login(is_staff=True)

        # fii data
        data = {
            'code': 'mxrf11',
            'description': 'maxi renda',
            'cnpj': '97.521.225/0001-25',
        }

        # make post request
        response = self.client.post(
            self.url,
            data,
            follow=True,
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'FII criado com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            self.url,
            302,
        )

    def test_fii_register_creates_a_new_fii_object_if_all_field_is_ok(self) -> None:  # noqa: E501
        # make login with user staff
        self.make_login(is_staff=True)

        # fii data
        data = {
            'code': 'mxrf11',
            'description': 'maxi renda',
            'cnpj': '97.521.225/0001-25',
        }

        # make post request
        self.client.post(
            self.url,
            data,
            follow=True,
        )

        fiis = FII.objects.all()

        self.assertEqual(len(fiis), 1)
