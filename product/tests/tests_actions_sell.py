from utils.mixins.auth import TestCaseWithLogin
from django.urls import reverse, resolve
from product import views
from product.models import UserAction
from .action_base import make_action
from parameterized import parameterized
from datetime import date


class ActionsSellTests(TestCaseWithLogin):
    url = reverse('product:actions_sell')

    def test_actions_sell_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/acoes/vender/')

    def test_actions_sell_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertEqual(response.func.view_class, views.ActionsSellView)

    def test_actions_sell_get_request_is_allowed_if_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_actions_sell_get_request_loads_correct_template(self) -> None:
        # make_login
        self.make_login()

        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'product/pages/actions/actions_sell.html',
            )

    def test_actions_sell_redirects_to_login_page_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/acoes/vender/',
            302,
        )

    @parameterized.expand([
        ('código'),
        ('quantidade'),
        ('vender'),
    ])
    def test_actions_sell_load_correct_content(self, content) -> None:
        # make login
        self.make_login()

        response = self.client.get(self.url)

        self.assertIn(
            content,
            response.content.decode('utf-8'),
        )

    def test_actions_sell_is_not_allowed_if_quantity_of_action_is_less_then_or_iqual_0(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make new action
        make_action('bbas3', 'banco do brasil')

        # try buy the action
        response_buy = self.client.post(
            reverse('product:actions_buy'),
            {
                'code': 'bbas3',
                'quantity': '5',
                'unit_price': 10,
                'date': date.today().strftime('%Y-%m-%d'),
                },
            follow=True
        )
        content_r_buy = response_buy.content.decode('utf-8')

        # checks if the success message is displayed
        self.assertIn(
            (
                'compra de 5 unidade(s) de '
                'BBAS3 realizada com sucesso'
            ),
            content_r_buy,
            )

        # I has buy 5 units of BBAS3.
        # I will try to sell 10 units.
        response_sell = self.client.post(
            self.url,
            {
                'code': 'bbas3',
                'quantity': 10,
                'unit_price': 10,
                'date': date.today().strftime('%Y-%m-%d'),
            },
            follow=True,
        )
        content_r_sell = response_sell.content.decode('utf-8')
        self.assertIn(
            'Quantidade insuficiente para venda',
            content_r_sell,
        )

    def test_actions_sell_is_allowed_if_the_user_has_the_action_and_quantity_is_biger_then_zero(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # make new action
        action = make_action('bbas3', 'banco do brasil')

        # try buy the action
        self.client.post(
            reverse('product:actions_buy'),
            {
                'code': 'bbas3',
                'quantity': 5,
                'unit_price': '10',
                'date': date.today().strftime('%Y-%m-%d'),
                },
            follow=True
        )

        # Try sell 5 units of bbas3
        response = self.client.post(
            self.url,
            {
                'code': 'bbas3',
                'quantity': 5,
                'unit_price': '10',
                'date': date.today().strftime('%Y-%m-%d'),
            },
            follow=True,
        )

        self.assertIn(
            'venda de 5 unidade(s) de BBAS3 realizada com sucesso',
            response.content.decode('utf-8'),
        )

        # checks if the action's quantity has decreased
        response_after_sale = self.client.get(
            reverse('product:actions_list')
        )
        self.assertIn(
            'bbas3',
            response_after_sale.content.decode('utf-8'),
        )
        self.assertIn(
            'R$ 0',
            response_after_sale.content.decode('utf-8'),
        )
        # the quantity should be zero
        self.assertEqual(
            UserAction.objects.filter(user=user,
                                      action=action,
                                      ).first().quantity,
            0,
        )
