from utils.mixins.auth import TestCaseWithLogin
from django.urls import reverse, resolve
from product import views
from parameterized import parameterized


class FixedIncomeRegisterTests(TestCaseWithLogin):
    url = reverse('product:fixed_income_register')

    def test_fixed_income_register_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/renda-fixa/registrar/')

    def test_fixed_income_register_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FixedIncomeRegisterView,
        )

    def test_fixed_income_register_returns_status_code_302_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/renda-fixa/registrar/',
            302,
        )

    def test_fixed_income_register_returns_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fixed_income_register_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'product/pages/fixed_income/fixed_income_register.html',
        )

    @parameterized.expand([
        ('categoria'),
        ('nome'),
        ('valor'),
        ('carência'),
        ('vencimento'),
        ('liquidez'),
        ('rentabilidade'),
        ('pagamento de juros'),
        ('observações'),
    ])
    def test_fixed_income_register_loads_correct_content(self, text: str) -> None:  # noqa: E501
        # make login
        self.make_login()

        # get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )

    @parameterized.expand([
        ('category', 'Campo obrigatório'),
        ('name', 'Campo obrigatório'),
        ('value', 'Campo obrigatório'),
        ('grace_period', 'Campo obrigatório'),
        ('maturity_date', 'Campo obrigatório'),
        ('liquidity', 'Campo obrigatório'),
        ('profitability', 'Campo obrigatório'),
        ('interest_receipt', 'Campo obrigatório'),
        ('description', 'Campo obrigatório'),
    ])
    def test_fixed_income_register_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        self.make_login()

        # form data
        form_data = {
            field: '',
        }

        # make post request
        response = self.client.post(
            self.url,
            form_data,
            follow=True,)
        content = response.content.decode('utf-8')

        # error messages
        self.assertIn(
            message,
            content,
        )
        self.assertRedirects(
            response,
            self.url,
            302,
        )

    def test_fixed_income_register_create_a_new_object_if_data_is_ok(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # form data
        form_data = {
            'user': user,
            'category': 'cdb',
            'name': 'cdb banco inter',
            'value': 12580.78,
            'grace_period': '2023-07-06',
            'maturity_date': '2025-07-06',
            'liquidity': 'nv',
            'profitability': '120% cdi',
            'interest_receipt': 'nh',
            'description': 'um cdb muito bom',
        }

        # make post request
        response = self.client.post(
            self.url,
            form_data,
            follow=True,)
        content = response.content.decode('utf-8')

        self.assertIn(
            "Ativo CDB BANCO INTER criado com sucesso.",
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/renda-fixa/',
            302,
        )

    def test_fail(self) -> None:
        self.fail('talvez usar o help text?')
