from utils.mixins.auth import TestCaseWithLogin
from django.urls import reverse, resolve
from product.views import DirectTreasureRegisterView


class DirectTreasureRegisterTests(TestCaseWithLogin):
    url = reverse('product:direct_treasure_register')

    def test_direct_treasure_register_url_is_correct(self) -> None:
        self.assertEqual(
            self.url,
            '/ativos/tesouro-direto/registrar/',
        )

    def test_direct_treasure_register_uses_correct_view(self) -> None:
        response = resolve(self.url)
        self.assertIs(
            response.func.view_class,
            DirectTreasureRegisterView,
        )

    def test_direct_treasure_register_is_not_allowed_if_user_is_not_authenticated(self) -> None:  # noqa: E501
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            '/?next=/ativos/tesouro-direto/registrar/',
            302,
        )

    def test_direct_treasure_register_is_allowed_if_user_is_authenticated(self) -> None:  # noqa: E501
        self.make_login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_direct_treasure_register_loads_correct_template(self) -> None:
        self.make_login()
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response,
            'product/pages/direct_treasure/register.html',
        )

    def test_direct_treasure_register_loads_correct_content(self) -> None:
        self.fail('continuar daqui. Criar o formulário de registro.')
