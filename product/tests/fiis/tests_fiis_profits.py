from django.urls import resolve, reverse
from product import views
from product.tests.base_tests import make_user_fii
from product.models import UserFII
from utils.mixins.auth import TestCaseWithLogin
from parameterized import parameterized


class FIIsProfitsTests(TestCaseWithLogin):
    url = reverse('product:fiis_manage_income')

    def test_fiis_profits_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/fiis/gerenciar-proventos/'
        )

    def test_fiis_profits_loads_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FIIManageIncomeReceipt,
        )

    def test_fiis_profits_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/fiis/gerenciar-proventos/',
            302,
        )

    def test_fiis_profits_is_allowed_if_user_is_authenticated(self) -> None:
        self.make_login()
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_fiis_profits_loads_correct_template(self) -> None:
        self.make_login()

        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/pages/fiis/fiis_profits.html'
        )

    @parameterized.expand([
        ('Receber Proventos',),
        ('fii',),
        ('MXRF11',),
        ('data',),
        ('valor',),
        ('salvar',)
    ])
    def test_fiis_profits_loads_correct_content_when_not_profits(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # make user fii for populate select input
        make_user_fii(
            user,
            1,
            1,
            'mxrf11',
            'maxi renda',
        )

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content
        )

    @parameterized.expand([
        ('fii', 'Campo obrigatório'),
        ('date', 'Campo obrigatório'),
        ('value', 'Campo obrigatório'),
    ])
    def test_fiis_profits_returns_error_messages_if_any_field_is_empty(self, field: str, msg: str) -> None:  # noqa: E501
        # make login
        self.make_login()

        # data
        data = {
            field: '',
        }

        # make post request
        response = self.client.post(
            self.url,
            data=data,
            follow=True,
        )

        self.assertIn(
            msg,
            response.content.decode('utf-8')
        )
        self.assertRedirects(
            response,
            '/ativos/fiis/gerenciar-proventos/',
            302,
        )

    def test_fiis_profits_returns_success_json_response_if_all_fields_is_ok(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # make the user fii
        user_fii = make_user_fii(
            user=user,
            qty=1,
            unit_price=10,
            code='mxrf11',
            desc='maxi renda',
        )

        # data
        data = {
            'product_id': user_fii.pk,
            'date': '2023-07-02',
            'value': 4.96,
        }

        # make post request
        response = self.client.post(
            self.url,
            data=data,
        )

        self.assertIn(
            '{"success": "success request"}',
            response.content.decode('utf-8')
        )

    def test_fiis_profits_create_a_new_history_and_increases_the_earnings_accumulated_field(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # make the user fii
        user_fii = make_user_fii(
            user=user,
            qty=1,
            unit_price=10,
            code='mxrf11',
            desc='maxi renda',
        )

        # data
        data = {
            'product_id': user_fii.pk,
            'date': '2023-07-02',
            'value': 4.96,
        }

        # make post request
        self.client.post(
            self.url,
            data=data,
        )

        # get user_fii
        u_fii = UserFII.objects.get(pk=1)

        # get_history
        history = u_fii.get_partial_history('profits')[0]

        self.assertEqual(
            u_fii.earnings_accumulated,
            4.96
        )
        self.assertEqual(
            history.handler,
            'profits',
        )
        self.assertEqual(
            str(history.date),
            '2023-07-02',
        )
        self.assertEqual(
            history.total_price,
            4.96
        )
