from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product.views import FIIHistoryDetails
from product.tests.base_tests import make_fii, make_simple_file
from product.models import UserFII, FiiHistory
from parameterized import parameterized


class FIIsHistoryTests(TestCaseWithLogin):
    url = reverse('product:fii_history', args=('mxrf11',))

    def test_fiis_history_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/fiis/mxrf11/')

    def test_fiis_history_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(response.func.view_class, FIIHistoryDetails)

    def test_fiis_history_returns_status_code_302_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/fiis/mxrf11/',
            302,
        )

    def test_fiis_history_returns_status_code_404_if_fii_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_fiis_history_returns_status_code_405_if_not_get_request(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_fiis_history_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        # create the fii
        make_fii('mxrf11', 'maxi renda')

        # buy the fii
        self.client.post(
            reverse('product:fiis_buy'),
            {
                'code': 'mxrf11',
                'quantity': 10,
                'unit_price': 9.50,
                'date': '2023-07-02',
            },
            follow=True
        )

        # checks template
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'product/partials/_history_variable_income.html',
        )

    def test_fiis_history_returns_status_code_200_if_user_is_authenticated_and_fii_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # create the fii
        make_fii('mxrf11', 'maxi renda')

        # buy the fii
        self.client.post(
            reverse('product:fiis_buy'),
            {
                'code': 'mxrf11',
                'quantity': 10,
                'unit_price': 9.50,
                'date': '2023-07-02',
            },
            follow=True
        )

        # checks history
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fiis_history_creates_a_new_history_if_the_user_buys_a_fii(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # create the fii
        fii = make_fii('mxrf11', 'maxi renda')

        # buy the fii
        self.client.post(
            reverse('product:fiis_buy'),
            {
                'code': 'mxrf11',
                'quantity': 10,
                'unit_price': 9.50,
                'date': '2023-07-02',
                'trading_note': make_simple_file(),
            },
            follow=True
        )

        # get user fii
        user_fii = UserFII.objects.get(
            user=self.get_user('user'),
            product=fii,
        )

        # get user history
        fii_history = FiiHistory.objects.filter(
            userproduct=user_fii,
        )

        # checks if the history has been created
        self.assertEqual(len(fii_history), 1)
        self.assertEqual(
            fii_history[0].userproduct.product.code, 'mxrf11',
        )
        self.assertEqual(fii_history[0].handler, 'buy')
        self.assertEqual(fii_history[0].quantity, 10)
        self.assertEqual(fii_history[0].unit_price, 9.50)
        self.assertEqual(str(fii_history[0].date), ('2023-07-02'))
        self.assertIn(
            '/media/trading-notes/fiis/file_test',
            fii_history[0].trading_note.url,
            )

    def test_fiis_history_creates_a_new_history_if_the_user_sells_a_fii(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # create the fii
        fii = make_fii('mxrf11', 'maxi renda')

        # buy the fii
        self.client.post(
            reverse('product:fiis_buy'),
            {
                'code': 'mxrf11',
                'quantity': 10,
                'unit_price': 9.50,
                'date': '2023-07-02',
                'trading_note': make_simple_file(),
            },
            follow=True
        )

        # sell the fii
        self.client.post(
            reverse('product:fiis_sell'),
            {
                'code': 'mxrf11',
                'quantity': 5,
                'unit_price': 10.75,
                'date': '2024-01-26',
                'trading_note': make_simple_file(),
            },
            follow=True
        )

        # get user fii
        user_fii = UserFII.objects.get(
            user=self.get_user('user'),
            product=fii,
        )

        # get user history
        fii_history = FiiHistory.objects.filter(
            userproduct=user_fii,
        )

        # checks if the history has been created
        self.assertEqual(len(fii_history), 2)
        self.assertEqual(
            fii_history[1].userproduct.product.code, 'mxrf11',
        )
        self.assertEqual(fii_history[1].handler, 'sell')
        self.assertEqual(fii_history[1].quantity, 5)
        self.assertEqual(fii_history[1].unit_price, 10.75)
        self.assertEqual(str(fii_history[1].date), ('2024-01-26'))
        self.assertIn(
            '/media/trading-notes/fiis/file_test',
            fii_history[1].trading_note.url,
            )

    @parameterized.expand([
        ('maxi renda'),
        ('cnpj: 94.961.154/4045-29'),
        ('02/07/23'),
        ('compra'),
        ('R$ 9,50'),
        ('26/01/24'),
        ('venda'),
        ('R$ 10,75'),
        ('nota.pdf'),
    ])
    def test_fiis_history_loads_correct_content(self, text: str) -> None:  # noqa: E501
        # make login
        self.make_login()

        # create the fii
        make_fii('mxrf11', 'maxi renda', cnpj='94961154404529')

        # buy the fii
        self.client.post(
            reverse('product:fiis_buy'),
            {
                'code': 'mxrf11',
                'quantity': 10,
                'unit_price': 9.50,
                'date': '2023-07-02',
                'trading_note': make_simple_file(),
            },
            follow=True
        )

        # sell the fii
        self.client.post(
            reverse('product:fiis_sell'),
            {
                'code': 'mxrf11',
                'quantity': 5,
                'unit_price': 10.75,
                'date': '2024-01-26',
                'trading_note': make_simple_file(),
            },
            follow=True
        )

        # make get request into fiis history
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        # checks the content into html
        self.assertIn(
            text,
            content,
        )
