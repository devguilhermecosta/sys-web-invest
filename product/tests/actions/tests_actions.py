from django.urls import reverse, resolve
from product import views
from utils.mixins.auth import TestCaseWithLogin
from product.tests.base_tests import make_user_action
from parameterized import parameterized


class ProductActionsTests(TestCaseWithLogin):
    url = reverse('product:actions')

    def test_actions_url_is_correct(self) -> None:
        self.assertEqual(self.url,
                         '/ativos/acoes/',
                         )

    def test_actions_class_view_is_correct(self) -> None:
        response = resolve(
            self.url
        )
        self.assertEqual(
            response.func.view_class,
            views.ActionsView,
        )

    def test_actions_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        response = self.client.get(
            self.url
        )

        self.assertTemplateUsed(
            response,
            'product/pages/actions/actions.html',
            )

    def test_actions_is_redirected_if_user_not_logged_in(self) -> None:
        response = self.client.get(
            self.url
        )
        self.assertRedirects(
            response,
            '/?next=/ativos/acoes/',
            302,
        )

    def test_actions_status_code_200_if_user_is_logged_in(self) -> None:
        # make login
        self.make_login()

        # access the dashboard actions
        response = self.client.get(
            self.url
        )

        self.assertEqual(response.status_code, 200)

    def test_actions_loads_correct_content(self) -> None:
        # make login
        self.make_login()

        # access the dashboard actions
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn('minhas ações', content)
        self.assertIn('comprar', content)
        self.assertIn('vender', content)
        self.assertIn('gerenciar proventos', content)

    @parameterized.expand([
        'Aplicação total:',
        # 'R$ 2000,00',
        'Total recebido em proventos:',
        'R$ 400,00',
        'Total pago em taxas:',
        'R$ 100,00',
    ])
    def test_actions_loads_correct_summary(self, text: str) -> None:
        '''
            the total application property is dynamically generated
            through the yfinance library, so testing this value is difficult,
            so your test is not included here.
        '''
        # make login
        _, user = self.make_login()

        # create the useraction
        p = make_user_action(user,
                             'bbas3',
                             'banco do brasil',
                             )

        # buy the action
        self.client.post(
            reverse('product:actions_buy'),
            {
                'code': 'bbas3',
                'quantity': 1,
                'unit_price': 2000,
                'date': '2023-07-02',
            },
            follow=True,
        )

        # create a profits history
        profits_data = {
            'userproduct': p.id,
            'handler': 'jscp',
            'date': '2023-07-02',
            'tax_and_irpf': 100,
            'unit_price': 500,
        }

        # make post request
        response = self.client.post(
            reverse('product:actions_manage_profits'),
            profits_data,
            follow=True,
        )

        # access the dashboard actions
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content
        )
