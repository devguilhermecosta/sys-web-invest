from utils.mixins.auth import TestCaseWithLogin


class FIIsHistoryTests(TestCaseWithLogin):
    def test_one(self) -> None:
        self.fail(
            'testar todo o history dos FIIs. '
            'refatorar as views de history em uma única view '
            'para as actions e fiis. '
            'refatorar os templates para um template comum.'
        )
