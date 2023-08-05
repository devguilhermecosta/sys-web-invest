from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.models import ProductFixedIncome
from product.tests.base_tests import make_fixed_income_product


class ProductFixedIncomeDeleteTests(TestCaseWithLogin):
    url = reverse('product:fixed_income_delete', args=(1,))

    def test_product_fixed_income_delete_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/renda-fixa/1/deletar/',
        )

    def test_product_fixed_income_delete_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FixedIncomeDeleteView,
        )

    def test_product_fixed_income_delete_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/renda-fixa/1/deletar/',
            302,
        )

    def test_product_fixed_income_delete_returns_404_if_get_request(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_product_fixed_income_delete_returns_404_if_the_product_does_not_exists(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_product_fixed_income_delete_remove_the_product_from_data_base(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the product
        make_fixed_income_product(user=user, name='cdb bb')

        # checks if the product has been created
        product = ProductFixedIncome.objects.get(pk=1)
        self.assertTrue(product.description, 'cdb bb')

        # make post request
        self.client.post(self.url)

        # checks if the product has been deleted
        product = ProductFixedIncome.objects.all()
        self.assertFalse(product.exists())

    def test_product_fixed_income_delete_returns_success_message(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the product
        make_fixed_income_product(user=user)

        # make post request
        response = self.client.post(self.url, follow=True)

        self.assertIn(
            'ativo deletado com sucesso',
            response.content.decode('utf-8'),
        )
        self.assertRedirects(
            response,
            '/ativos/renda-fixa/',
            302
        )
