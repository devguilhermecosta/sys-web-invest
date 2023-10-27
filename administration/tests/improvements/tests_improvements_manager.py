from datetime import date

from django.urls import resolve, reverse
from parameterized import parameterized

from utils.mixins.auth import TestCaseWithLogin

from ... import views
from .base_test import make_improvement
from improvement.models import Improvement


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
        _, user = self.make_login(is_staff=True)

        # make the improvement
        make_improvement(
            user=user,
            title='this is the title',
            description='this is the description',
            status='enviado',
        )

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
        'enviado',  # status option
        'em análise',  # status option
        'em desenvolvimento',  # status option
        'recusado',  # status option
        'concluído',  # status option
        'salvar',
        date.today().strftime("%d/%m/%Y"),
        '/painel-de-controle/melhorias/lista/',  # url back to page
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

    #  BEGGINNING OF THE POST REQUEST

    def test_improvements_manager_post_request_is_not_allowed_if_the_user_is_not_logged_in(self) -> None:  # noqa: E501
        # make post request without is logged in
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            '/?next=/painel-de-controle/melhorias/gerenciar/1/',
            302,
        )

    def test_improvements_manager_post_request_returns_status_code_404_if_the_user_is_not_a_staff(self) -> None:  # noqa: E501
        # make login with a common user
        self.make_login(is_staff=False)

        # make post request
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_improvements_manager_returns_error_message_if_the_improvement_does_not_exists(self) -> None:  # noqa: E501
        # make login with a user staff
        self.make_login(is_staff=True)

        # make post request without a existing improvement
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 404)

    def test_improvements_manager_returns_error_message_if_the_status_field_is_empty(self) -> None:  # noqa: E501
        # make login with a user staff
        _, user = self.make_login(is_staff=True)

        # make a improvement
        make_improvement(
            user=user,
            title='this is the title',
            description='this is the description',
            status='enviado',
        )

        # make post request with empty status field
        response = self.client.post(self.url, data={'status': ''}, follow=True)

        self.assertIn(
            'campo obrigatório',
            response.content.decode('utf-8'),
        )
        self.assertRedirects(
            response,
            '/painel-de-controle/melhorias/gerenciar/1/',
            302,
        )

    def test_improvements_manager_returns_success_message_if_the_status_field_is_ok(self) -> None:  # noqa: E501
        # make login with a user staff
        _, user = self.make_login(is_staff=True)

        # make a improvement
        make_improvement(
            user=user,
            title='this is the title',
            description='this is the description',
            status='enviado',
        )

        # make post request
        response = self.client.post(
            self.url,
            data={'status': 'em desenvolvimento'},
            follow=True,
        )

        self.assertIn(
            'alteração salva com sucesso',
            response.content.decode('utf-8'),
        )
        self.assertRedirects(
            response,
            '/painel-de-controle/melhorias/gerenciar/1/',
            302,
        )

    def test_improvements_manager_changes_the_status_field(self) -> None:  # noqa: E501
        # make login with a user staff
        _, user = self.make_login(is_staff=True)

        # make a improvement
        make_improvement(
            user=user,
            title='this is the title',
            description='this is the description',
            status='enviado',
        )

        # checks the status before modification
        imp = Improvement.objects.first()
        self.assertEqual(imp.status, 'enviado')

        # make post request
        self.client.post(
            self.url,
            data={'status': 'em desenvolvimento'},
            follow=True,
        )

        # checks the status after modification
        imp = Improvement.objects.first()
        self.assertEqual(imp.status, 'em desenvolvimento')
