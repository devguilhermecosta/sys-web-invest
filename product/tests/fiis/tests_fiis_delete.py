from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product import views
from product.tests.base_tests import make_user_fii
from product.models import UserFII


class FIIsDeleteTests(TestCaseWithLogin):
    url = reverse('product:fiis_delete', args=(1,))

    def test_fiis_delete_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/fiis/1/deletar/',
        )

    def test_fiis_delete_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.FiisDeleteView,
        )

    def test_fiis_delete_returns_status_code_404_if_get_request(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_fiis_delete_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make post request without being logged in
        response = self.client.post(self.url)

        self.assertRedirects(
            response,
            '/?next=/ativos/fiis/1/deletar/',
            302,
        )

    def test_fiis_delete_returns_status_code_404_if_the_product_does_not_exists(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make post request without an existing product
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_fiis_delete_returns_status_code_404_if_the_product_belongs_to_antoher_user(self) -> None:  # noqa: E501
        # create the another user
        another_user = self.create_user(username='jhon',
                                        email='jhon@email.com',
                                        )

        # create the userfii
        make_user_fii(another_user, 'mxrf11', 'maxi renda')

        # make login with user
        self.make_login()

        # make post request using another_user's product
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_fiis_delete_remove_the_fii_from_data_base(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the userfii
        make_user_fii(user, 'mxrf11', 'maxi renda')

        # checks if the fii exists
        userfii = UserFII.objects.filter(user=user)
        self.assertEqual(len(userfii), 1)

        # make post request
        self.client.post(self.url)

        # checks again if the fii exists
        userfii = UserFII.objects.filter(user=user)
        self.assertEqual(len(userfii), 0)

    def test_fiis_delete_returns_success_message_if_the_fii_is_deleted(self) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create the userfii
        make_user_fii(user, 'mxrf11', 'maxi renda')

        # make post request
        response = self.client.post(self.url, follow=True)
        content = response.content.decode('utf-8')

        self.assertIn(
            'ativo deletado com sucesso',
            content,
        )
        self.assertRedirects(
            response,
            '/ativos/fiis/lista/',
            302,
        )
