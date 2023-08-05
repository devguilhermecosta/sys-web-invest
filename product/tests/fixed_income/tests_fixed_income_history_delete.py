from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.tests.base_tests import make_fixed_income_product
from product.models import FixedIncomeHistory


class FixedInomeHistoryDeleteTests(TestCaseWithLogin):
    url = reverse(
        'product:fixed_income_history_delete',
        kwargs={
            'history_id': 1,
            'product_id': 1,
            }
        )

    def test_fixed_income_history_delete_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/renda-fixa/1/historico/1/deletar/'
        )

    def test_fixed_income_history_delete_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertEqual(
            response.func.view_class,
            views.FixedIncomeHistoryDeleteView,
        )

    def test_fixed_income_history_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/renda-fixa/1/historico/1/deletar/',
            302,
        )

    def test_fixed_income_history_delete_returns_status_404_if_get_request(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create an product and create a history apply
        make_fixed_income_product(user=user, value=10)

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_fixed_income_history_delete_the_history_if_the_user_is_logged_in(self) -> None:  # noqa: E501
        '''
            The history must belong to the logged in user.
            The history must belong to the current product.
            Instead, http404() will be returned.
        '''
        # make login
        _, user = self.make_login()

        # create an product and create a history apply
        product = make_fixed_income_product(user=user, value=10)

        # checks if the history exists
        history = FixedIncomeHistory.objects.filter(
            product=product,
        )
        self.assertEqual(len(history), 1)
        self.assertEqual(history.first().get_final_value(), 10)

        # make post request
        self.client.post(self.url)

        # checks again if the history exists
        history = FixedIncomeHistory.objects.filter(
            product=product,
        )
        self.assertEqual(len(history), 0)

    def test_fixed_income_history_delete_returns_success_message_if_the_history_is_successfully_deleted(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create an product and create a history apply
        make_fixed_income_product(user=user, value=10)

        # make post request
        response = self.client.post(self.url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn(
            'histórico deletado com sucesso',
            content
        )
        self.assertRedirects(
            response,
            reverse('product:fixed_income_history', args=(1,)),
            302,
        )
