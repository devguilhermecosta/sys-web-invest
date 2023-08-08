from utils.mixins.auth import TestCaseWithLogin
from django.urls import reverse, resolve
from ...views.fixed_income import FixedIncomeView
from product.tests.base_tests import make_fixed_income_product
from product.models import ProductFixedIncome
from parameterized import parameterized


class FixedIncomeTests(TestCaseWithLogin):
    url = reverse('product:fixed_income')

    def test_fixed_income_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/renda-fixa/')

    def test_fixed_income_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(response.func.view_class, FixedIncomeView)

    def test_fixed_income_returns_status_code_302_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/renda-fixa/',
            302,
        )

    def test_fixed_income_returns_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fixed_income_returns_status_code_405_if_not_get_request(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_fixed_income_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'product/partials/_dt_and_fi_intro.html',
        )

    def test_fixed_income_loads_no_registered_product_if_user_has_no_products(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.get(self.url)

        self.assertIn(
            'nenhum produto cadastrado',
            response.content.decode('utf-8'),
        )

    @parameterized.expand([
        ('cdb bb 2035'),
        ('R$ 1250,00'),
        ('01/01/2035'),
    ])
    def test_fixed_income_loads_correct_content_if_user_has_products(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create object
        make_fixed_income_product(user=user, value=1250)

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        # get queryset
        queryset = ProductFixedIncome.objects.filter(
            user=user
        )

        self.assertIn(
            text,
            content
        )
        self.assertEqual(len(queryset), 1)

    @parameterized.expand([
        ('Aplicação total'),
        ('R$ 1250,00'),
        ('Total recebido em proventos'),
        ('R$ 37,25'),
        ('Total pago em taxas'),
        ('R$ 12,75'),
    ])
    def test_fixed_income_loads_correct_summary(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create object
        make_fixed_income_product(user=user,
                                  value=1250,
                                  tax=12.75,
                                  profits_value=50,
                                  )

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content
        )

    def test_fixed_income_loads_just_products_of_authenticated_user(self) -> None:  # noqa: E501
        # create a new user
        user_one = self.create_user(True,
                                    username='userone',
                                    password='userone@email.com',
                                    )

        # make fixed income with user_one
        make_fixed_income_product(user=user_one,
                                  category='lci',
                                  name='lci fazendinha test',
                                  )

        # make login with username user
        _, user = self.make_login()

        # make fixed income with user
        make_fixed_income_product(user=user,
                                  category='cdb',
                                  name='cdb c6 banck',
                                  )

        # get all fixed income objects
        fixed_income_objs = ProductFixedIncome.objects.all()

        # checks if the two objects has been created
        self.assertEqual(len(fixed_income_objs), 2)
        self.assertEqual(fixed_income_objs[0].name, 'lci fazendinha test')
        self.assertEqual(fixed_income_objs[0].category, 'lci')
        self.assertEqual(fixed_income_objs[1].name, 'cdb c6 banck')
        self.assertEqual(fixed_income_objs[1].category, 'cdb')

        # access fixed income page with user
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        # checks if the user has the correct object
        self.assertIn(
            'cdb c6 banck',
            content,
        )
        self.assertNotIn(
            'lci fazendinha test',
            content,
        )

        # NOW I'M GOING TO TEST IF THE USER'S PRODUCT IS IN USER_ONE

        # make logout with user
        self.client.post(
            reverse('dashboard:logout')
        )

        # make login with user_one
        self.make_login(create_user=False, username='userone')

        # access fixed income page
        response_2 = self.client.get(self.url)
        content_2 = response_2.content.decode('utf-8')

        # checks if the user_one has the correct object
        self.assertIn(
            'lci fazendinha test',
            content_2,
        )
        self.assertNotIn(
            'cdb c6 banck',
            content_2
        )
