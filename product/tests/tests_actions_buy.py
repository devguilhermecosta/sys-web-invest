from django.urls import reverse, resolve
from parameterized import parameterized
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.models import UserAction
from product.tests.action_base import make_action


class ActionsBuyTests(TestCaseWithLogin):
    def setUp(self) -> None:
        self.action_data = {
            'code': 'bbas3',
            'quantity': '1',
            'unit_price': '10',
        }
        return super().setUp()

    def test_actions_get_request_url_is_correct(self) -> None:
        url = reverse('product:actions_buy')
        self.assertEqual(url, '/ativos/acoes/comprar/')

    def test_actions_get_request_is_redirected_if_user_not_logget_in(self) -> None:  # noqa: E501
        response = self.client.get(
            reverse('product:actions_buy')
        )

        self.assertRedirects(
            response,
            '/?next=/ativos/acoes/comprar/',
            302,
        )

    def test_actions_get_request_status_code_200_if_user_is_logged_in(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # access actions buy with get request
        response = self.client.get(
            reverse('product:actions_buy')
        )

        self.assertEqual(response.status_code, 200)

    def test_actions_uses_correct_view(self) -> None:
        response = resolve(
            reverse('product:actions_buy')
        )
        self.assertIs(response.func.view_class, views.ActionsBuyView)

    def test_actions_loads_correct_template(self) -> None:
        # make_login
        self.make_login()

        # access actions buy with get request
        response = self.client.get(
            reverse('product:actions_buy')
        )
        self.assertTemplateUsed(
            response,
            'product/pages/actions_buy.html'
        )

    def test_actions_loads_correct_content(self) -> None:
        # make_login
        self.make_login()

        # access actions buy with get request
        response = self.client.get(
            reverse('product:actions_buy')
        )

        content = response.content.decode('utf-8')

        self.assertIn('código', content)
        self.assertIn('quantidade', content)
        self.assertIn('valor unitário', content)
        self.assertIn('comprar', content)

    @parameterized.expand([
        ('code', 'Campo obrigatório'),
        ('quantity', 'Campo obrigatório'),
        ('unit_price', 'Campo obrigatório'),
    ])
    def test_actions_buy_returns_error_messages_if_any_field_is_empty(self, field, message) -> None:  # noqa: E501
        # make login
        self.make_login()

        # try buy the action
        response = self.client.post(
            reverse('product:actions_buy'),
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
            reverse('product:actions_buy'),
            self.action_data,
            follow=True
        )

        self.assertIn(
            f'Código {self.action_data["code"].upper()} não encontrado',
            response.content.decode('utf-8'),
            )

    def test_actions_buy_returns_success_messages_if_action_is_purchased_and_create_a_new_user_action(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make new action
        action = make_action('bbas3', 'banco do brasil')

        # set action_data
        self.action_data.update({'action': action})

        # try buy the action
        response = self.client.post(
            reverse('product:actions_buy'),
            self.action_data,
            follow=True
        )

        # Try get new user_action into the databases
        user_action = UserAction.objects.filter(
            user=self.get_user(username='user'),
            action=action,
        )

        # checks if the user_action was saved in the databases
        self.assertTrue(user_action.exists())

        # checks if the success message is displayed
        self.assertIn(
            (
                f'compra de {self.action_data["quantity"]} unidade(s) de '
                f'{self.action_data["code"].upper()} '
                'realizada com sucesso'
            ),
            response.content.decode('utf-8'),
            )

        # checks if the quantity, unit_price and total_price are corrects
        self.assertEqual(user_action.first().quantity, 1)
        self.assertEqual(user_action.first().unit_price, 10)
        self.assertAlmostEqual(user_action.first().get_total_price(), 10)

        # checks if the user was redirected after purchase
        self.assertRedirects(
            response,
            '/ativos/acoes/',
            302,
        )

    def test_actions_buy_update_the_user_action_if_action_existis_into_databases(self) -> None:  # noqa: E501
        """ if user was purchase the same action, is not allowed
            create a new object, this should just update the existing action.
        """
        # make login
        self.make_login()

        # make new action
        action = make_action('bbas3', 'banco do brasil')

        # set action_data for the first time
        self.action_data.update(
            {
                'action': action,
                'quantity': 1,
                'unit_price': 10,
            }
            )

        # buy the action for the first time
        self.client.post(
            reverse('product:actions_buy'),
            self.action_data,
            follow=True
        )

        # Try get new user_action into the databases
        user_action = UserAction.objects.filter(
            user=self.get_user(username='user'),
            action=action,
        )

        # checks if the user_action was saved in the databases
        self.assertTrue(user_action.exists())

        # cheks if quantity and price are corrects
        # the quantity must be 1, and unit_price must be 10
        # the total_price must be 10
        self.assertEqual(user_action.first().quantity, 1)
        self.assertEqual(user_action.first().unit_price, 10)
        self.assertEqual(user_action.first().get_total_price(), 10)

        # set action_data for the second time
        self.action_data.update(
            {
                'action': action,
                'quantity': 10,
                'unit_price': 30,
            }
            )

        # buy the action for the second time
        self.client.post(
            reverse('product:actions_buy'),
            self.action_data,
            follow=True
        )

        # cheks if quantity and price are updated
        # now, the quantity must be 11, and unit_price must be 30
        # the total_price must be 330
        self.assertEqual(user_action.first().quantity, 11)
        self.assertEqual(user_action.first().unit_price, 30)
        self.assertEqual(user_action.first().get_total_price(), 330)
        self.fail('testar todo o FIIs buy. '
                  'refatorar a view de compra de actions e fiis. '
                  'as classes que precisam de login devem herdar da class TestCaseWithLogin. '
                  'modificar a arquitetura dos templates para novas pastas'
                  )
