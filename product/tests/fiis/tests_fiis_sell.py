from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product.views import FIIsSellView
from product.models import UserFII
from product.tests.base_tests import make_fii
from parameterized import parameterized


class FIIsSellTests(TestCaseWithLogin):
    url = reverse('product:fiis_sell')

    def test_fiis_sell_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/fiis/vender/')

    def test_fiis_sell_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertEqual(response.func.view_class, FIIsSellView)

    def test_fiis_sell_get_request_status_code_302_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/fiis/vender/',
            302,
        )

    def test_fiis_sell_get_request_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fiis_sell_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'product/pages/fiis/fiis_sell.html'
        )

    @parameterized.expand([
        ('código'),
        ('quantidade'),
        ('valor unitário'),
        ('data'),
        ('trading_note'),
    ])
    def test_fiis_sell_loads_correct_content(self, text: str) -> None:
        # make login
        self.make_login()

        response = self.client.get(self.url)

        self.assertIn(
            text,
            response.content.decode('utf-8')
        )

    @parameterized.expand([
        ('code', 'Campo obrigatório'),
        ('quantity', 'Campo obrigatório'),
        ('unit_price', 'Campo obrigatório'),
        ('date', 'Campo obrigatório'),
    ])
    def test_fiis_sell_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        self.make_login()

        # fii data
        fii_sell_data = {
            field: '',
        }

        response = self.client.post(
            self.url,
            fii_sell_data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/fiis/vender/',
            302,
        )

    def test_fiis_sell_returns_error_message_if_code_length_is_less_then_6(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # fii data
        fii_sell_data = {
            'code': '123',
        }

        response = self.client.post(
            self.url,
            fii_sell_data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            'O código deve ter 6 caracteres',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/fiis/vender/',
            302,
        )

    def test_fiis_sell_returns_error_message_if_code_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # fii data
        fii_sell_data = {
            'code': 'mxrf11',
        }

        response = self.client.post(
            self.url,
            fii_sell_data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Código MXRF11 não encontrado',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/fiis/vender/',
            302,
        )

    @parameterized.expand([
        ('quantity', 'A quantidade deve ser maior que zero'),
        ('unit_price', 'O valor deve ser maior que zero'),
    ])
    def test_fiis_sell_returns_error_messages_if_quantity_or_unit_price_is_less_then_0(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        self.make_login()

        # fii data
        fii_sell_data = {
            field: -1,
        }

        response = self.client.post(
            self.url,
            fii_sell_data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            message,
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/fiis/vender/',
            302,
        )

    def test_fiis_sell_returns_error_message_if_quantity_field_is_biger_then_the_user_action_quantity(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # create the fii
        fii = make_fii('mxrf11', 'maxi renda')

        # fii data for buy fii
        fii_buy_data = {
            'code': 'mxrf11',
            'quantity': 10,
            'unit_price': 8.50,
            'date': '2023-07-01',
        }

        # buy the fii
        self.client.post(
            reverse('product:fiis_buy'),
            fii_buy_data,
            follow=True,
        )

        # check if the fii has been created
        fii = UserFII.objects.filter(
            user=self.get_user('user'),
            fii=fii,
        )
        self.assertTrue(fii.exists())

        # fii data for sell fii
        fii_sell_data = {
            'code': 'mxrf11',
            'quantity': 11,
            'unit_price': 8.50,
            'date': '2023-07-01',
        }

        # try sell the fii
        response = self.client.post(
            self.url,
            fii_sell_data,
            follow=True,
        )
        self.assertIn(
            'Quantidade insuficiente para venda',
            response.content.decode('utf-8'),
        )

    def test_fiis_sell_returns_success_message_if_the_fii_has_been_sold(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # create the fii
        fii = make_fii('mxrf11', 'maxi renda')

        # fii data for buy fii
        fii_buy_data = {
            'code': 'mxrf11',
            'quantity': 10,
            'unit_price': 8.50,
            'date': '2023-07-01',
        }

        # buy the fii
        self.client.post(
            reverse('product:fiis_buy'),
            fii_buy_data,
            follow=True,
        )

        # check if the fii has been created
        fii = UserFII.objects.filter(
            user=self.get_user('user'),
            fii=fii,
        )
        self.assertTrue(fii.exists())

        # fii data for sell fii
        fii_sell_data = {
            'code': 'mxrf11',
            'quantity': 1,
            'unit_price': 8.50,
            'date': '2023-07-01',
        }

        # try sell the fii
        response = self.client.post(
            self.url,
            fii_sell_data,
            follow=True,
        )

        # checks if the fii has been sold
        self.assertIn(
            'venda de 1 unidade(s) de MXRF11 realizada com sucesso',
            response.content.decode('utf-8'),
        )

    def test_fiis_sell_user_fii_quantity_must_have_decreased_if_fii_is_sold(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # create the fii
        fii = make_fii('mxrf11', 'maxi renda')

        # fii data for buy fii
        fii_buy_data = {
            'code': 'mxrf11',
            'quantity': 10,
            'unit_price': 8.50,
            'date': '2023-07-01',
        }

        # buy the fii
        self.client.post(
            reverse('product:fiis_buy'),
            fii_buy_data,
            follow=True,
        )

        # check if the fii has been created
        user_fii = UserFII.objects.filter(
            user=self.get_user('user'),
            fii=fii,
        )
        self.assertTrue(user_fii.exists())

        # fii data for sell fii
        fii_sell_data = {
            'code': 'mxrf11',
            'quantity': 5,
            'unit_price': 10,
            'date': '2023-07-01',
        }

        # try sell the fii
        self.client.post(
            self.url,
            fii_sell_data,
            follow=True,
        )

        # checks if the fii quantity has decreased
        # the quantity must been 5
        user_fii_2 = UserFII.objects.filter(
            user=self.get_user('user'),
            fii=fii,
        )
        self.assertEqual(user_fii_2.first().quantity, 5)
        self.fail('refatorar as views de compra e venda')
