from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from parameterized import parameterized
from datetime import date
from ... import views
from ... tests.improvements.base_test import (
    make_improvement,
    make_improvements_in_batch,
    )


class AdminImprovementsTests(TestCaseWithLogin):
    url = reverse('admin:improvements_list')

    def test_improvements_list_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/painel-de-controle/melhorias/lista/')

    def test_improvements_list_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(response.func.view_class, views.ImprovementsList)

    def test_improvements_list_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without the user is logged in
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/?next=/painel-de-controle/melhorias/lista/',
            302,
        )

    def test_improvement_list_is_not_allowed_if_the_logged_in_user_is_not_a_staff(self) -> None:  # noqa: E501
        # make login with a common user
        self.make_login(is_staff=False)

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_improvement_list_returns_status_code_200_if_the_user_is_authenticated_and_the_user_is_staff(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_improvement_list_uses_correct_template(self) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'administration/pages/improvements_list.html',
        )

    @parameterized.expand([
        '/dashboard/painel-do-usuario/',  # url back to page
        'sugestões e reclamações',
        'id',
        'usuário',
        'data',
        'título',
        'status',
        'última movimentação',
        '1',
        'jhondoe',
        date.today().strftime("%d/%m/%Y"),
        'i have a suggestion',
        'enviado',
        date.today().strftime("%d/%m/%Y"),
    ])
    def test_improvements_list_loads_correct_content(self, text: str) -> None:
        # make login with a user staff
        _, user = self.make_login(is_staff=True, username="jhondoe")

        # make the improvement
        make_improvement(
            user=user,
            title='i have a suggestion',
            description='this is the description',
            status='enviado',
            )

        # make get request
        response = self.client.get(self.url)

        self.assertIn(
            text,
            response.content.decode('utf-8'),
        )

    def test_improvements_list_loads_all_improvement_objects(self) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # make several improvements
        make_improvements_in_batch(10)

        # make get request
        response = self.client.get(self.url)
        improvements = response.context['improvements']

        self.assertEqual(len(improvements), 10)
