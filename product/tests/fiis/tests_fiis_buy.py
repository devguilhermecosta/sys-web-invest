from utils.mixins.auth import TestCaseWithLogin


class FIIsBuyTests(TestCaseWithLogin):
    def test_fail(self) -> None:
        self.fail('continuar daqui e criar o history')
