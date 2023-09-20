from django.urls import reverse, resolve
from utils.mixins.auth import TestCaseWithLogin
from parameterized import parameterized
from datetime import date
from ... import views
from .base_test import make_improvement


class AdminImprovementManagerTests(TestCaseWithLogin):
    url = reverse('admin:improvements_manager', args=(1,))

    def test_improvements_manager_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/painel-de-controle/melhorias/gerenciar/1/',
        )

    def test_improvements_manager_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(response.func.view_class, views.ImprovementMaganer)

    def test_improvements_manager_is_not_allowed_if_the_user_is_not_authenticated(self) -> None:  # noqa: E501
        # make get request without is logged in
        response = self.client.get(self.url)

        self.assertRedirects(
            response,
            '/?next=/painel-de-controle/melhorias/gerenciar/1/',
            302,
        )

    def test_improvements_manager_returns_status_code_404_if_logged_in_user_is_not_a_staff(self) -> None:  # noqa: E501
        # make login with a common user
        self.make_login()

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 404)

    def test_improvements_manager_returns_status_code_200_if_the_user_is_authenticated_and_is_a_staff(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_improvements_manager_user_the_corret_template(self) -> None:
        # make login with a user staff
        self.make_login(is_staff=True)

        # make get request
        response = self.client.get(self.url)

        self.assertTemplateUsed(
            response,
            'administration/pages/improvement_manager.html',
        )

    @parameterized.expand([
        'id',
        'usuário',
        'título',
        'descrição',
        'data',
        'status',
        'última atualização',
        'jhondoe',
        'this is the title',
        'this is the description',
        'enviado',
        'salvar',
        date.today().strftime("%d/%m/%Y"),
    ])
    def test_improvements_manager_loads_the_corret_content(self, text: str) -> None:  # noqa: E501
        # make login with a user staff
        _, user = self.make_login(is_staff=True, username='jhondoe')

        # make the improvement
        make_improvement(
            user=user,
            title='this is the title',
            description='this is the description',
            status='enviado',
        )

        # make get request
        response = self.client.get(self.url)

        self.assertIn(
            text,
            response.content.decode('utf-8'),
        )
