from utils.mixins.auth import TestCaseWithLogin
from django.urls import reverse


class ProductFixedIncomeHistoryTests(TestCaseWithLogin):
    url = reverse('product:fixed_income_history', args=(1,))

    def test_fixed_income_history_url_is_correct(self) -> None:
        self.assertEqual(self.url, '/ativos/renda-fixa/1/historico/')
        self.fail('continuar a partir daqui')
