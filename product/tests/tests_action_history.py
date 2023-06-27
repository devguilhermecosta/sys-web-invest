from django.urls import resolve, reverse
from product.views import ActionHistoryDetails
from product.models import UserAction, ActionHistory
from utils.mixins.auth import TestCaseWithLogin
from .action_base import make_action
from .test_base import make_simple_file
from datetime import date


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

    def test_action_history_get_request_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: 501
        # make login
        self.make_login()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_action_history_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/pages/actions/actions_history.html',
            )

    def test_action_history_loads_correct_content(self) -> None:
        '''
            if the user has the action, the history will contain data
            on purchases, sales, earnings, etc., otherwise a page
            not found will be raised.
        '''
        # make login
        _, user = self.make_login()

        # make new action
        make_action('bbas3', 'banco do brasil', '82794638958601')

        action_data = {
            'code': 'bbas3',
            'quantity': 5,
            'unit_price': '10',
            'date': date.today().strftime('%Y-%m-%d'),
            'trading_note': make_simple_file(),
        }

        # buy the action
        self.client.post(
            reverse('product:actions_buy'),
            action_data,
            follow=True
        )

        # sell 5 units of bbas3
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
            'cnpj: 82794638958601',
            content,
        )
        self.assertIn(
            'R$ 50,00',
            content,
        )
        self.assertIn(
            'compra',
            content,
        )
        self.assertIn(
            'venda',
            content,
        )
        self.fail(
            'continuar daqui. Este teste não está funcionando. '
            'o arquivo pdf está sendo salvo em duplicidade. '
            'salvar o pdf em uma pasta com o nome do usuário. '
            )
