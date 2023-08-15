from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from .. import views
from product.tests.base_tests import make_fii
from product.models import FII
from parameterized import parameterized


class FIIEditTests(TestCaseWithLogin):
    url = reverse('admin:fii_edit', args=('mxrf11',))

    def test_fiis_edit_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/painel-de-controle/cadastrar/fii/mxrf11/editar/',
        )

    def test_fiis_edit_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FIIUpdate,
        )

    def test_fiis_edit_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without make login
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/?next=/painel-de-controle/cadastrar/fii/mxrf11/editar/',
            302,
        )

    def test_fiis_edit_is_not_allowed_if_the_user_is_logged_in_but_is_not_a_staff(self) -> None:  # noqa: E501
        # make login with a common user
        self.make_login()

        # make get request
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/dashboard/painel-do-usuario/',
            302,
        )

    def test_fiis_edit_returns_status_code_404_if_the_fii_does_not_exists(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request without an existing fii
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_fiis_edit_returns_status_code_200_if_the_user_is_logged_in_and_is_a_staff(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the fii
        make_fii('mxrf11', 'maxi renda')

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_fiis_edit_loads_correct_template(self) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the fii
        make_fii('mxrf11', 'maxi renda')

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'administration/pages/product_register.html',
        )

    @parameterized.expand([
        '/painel-de-controle/cadastrar/fii/',  # link back to page
        'maxi renda',
        'mxrf11',
        '97.521.225/0001-25',
        'salvar',
    ])
    def test_fiis_edit_loads_correct_content(self, text: str) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the fii
        make_fii('mxrf11', 'maxi renda', '97.521.225/0001-25')

        # make get request
        response = self.client.get(self.url)

        self.assertIn(
            text,
            response.content.decode('utf-8'),
        )

    # post request

    @parameterized.expand([
        ('code', 'O código deve ter 6 caracteres'),
        ('description', 'A descrição deve ter pelo menos 3 caracteres'),
        ('cnpj', 'CNPJ inválido'),
    ])
    def test_fiis_edit_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the fii
        make_fii('mxrf11', 'maxi renda', '97.521.225/0001-25')

        # fii edit data
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
        ('code', 'pvbi11', 'Este código já está em uso'),
        ('cnpj', '35.652.102/0001-76', 'Este CNPJ já está em uso'),
    ])
    def test_fiis_edit_returns_error_messages_if_the_code_and_the_cnpj_is_already_in_use(self, field: str, value: str, message: str) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the first fii
        make_fii('mxrf11', 'maxi renda', '97.521.225/0001-25')

        # create the second fii
        make_fii('pvbi11', 'vbi prime properties', '35.652.102/0001-76')

        # fii edit data
        data = {
            field: value,
        }

        # tries edit the mxrf11 with the same data that pvbi11
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

    def test_fiis_edit_returns_error_message_if_the_cnpj_is_invalid(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the fii
        make_fii('mxrf11', 'maxi renda', '97.521.225/0001-25')

        # tries edit the fii with a invalid cnpj
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

    def test_fiis_edit_returns_success_message_if_all_field_is_ok(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the fii
        make_fii('mxrf11', 'maxi renda', '97.521.225/0001-25')

        # make post request
        response = self.client.post(
            self.url,
            {
                'code': 'pvbi11',
                'description': 'vbi prime properties',
                'cnpj': '35.652.102/0001-76',
            },
            follow=True,
            )

        self.assertIn(
            'salvo com sucesso',
            response.content.decode('utf-8'),
        )
        self.assertRedirects(
            response,
            '/painel-de-controle/cadastrar/fii/',
            302,
        )

    def test_fiis_edit_changes_the_fii_data_if_all_field_is_ok(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # create the fii
        make_fii('mxrf11', 'maxi renda', '97.521.225/0001-25')

        # make post request
        self.client.post(
            self.url,
            {
                'code': 'pvbi11',
                'description': 'vbi prime properties',
                'cnpj': '35.652.102/0001-76',
            },
            follow=True,
            )

        # checks if the fiis data has been changed
        fii = FII.objects.first()
        self.assertEqual(fii.code, 'pvbi11')
        self.assertEqual(fii.description, 'vbi prime properties')
        self.assertEqual(fii.cnpj, '35.652.102/0001-76')
