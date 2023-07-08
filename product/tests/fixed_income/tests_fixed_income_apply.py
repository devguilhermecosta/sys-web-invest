from utils.mixins.auth import TestCaseWithLogin


class FixedIncomeApplyTests(TestCaseWithLogin):
    def fail(self) -> None:
        self.fail(
            'continuar o script js para a confirmação '
            'de aplicação e resgate da renda fixa. '
            'continuar os tests daqui.'
        )
