from django.urls import resolve, reverse
from product.views import ActionHistoryDetails
from product.models import UserAction, ActionHistory
from utils.mixins.auth import TestCaseWithLogin
from ..base_tests import make_action, make_simple_file
from parameterized import parameterized


class ActionHistoryTests(TestCaseWithLogin):
    url = reverse('product:action_history', args=('cash3',))

    def test_action_history_uses_correct_url(self) -> None:
        self.assertEqual(self.url, '/ativos/acoes/cash3/')

    def test_action_history_loads_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            ActionHistoryDetails,
        )

    def test_action_history_returns_status_code_302_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/acoes/cash3/',
            302,
        )

    def test_action_history_returns_status_code_404_if_the_user_does_not_have_the_action(self) -> None:  # noqa: 501
        # make login
        self.make_login()

        # request with action code 'cash3'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_actions_history_returns_status_code_405_if_not_get_request(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_action_history_get_request_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: 501
        # make login
        self.make_login()

        # create the new action
        make_action('cash3', 'meliuz')

        # buy the action
        self.client.post(
            reverse('product:actions_buy'),
            {
                'code': 'cash3',
                'quantity': '1',
                'unit_price': 1,
                'date': '2023-07-02',
            },
            follow=True
        )

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_action_history_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        # create the new action
        make_action('cash3', 'meliuz')

        # buy the action
        self.client.post(
            reverse('product:actions_buy'),
            {
                'code': 'cash3',
                'quantity': '1',
                'unit_price': 1,
                'date': '2023-07-02',
            },
            follow=True
        )

        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/partials/_history_variable_income.html',
            )

    def test_action_history_creates_a_new_history_if_user_buys_the_action(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make new action
        action = make_action('bbas3', 'banco do brasil')

        # buy the action
        self.client.post(
            reverse('product:actions_buy'),
            {
                'code': 'bbas3',
                'quantity': 5,
                'unit_price': 10,
                'date': '2023-07-02',
                'trading_note': make_simple_file(),
            },
            follow=True
        )

        # get user action
        user_action = UserAction.objects.get(
            user=self.get_user('user'),
            product=action
        )

        # get action history
        action_history = ActionHistory.objects.filter(
            userproduct=user_action,
        )

        # checks history
        self.assertEqual(len(action_history), 1)
        self.assertEqual(
            action_history[0].userproduct.product.code, 'bbas3',
        )
        self.assertEqual(
            str(action_history[0].date), '2023-07-02',
        )
        self.assertEqual(action_history[0].handler, 'buy')
        self.assertEqual(action_history[0].quantity, 5)
        self.assertEqual(action_history[0].unit_price, 10)
        self.assertIn(
            '/media/trading-notes/actions/file_test',
            action_history[0].trading_note.url,
            )

    def test_action_history_creates_a_new_history_if_user_sells_the_action(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make new action
        action = make_action('bbas3', 'banco do brasil')

        # buy the action
        self.client.post(
            reverse('product:actions_buy'),
            {
                'code': 'bbas3',
                'quantity': 5,
                'unit_price': 10,
                'date': '2023-07-02',
                'trading_note': make_simple_file(),
            },
            follow=True
        )

        # sell the action
        self.client.post(
            reverse('product:actions_sell'),
            {
                'code': 'bbas3',
                'quantity': 4,
                'unit_price': 25,
                'date': '2023-12-02',
                'trading_note': make_simple_file(),
            },
            follow=True
        )

        # get user action
        user_action = UserAction.objects.get(
            user=self.get_user('user'),
            product=action
        )

        # get action history
        action_history = ActionHistory.objects.filter(
            userproduct=user_action,
        )

        # checks history
        self.assertEqual(len(action_history), 2)
        self.assertEqual(
            action_history[1].userproduct.product.code, 'bbas3',
        )
        self.assertEqual(
            str(action_history[1].date), '2023-12-02',
        )
        self.assertEqual(action_history[1].handler, 'sell')
        self.assertEqual(action_history[1].quantity, -4)
        self.assertEqual(action_history[1].unit_price, 25)
        self.assertIn(
            '/media/trading-notes/actions/file_test',
            action_history[1].trading_note.url,
            )

    @parameterized.expand([
        'bbas3',
        'banco do brasil',
        'cnpj: 82.794.638/9586-01',
        'total acumulado em proventos',
        'R$ 129,00',
        'R$ 50,00',
        'R$ 100,00',
        'compra',
        'venda',
        'deletar',
        '/ativos/acoes/1/historico/1/deletar/'
    ])
    def test_action_history_loads_correct_content(self, text) -> None:
        '''
            if the user has the action, the history will contain data
            on purchases, sales, earnings, etc., otherwise a page
            not found will be raised.
        '''
        # make login
        _, user = self.make_login()

        # make new action
        make_action('bbas3', 'banco do brasil', '82794638958601')

        # get the user action
        user_action = UserAction.objects.filter(
            user=user,
        )

        # action data
        action_data = {
            'code': 'bbas3',
            'quantity': 5,
            'unit_price': 10,
            'date': '2023-07-02',
        }

        # buy the action
        self.client.post(
            reverse('product:actions_buy'),
            action_data,
            follow=True
        )

        # set action data
        action_data.update({
            'unit_price': 20,
        })

        # Try sell 5 units of bbas3
        self.client.post(
            reverse('product:actions_sell'),
            action_data,
            follow=True,
        )

        # Try receve profits
        user_action[0].receive_profits(
            'dividends',
            '2023-10-27',
            129,
            0,
        )

        # access bbas3 action history
        response = self.client.get(
            reverse('product:action_history', args=('bbas3',))
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )
