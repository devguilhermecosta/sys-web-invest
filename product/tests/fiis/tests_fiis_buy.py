from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product.views import FIISBuyView
from product.models import UserFII, FiiHistory
from product.tests.base_tests import make_fii, make_simple_file
from parameterized import parameterized


class FIIsBuyTests(TestCaseWithLogin):
    url = reverse('product:fiis_buy')

    def test_fiis_buy_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/fiis/comprar/')

    def test_fiis_buy_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertEqual(response.func.view_class, FIISBuyView)

    def test_fiis_buy_get_request_302_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/fiis/comprar/',
            302,
        )

    def test_fiis_buy_returns_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fiis_buy_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'product/pages/fiis/fiis_buy.html',
        )

    @parameterized.expand([
        ('código'),
        ('quantidade'),
        ('valor unitário'),
        ('data'),
        ('trading_note'),
    ])
    def test_fiis_buy_loads_correct_content(self, text: str) -> None:
        # make login
        self.make_login()

        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(text, content)

    @parameterized.expand([
        ('code', 'Campo obrigatório'),
        ('quantity', 'Campo obrigatório'),
        ('unit_price', 'Campo obrigatório'),
        ('date', 'Campo obrigatório'),
    ])
    def test_fiis_buy_returns_error_messages_if_any_field_form_are_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        self.make_login()

        # fii data
        user_fii_data = {
            field: '',
        }

        # make fii
        make_fii('mxrf11', 'maxi renda')

        # try buy fii without data
        response = self.client.post(
            self.url,
            user_fii_data,
            follow=True
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content
        )
        self.assertRedirects(
            response,
            '/ativos/fiis/comprar/',
            302,
        )

    def test_fiis_buy_returns_error_messages_if_fii_code_are_incorrect(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # fii data
        user_fii_data = {
            'code': '123',
        }

        # try buy fii without data
        response = self.client.post(
            self.url,
            user_fii_data,
            follow=True
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'O código deve ter 6 caracteres',
            content
        )
        self.assertRedirects(
            response,
            '/ativos/fiis/comprar/',
            302,
        )

    def test_fiis_buy_returns_error_messages_if_fii_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # fii data
        user_fii_data = {
            'code': 'mxrf11',
        }

        # try buy fii without create the fii object
        response = self.client.post(
            self.url,
            user_fii_data,
            follow=True
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Código MXRF11 não encontrado',
            content
        )
        self.assertRedirects(
            response,
            '/ativos/fiis/comprar/',
            302,
        )

    def test_fiis_buy_returns_error_messages_if_quantity_or_unit_price_are_less_then_zero(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # fii data
        user_fii_data = {
            'quantity': -1,
            'unit_price': -1,
        }

        # try buy fii
        response = self.client.post(
            self.url,
            user_fii_data,
            follow=True
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            'O valor deve ser maior que zero',
            content
        )
        self.assertIn(
            'A quantidade deve ser maior que zero',
            content
        )
        self.assertRedirects(
            response,
            '/ativos/fiis/comprar/',
            302,
        )

    def test_fiis_buy_creates_a_new_fii_object_if_this_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # create the fii
        fii = make_fii('mxrf11', 'maxi renda')

        # fii data
        user_fii_data = {
            'code': 'mxrf11',
            'quantity': 10,
            'unit_price': 9.50,
            'date': '2023-07-01',
            'trading_note': make_simple_file(),
        }

        # try buy fii
        response = self.client.post(
            self.url,
            user_fii_data,
            follow=True
        )
        content = response.content.decode('utf-8')

        user_fii = UserFII.objects.filter(
            product=fii
        )

        user_fii_history = FiiHistory.objects.filter(
            userproduct=user_fii[0],
        )

        self.assertIn(
            'compra de 10 unidade(s) de MXRF11 realizada com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/fiis/',
            302,
        )
        # checks if the new fii has been saved into databases
        self.assertEqual(len(user_fii), 1)

        # checks if the trading note has been saved into media folder
        self.assertIn(
            '/media/trading-notes/fiis/file_test',
            user_fii_history[0].trading_note.url,
        )

    def test_fiis_buy_sum_the_quantity_into_the_fii_existing(self) -> None:  # noqa: E501
        '''
            When te user already has the FII, if he buys again, the quantity
            will be added together.
        '''
        # make login
        self.make_login()

        # create the fii
        fii = make_fii('mxrf11', 'maxi renda')

        # fii data
        user_fii_data = {
            'code': 'mxrf11',
            'quantity': 10,
            'unit_price': 9.50,
            'date': '2023-07-01',
            'trading_note': make_simple_file(),
        }

        # the user buy the fii at first time
        self.client.post(
            self.url,
            user_fii_data,
            follow=True
        )

        # Get the user fii into databases
        user_fii = UserFII.objects.filter(
            user=self.get_user('user'),
            product=fii,
        )

        # checks if the quantity is 10 and total price is 95.00
        self.assertEqual(user_fii.first().quantity, 10)
        self.assertEqual(user_fii.first().get_total_price(), 95.00)

        # fii data 2
        user_fii_data_2 = {
            'code': 'mxrf11',
            'quantity': 20,
            'unit_price': 9.50,
            'date': '2023-07-01',
            'trading_note': make_simple_file(),
        }

        # the user buy the fii at second time
        self.client.post(
            self.url,
            user_fii_data_2,
            follow=True
        )

        # checks if the quantity is 30 and total price is 285.00
        self.assertEqual(user_fii.first().quantity, 30)
        self.assertEqual(user_fii.first().get_total_price(), 285.00)
