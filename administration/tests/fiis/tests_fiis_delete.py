from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product.models import FII
from product.tests.base_tests import make_fii, make_user_fii
from administration import views


class FIIsDeleteTests(TestCaseWithLogin):
    url = reverse('admin:fii_delete', args=('mxrf11',))

    def test_fiis_delete_urls_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/painel-de-controle/cadastrar/fii/mxrf11/deletar/',
        )

    def test_fiis_delete_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FIIDelete,
        )

    def test_fiis_delete_is_not_allowed_if_the_user_is_not_logged_in(self) -> None:  # noqa: E501
        # make post request without is logged in
        response = self.client.post(self.url, follow=True)

        self.assertRedirects(
            response,
            '/?next=/painel-de-controle/cadastrar/fii/mxrf11/deletar/',
            302,
        )

    def test_fiis_delete_is_not_allowed_if_the_user_is_logged_in_but_is_not_a_staff(self) -> None:  # noqa: E501
        ''' the user is redirected to dashboard '''
        # make login with a common user
        self.make_login()

        # create the fii
        make_fii('mxrf11', 'maxi renda')

        # make post request
        response = self.client.post(self.url, follow=True)

        self.assertRedirects(
            response,
            '/dashboard/painel-do-usuario/',
            302,
        )

    def test_fiis_delete_returns_status_code_404_with_a_common_logged_in_user_if_get_request(self) -> None:  # noqa: E501
        # make login with a common user
        self.make_login()

        # create the fii
        make_fii('mxrf11', 'maxi renda')

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_fiis_delete_returns_status_code_404_with_a_staff_logged_in_user_if_get_request(self) -> None:  # noqa: E501
        # make login with a staff user
        self.make_login(is_staff=True)

        # create the fii
        make_fii('mxrf11', 'maxi renda')

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_fiis_delete_returns_status_code_404_if_the_fii_does_not_exists(self) -> None:  # noqa: E501
        # make login with a staff user
        self.make_login(is_staff=True)

        # make post request without an existing fii
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_fiis_delete_returns_error_message_if_the_fii_is_used_by_any_user(self) -> None:  # noqa: E501
        # make login with a staff user
        _, user = self.make_login(is_staff=True)

        # create the fii and user_fii
        make_user_fii(user, 'mxrf11', 'maxi renda')

        # make post request
        response = self.client.post(self.url, follow=True)

        self.assertIn(
            'Este ativo não pode ser deletado, '
            'pois está em uso por algum usuário.',
            response.content.decode('utf-8')
        )
        self.assertRedirects(
            response,
            '/painel-de-controle/cadastrar/fii/',
            302,
        )

    def test_fiis_delete_returns_success_message_if_the_fii_is_deleted(self) -> None:  # noqa: E501
        # make login with a staff user
        self.make_login(is_staff=True)

        # created the fii
        make_fii('mxrf11', 'maxi renda')

        # make post request
        response = self.client.post(self.url, follow=True)

        self.assertIn(
            'ativo deletado com sucesso',
            response.content.decode('utf-8')
        )
        self.assertRedirects(
            response,
            '/painel-de-controle/cadastrar/fii/',
            302,
        )

    def test_fiis_delete_remove_the_fii_from_db_if_the_fii_is_deleted(self) -> None:  # noqa: E501
        # make login with a staff user
        self.make_login(is_staff=True)

        # created the fii
        make_fii('mxrf11', 'maxi renda')

        # checks if the fii exists
        fiis = FII.objects.filter(code='mxrf11')
        self.assertEqual(len(fiis), 1)

        # make post request
        self.client.post(self.url, follow=True)

        # checks again if the fii exists
        # the length must be zero
        fiis = FII.objects.filter(code='mxrf11')
        self.assertEqual(len(fiis), 0)
