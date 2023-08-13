from django.urls import resolve, reverse
from parameterized import parameterized

from product import views
from product.models import UserFII
from product.tests.base_tests import (
    make_user_fii,
    create_profits_history,
    )
from utils.mixins.auth import TestCaseWithLogin


class FIIsProfitsTests(TestCaseWithLogin):
    url = reverse('product:fiis_manage_income')

    def test_fiis_profits_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/fiis/gerenciar-proventos/'
        )

    def test_fiis_profits_loads_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FIIManageIncomeReceipt,
        )

    def test_fiis_profits_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/fiis/gerenciar-proventos/',
            302,
        )

    def test_fiis_profits_is_allowed_if_user_is_authenticated(self) -> None:
        self.make_login()
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_fiis_profits_loads_correct_template(self) -> None:
        self.make_login()

        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/pages/fiis/fiis_profits.html'
        )

    @parameterized.expand([
        ('lançar rendimento'),
        ('fii'),
        ('MXRF11'),
        ('data'),
        ('valor'),
        ('salvar'),
        ('Total acumulado em proventos (FIIs):'),
    ])
    def test_fiis_profits_loads_correct_content_when_not_profits(self, text: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # make user fii for populate select input
        make_user_fii(
            user,
            'mxrf11',
            'maxi renda',
        )

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            text,
            content
        )

    def test_fiis_profits_loads_in_the_select_input_only_the_userfiis_of_the_logged_in_user(self) -> None:  # noqa: E501
        # create another user
        another_user = self.create_user(
            username='jhondoe',
            email='jhondoe@email.com',
        )

        # create the user_fii for another_user
        make_user_fii(another_user,
                      'brcr11',
                      'bresco',
                      )

        # checks if the user_fii for another_user exists
        another_user_userfii = UserFII.objects.filter(
            user=another_user,
        )
        self.assertEqual(
            len(another_user_userfii),
            1
        )
        self.assertEqual(
            str(another_user_userfii.first()),
            'brcr11 de jhondoe',
        )

        ######

        # make login with user=user and create a new user_fii
        create_profits_history(self.client,
                               self.make_login,
                               code='mxrf11',
                               desc='maxi renda',
                               )

        # make get request
        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        # checks if the mxrf11 of user is in the select input
        self.assertIn(
            'MXRF11',
            content
        )

        # checks if the brcr11 of another_user is not in the select input
        self.assertNotIn(
            'BRCR11',
            content
        )

    @parameterized.expand([
        ('userproduct', '{"error": "form errors"}'),
        ('date', '{"error": "form errors"}'),
        ('unit_price', '{"error": "form errors"}'),
    ])
    def test_fiis_profits_returns_error_messages_if_any_field_is_empty(self, field: str, msg: str) -> None:  # noqa: E501
        # make login
        self.make_login()

        # data
        data = {
            field: '',
        }

        # make post request
        response = self.client.post(
            self.url,
            data=data,
            follow=True,
        )

        self.assertIn(
            msg,
            response.content.decode('utf-8')
        )

    def test_fiis_profits_returns_success_json_response_if_all_fields_is_ok(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # make the user fii
        user_fii = make_user_fii(
            user=user,
            code='mxrf11',
            desc='maxi renda',
        )

        # data
        data = {
            'userproduct': user_fii.pk,
            'date': '2023-07-02',
            'unit_price': 4.96,
        }

        # make post request
        response = self.client.post(
            self.url,
            data=data,
        )

        self.assertIn(
            '{"data": "success request"}',
            response.content.decode('utf-8')
        )

    def test_fiis_profits_create_a_new_history(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # make the user fii
        user_fii = make_user_fii(
            user=user,
            code='mxrf11',
            desc='maxi renda',
        )

        # data
        data = {
            'userproduct': user_fii.pk,
            'date': '2023-07-02',
            'unit_price': 4.96,
        }

        # make post request
        self.client.post(
            self.url,
            data=data,
        )

        # get user_fii
        u_fii = UserFII.objects.get(pk=1)

        # get_history
        history = u_fii.get_partial_history('profits')[0]

        self.assertEqual(history.handler, 'profits')
        self.assertEqual(str(history.date), '2023-07-02')
        self.assertEqual(float(history.get_final_value()), 4.96)
