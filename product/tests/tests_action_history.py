from django.urls import resolve, reverse
from product.views import ActionHistoryDetails
from utils.mixins.auth import TestCaseWithLogin
from .action_base import make_action
from datetime import date
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

    def test_action_history_get_request_is_allowed_if_user_is_authenticated(self) -> None:  # noqa: E501
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
                'date': date.today().strftime('%Y-%m-%d'),
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
                'date': date.today().strftime('%Y-%m-%d'),
            },
            follow=True
        )

        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/pages/actions/actions_history.html',
            )

    @parameterized.expand([
        ('cnpj: 82794638958601'),
        ('R$ 50,00'),
        ('compra'),
        ('venda'),
        ('R$ 100,00'),
    ])
    def test_action_history_loads_correct_content(self, text) -> None:
        '''
            if the user has the action, the history will contain data
            on purchases, sales, earnings, etc., otherwise a page
            not found will be raised.
        '''
        # make login
        self.make_login()

        # make new action
        make_action('bbas3', 'banco do brasil', '82794638958601')

        # action data
        action_data = {
            'code': 'bbas3',
            'quantity': 5,
            'unit_price': 10,
            'date': date.today().strftime('%Y-%m-%d'),
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

        # access bbas3 action history
        response = self.client.get(
            reverse('product:action_history', args=('bbas3',))
        )
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content,
        )
        # self.fail(
        #     'o arquivo pdf está sendo salvo em duplicidade. '
        #     'salvar o pdf em uma pasta com o nome do usuário. '
        #     )
