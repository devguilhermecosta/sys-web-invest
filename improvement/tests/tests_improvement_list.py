from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from .. import views
from .base_test import make_improvement
from ..models import Improvement
from parameterized import parameterized
from datetime import date


class ImprovementListTests(TestCaseWithLogin):
    url = reverse('improvement:list')

    def test_improvement_list_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/melhorias/minha-lista/',
        )

    def test_improvement_list_uses_the_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            views.ImprovementList,
        )

    def test_improvement_list_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without is logged in
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/?next=/melhorias/minha-lista/',
            302,
        )

    def test_improvement_list_returns_status_code_200_if_the_user_is_authenticated(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_improvement_list_post_request_is_not_allowed(self) -> None:
        # make login
        self.make_login()

        # tries make post request
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 405)

    def test_improvement_list_returns_default_message_if_the_user_has_no_requests(self) -> None:  # noqa: E501
        # make login
        self.make_login()

        # make get request
        response = self.client.get(self.url)

        self.assertIn(
            'nenhuma solicitação até o momento.',
            response.content.decode('utf-8'),
        )

    @parameterized.expand([
        ('id'),
        ('abertura'),
        ('título'),
        ('status'),
        ('atualizado em'),
        ('1'),
        (str(date.today().strftime('%d/%m/%Y'))),
        ('my subject'),
        ('my content'),
        ('enviado'),
        ('id'),
    ])
    def test_improvement_list_loads_the_user_requests(self, content: str) -> None:  # noqa: E501
        # make login
        _, user = self.make_login()

        # create a Improvement object
        make_improvement(user, 'my subject', 'my content')

        # make get request
        response = self.client.get(self.url)

        # get the Improvement context
        improvements = response.context['improvements']

        self.assertIn(
            content,
            response.content.decode('utf-8'),
        )
        self.assertNotIn(
            'nenhuma solicitação até o momento.',
            response.content.decode('utf-8'),
        )
        self.assertEqual(len(improvements), 1)

    def test_improvement_list_loads_only_the_requests_own_to_logged_in_user(self) -> None:  # noqa: E501
        # make login with user
        _, user = self.make_login()

        # create a new user
        new_user = self.create_user(username='jhon', email='jhon@email.com')

        # create a Improvement object to user
        make_improvement(user, 'my subject', 'my content')

        # create a Improvement object to new_user
        make_improvement(new_user, 'new_user subject', 'new_user content')

        # make get request
        response = self.client.get(self.url)

        # get the Improvement context
        improvements = response.context['improvements']

        # get the Improvement all objects
        all_improvements = Improvement.objects.all()

        # the all_improvements must be 2
        self.assertEqual(len(all_improvements), 2)

        # the improvements context length must be 1
        self.assertEqual(len(improvements), 1)

        # the subject of logged in user is renderized
        self.assertIn(
            'my subject',
            response.content.decode('utf-8')
        )

        # the subject of new_user is not renderized
        self.assertNotIn(
            'new_user subject',
            response.content.decode('utf-8')
        )
