from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from product.views import AllFIIsView
from product.models import FII
from parameterized import parameterized
from ..base_tests import make_fii


class FiisListTests(TestCaseWithLogin):
    url = reverse('product:fiis_list')

    def test_fiis_list_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/fiis/lista/')

    def test_fiis_list_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertEqual(response.func.view_class, AllFIIsView)

    def test_fiis_list_get_request_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/?next=/ativos/fiis/lista/',
            302,
        )

    def test_fiis_list_returns_status_code_404_if_not_get_request(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)

    def test_fiis_list_returns_status_code_200_if_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_fiis_list_loads_correct_template(self) -> None:
        # make login
        self.make_login()

        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'product/pages/fiis/fiis_list.html',
        )

    def test_fiis_list_loads_no_fii_so_far_if_user_has_not_fiis(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertIn(
            'nenhum fii até o momento',
            content,
        )

    @parameterized.expand([
        ('FIIs em carteira'),
        ('mxrf11'),
        ('R$ 9,50'),
    ])
    def test_fiis_list_loads_correct_content_if_user_has_fiis(self, text) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make fii
        make_fii('mxrf11', 'maxi renda')

        # buy fii
        self.client.post(
            reverse('product:fiis_buy'),
            {
                'code': 'mxrf11',
                'quantity': 10,
                'unit_price': 9.50,
                'date': '2023-06-29',
            },
            follow=True,
        )

        response = self.client.get(self.url)
        content = response.content.decode('utf-8')

        self.assertEqual(
            len(FII.objects.all()),
            1,
        )
        self.assertIn(
            text,
            content,
        )

    def test_fiis_list_render_only_authenticated_user_fiis(self) -> None:
        '''
            this test verifies that the authenticated user's fiis
            are not loaded in another user.
        '''
        # create the action
        make_fii('mxrf11', 'maxi renda')

        # make login with username 'user'
        self.make_login()

        # buy mxrf11 fii
        response_fiis_buy = self.client.post(
            reverse('product:fiis_buy'),
            {
                'code': 'mxrf11',
                'quantity': 10,
                'unit_price': 9.50,
                'date': '2023-06-29',
            },
            follow=True,
        )

        # check if the fii has been purchased
        self.assertIn(
            'compra de 10 unidade(s) de MXRF11 realizada com sucesso',
            response_fiis_buy.content.decode('utf-8')
            )

        # get request to fiis_list url
        response_fiis_list = self.client.get(self.url)
        content = response_fiis_list.content.decode('utf-8')

        # check if the fii MXRF11 is in the fiis list
        self.assertIn(
            'mxrf11',
            content,
        )

        # make logout with 'user'
        self.client.logout()

        # create the new user with username 'user_2'
        self.create_user(
            with_profile=True,
            username='user_2',
            email='user_2@email.com'
            )

        # make login with user_2
        self.make_login(create_user=False, username='user_2')

        # access fiis list
        response_fiis_list_user_2 = self.client.get(self.url)
        content_user_2 = response_fiis_list_user_2.content.decode('utf-8')

        # checks if the fiis list is empty
        self.assertIn(
            'nenhum fii até o momento',
            content_user_2,
            )
        self.assertNotIn(
            'mxrf11',
            content_user_2,
        )
