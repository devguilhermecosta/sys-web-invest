from utils.mixins.auth import TestCaseWithLogin
from django.urls import reverse, resolve
from product import views
from product.tests.base_tests import make_fixed_income_product
from product.models import ProductFixedIncome, FixedIncomeHistory
from parameterized import parameterized


class FixedIncomeProfitsReceiptTests(TestCaseWithLogin):
    url = reverse('product:fixed_income_profits_receipt', args=(1,))

    def test_fixed_income_profits_receipt_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/renda-fixa/1/receber-juros/',
        )

    def test_fixed_income_profits_receipt_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FixedIncomeProfitsReceiptView,
        )

    def test_fixed_income_profits_receipt_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without being logged in
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/renda-fixa/1/receber-juros/',
            302,
        )

    def test_fixed_income_profits_receipt_returns_status_code_404_if_the_product_dont_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make get request without an existing product
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_fixed_income_profits_receipt_returns_status_code_404_if_the_product_belongs_to_another_user(self) -> None:  # noqa: E501
        # create an another user and create an product fixed income
        another_user = self.create_user(username='another_user',
                                        email='another@email.com',
                                        )
        make_fixed_income_product(user=another_user,
                                  name='cdb meliuz 2026')

        # check if the another_user's product was created
        products = ProductFixedIncome.objects.filter(user=another_user)
        self.assertEqual(len(products), 1)
        self.assertEqual(products.first().name,
                         'cdb meliuz 2026',
                         )

        # make login with user=user
        self.make_login()

        # making a GET request to get another user's product
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_fixed_income_profits_receipt_returns_status_code_200_if_the_user_is_authenticated_and_the_product_exists(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a product fixed income
        make_fixed_income_product(user=user)

        # make get request
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fixed_income_profits_receipt_loads_correct_template(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a product fixed income
        make_fixed_income_product(user=user)

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/partials/_dt_and_fi_default_form.html',
        )

    @parameterized.expand([
        'CDB C6 2026',
        'data',
        'valor bruto',
        'taxas e impostos',
        'receber',
    ])
    def test_fixed_income_profits_receipt_loads_correct_content(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a product fixed income
        make_fixed_income_product(user=user, name='cdb c6 2026')

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )

    @parameterized.expand([
        ('date', 'Campo obrigatório'),
        ('value', 'Campo obrigatório'),
    ])
    def test_fixed_income_profits_receipt_returns_error_messages_if_any_field_is_empty(self, field: str, message: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a product fixed income
        make_fixed_income_product(user=user, name='cdb c6 2026')

        # profits receipt data
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

    def test_fixed_income_profits_receipt_returns_success_message_if_the_form_is_ok(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a product fixed income
        make_fixed_income_product(user=user, name='cdb c6 2026')

        # profits receipt data
        data = {
            'date': '2023-07-02',
            'value': 10,
        }

        # make post request
        response = self.client.post(
            self.url,
            data,
            follow=True,
            )
        content = response.content.decode('utf-8')

        self.assertIn(
            'Recebimento de juros salvo com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/renda-fixa/1/detalhes/',
            302,
        )

    def test_fixed_income_profits_receipt_creates_a_new_history_if_form_is_ok(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a product fixed income
        p = make_fixed_income_product(user=user, name='cdb c6 2026')

        # profits receipt data
        data = {
            'date': '2023-07-02',
            'value': 10,
            'tax_and_irpf': 1,
        }

        # make post request
        self.client.post(
            self.url,
            data,
            follow=True,
            )

        # get the profits history
        history = FixedIncomeHistory.objects.filter(
            product=p,
            state='profits',
        )

        self.assertEqual(len(history), 1)
        self.assertEqual(str(history.first().date), '2023-07-02')
        self.assertEqual(history.first().get_final_value(), 9)
        self.assertEqual(history.first().tax_and_irpf, -1)
