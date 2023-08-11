from django.urls import reverse, resolve
from django.test import override_settings
from parameterized import parameterized
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.models import UserAction
from ..base_tests import make_action, make_simple_file
from product.models import ActionHistory
from datetime import date
import shutil
import contextlib


TEST_DIR = 'test_data'


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class ActionsBuyTests(TestCaseWithLogin):
    url = reverse('product:actions_buy')
    date = date.today().strftime('%Y-%m-%d')

    def setUp(self) -> None:
        self.action_data = {
            'code': 'bbas3',
            'quantity': '1',
            'unit_price': '10',
            'date': self.date,
        }
        return super().setUp()

    def tearDown(self) -> None:
        with contextlib.suppress(OSError):
            shutil.rmtree(TEST_DIR)
        return super().tearDown()

    def test_actions_get_request_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/acoes/comprar/')

    def test_actions_get_request_is_redirected_if_user_not_logget_in(self) -> None:  # noqa: E501
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/?next=/ativos/acoes/comprar/',
            302,
        )

    def test_actions_get_request_status_code_200_if_user_is_logged_in(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # access actions buy with get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_actions_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(response.func.view_class, views.ActionsBuyView)

    def test_actions_loads_correct_template(self) -> None:
        # make_login
        self.make_login()

        # access actions buy with get request
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'product/pages/actions/actions_buy.html'
        )

    def test_actions_loads_correct_content(self) -> None:
        # make_login
        self.make_login()

        # access actions buy with get request
        response = self.client.get(self.url)

        content = response.content.decode('utf-8')

        self.assertIn('código', content)
        self.assertIn('quantidade', content)
        self.assertIn('valor unitário', content)
        self.assertIn('comprar', content)

    @parameterized.expand([
        ('code', 'Campo obrigatório'),
        ('quantity', 'Campo obrigatório'),
        ('unit_price', 'Campo obrigatório'),
        ('date', 'Campo obrigatório'),
    ])
    def test_actions_buy_returns_error_messages_if_any_field_is_empty(self, field, message) -> None:  # noqa: E501
        # make login
        self.make_login()

        # try buy the action
        response = self.client.post(
            self.url,
            {
                f'{field}': '',
            },
            follow=True
        )

        self.assertIn(message, response.content.decode('utf-8'))

    def test_actions_buy_returns_error_messages_if_action_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # try buy the action
        response = self.client.post(
            self.url,
            self.action_data,
            follow=True
        )

        self.assertIn(
            f'Código {self.action_data["code"].upper()} não encontrado',
            response.content.decode('utf-8'),
            )

    def test_actions_buy_returns_success_messages_if_action_is_purchased_and_create_a_new_user_action(self) -> None:  # noqa: E501
        '''
            the total application property is dynamically generated
            through the yfinance library, so testing this value is difficult,
            so your test is not included here.
        '''
        # make login
        self.make_login()

        # make new action
        action = make_action('bbas3', 'banco do brasil')

        # try buy the action
        response = self.client.post(
            self.url,
            self.action_data,
            follow=True,
        )

        # Try get new user_action into the databases
        user_action = UserAction.objects.filter(
            user=self.get_user(username='user'),
            product=action,
        ).first()

        # checks if the success message is displayed
        self.assertIn(
            (
                f'compra de {self.action_data["quantity"]} unidade(s) de '
                f'{self.action_data["code"].upper()} '
                'realizada com sucesso'
            ),
            response.content.decode('utf-8'),
            )

        self.assertEqual(user_action.product.code, 'bbas3')

        # checks if the user was redirected after purchase
        self.assertRedirects(
            response,
            '/ativos/acoes/',
            302,
        )

    def test_actions_buy_update_the_user_action_if_action_exists_into_databases(self) -> None:  # noqa: E501
        """
            if user was purchase the same action, is not allowed
            create a new object, this should just update the existing action.

            the total application property is dynamically generated
            through the yfinance library, so testing this value is difficult,
            so your test is not included here.
        """
        # make login
        self.make_login()

        # make new action
        action = make_action('bbas3', 'banco do brasil')

        # set action_data for the first time
        self.action_data.update(
            {
                'quantity': 1,
                'unit_price': 10,
            }
            )

        # buy the action for the first time
        self.client.post(
            self.url,
            self.action_data,
            follow=True
        )

        # Try get new user_action into databases
        user_action = UserAction.objects.filter(
            user=self.get_user(username='user'),
            product=action,
        )

        # checks if the user_action was saved in the databases
        self.assertTrue(user_action.exists())

        # cheks if quantity and price are corrects
        # the quantity must be 1 and the total_price must be **
        self.assertEqual(user_action.first().get_quantity(), 1)

        # set action_data for the second time
        self.action_data.update(
            {
                'quantity': 10,
                'unit_price': 30,
            }
            )

        # buy the action for the second time
        self.client.post(
            self.url,
            self.action_data,
            follow=True
        )

        # cheks if quantity and price are updated
        # now, the quantity must be 11 and the total_price must be **
        self.assertEqual(user_action.first().get_quantity(), 11)

    def test_actions_buy_creates_a_action_history_after_purchase(self) -> None:  # noqa: E501
        ''' after the each action purchase, automatically a new history
            will be create with handler 'buy'.
            the trading note is optional.
        '''
        # make login
        self.make_login()

        # make new action
        action = make_action('bbas3', 'banco do brasil')

        # insert the trading note into action data
        self.action_data.update({
            'trading_note': make_simple_file(),
        })

        # buy the action
        self.client.post(
            self.url,
            self.action_data,
            follow=True,
        )

        # get the new user_action into the databases
        user_action = UserAction.objects.filter(
            user=self.get_user(username='user'),
            product=action,
        ).first()

        # get queryset from action history
        action_history = ActionHistory.objects.filter(
            userproduct=user_action,
        )

        self.assertEqual(len(action_history), 1)

        # checks action history buy
        self.assertIn(
            'compra de 1 unidade(s) de bbas3 do usuário user realizada no dia',
            str(action_history[0]),
        )

        # checks is the trading note has been uploaded
        self.assertIn(
            '/trading-notes/actions/file_test',
            action_history[0].trading_note.url,
        )
