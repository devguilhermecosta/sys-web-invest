from utils.mixins.auth import TestCaseWithLogin


class DirectTreasureRedeemTests(TestCaseWithLogin):
    def test_fail(self):
        self.fail('continuar daqui')
