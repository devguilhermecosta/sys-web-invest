from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from administration import views
from product.models import FII
from product.tests.base_tests import make_fii
from unittest.mock import patch


class FIIsAutoRegisterTests(TestCaseWithLogin):
    url = reverse('admin:fii_auto_register')

    def test_fiis_auto_register_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/painel-de-controle/cadastrar/auto/fiis/',
        )

    def test_fiis_auto_register_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FIIAutoRegister,
        )

    def test_fiis_auto_register_returns_status_code_404_if_get_request(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_fiis_auto_register_returns_status_code_302_if_the_user_is_not_logged_in(self) -> None:  # noqa: E501
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/?next=/painel-de-controle/cadastrar/auto/fiis/',
            302,
        )

    def test_fiis_auto_register_returns_status_code_404_if_the_user_logged_in_is_not_staff(self) -> None:  # noqa: E501
        self.make_login(is_staff=False)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_fiis_auto_register_returns_status_code_200_if_the_user_logged_in_is_staff(self) -> None:  # noqa: E501
        self.make_login(is_staff=True)
        response = self.client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_fiis_auto_register_creates_several_new_objects(self) -> None:
        # checks the fii length before the update
        all_fiis = FII.objects.all()
        self.assertEqual(len(all_fiis), 0)

        # update the data base
        self.make_login(is_staff=True)
        self.client.post(self.url, follow=True)

        # checks again the fii length
        all_fiis = FII.objects.all()
        self.assertTrue(len(all_fiis) > 100)

    def test_fiis_auto_register_does_not_register_the_same_registered_fii(self) -> None:  # noqa: E501
        # create a new fii
        make_fii('mxrf11', 'maxi renda')

        # checks if the mxrf11 exists and checks this length
        fii = FII.objects.filter(code='mxrf11')
        self.assertTrue(fii.exists())
        self.assertEqual(len(fii), 1)

        # update the data base
        self.make_login(is_staff=True)
        self.client.post(self.url, follow=True)

        # checks again if the mxrf11 exists and checks this length.
        # the length property must be one.
        fii = FII.objects.filter(code='mxrf11')
        self.assertTrue(fii.exists())
        self.assertEqual(len(fii), 1)

    def test_fiis_auto_register_does_not_register_the_actions(self) -> None:  # noqa: E501
        # update the data base
        self.make_login(is_staff=True)
        self.client.post(self.url, follow=True)

        # checks if the bbas3 and vale3 exists from FII DB.
        # the BBAS3 and VALE3 are a Action.
        query_1 = FII.objects.filter(code='bbas3')
        query_2 = FII.objects.filter(code='vale3')
        self.assertFalse(query_1.exists())
        self.assertFalse(query_2.exists())

        # checks if the MXRF11 exists from FII DB
        # the MXRF11 must be exists because this is a FII
        query_3 = FII.objects.filter(code='mxrf11')
        self.assertTrue(query_3.exists())

    def test_fiis_auto_register_returns_success_message_if_ok(self) -> None:  # noqa: E501
        # update the data base
        self.make_login(is_staff=True)
        response = self.client.post(self.url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn(
            'fiis registrados com sucesso',
            content,
        )

    def test_fiis_auto_register_returns_error_message_if_any_error_occurs(self) -> None:  # noqa: E501
        # create an incorrect url to make request
        new_url = 'https://brapi.dev/api/quote/list/my_error'

        with patch('administration.views.products.base_view.auto_register.AutoRegister.resp',  # noqa: E501
                   new=new_url):

            # tries update the data base
            self.make_login(is_staff=True)
            response = self.client.post(self.url, follow=True)
            content = response.content.decode('utf-8')

            self.assertIn(
                'Erro ao atualizar a lista de ativos.',
                content,
            )
            self.assertRedirects(
                response,
                '/painel-de-controle/cadastrar/fii/',
                302,
            )
