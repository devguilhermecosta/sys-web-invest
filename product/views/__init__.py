# flake8: noqa

from .actions import (
    ActionsBuyView,
    ActionsSellView,
    ActionsView,
    AllActionsView,
    ActionHistoryDetails,
    ActionsManageProfitsView,
    ActionsGetTotalProfitsView,
    ActionsManageProfitsHistoryView,
    ActionsManageProfitsHistoryEditView,
    ActionsManageProfitsHistoryDeleteView,
    )
from .fiis import (
    FIIsView,
    FIISBuyView,
    AllFIIsView,
    FIIsSellView,
    FIIManageIncomeReceipt,
    FIIHistoryDetails,
    FIIManageIncomeReceiptHistory,
    FIIManageIncomeReceiptEditHistory,
    FIIManageIncomeReceiptDeleteHistory,
    GetTotalProfitsView,
    )
from .fixed_income import (
    FixedIncomeView,
    FixedIncomeRegisterView,
    FixedIncomeEditView,
    FixedIncomeDeleteView,
    FixedIncomeDetailsView,
    FixedIncomeApplyView,
    FixedIncomeRedeemView,
    FixedIncomeHistoryView,
    FixedIncomeHistoryEditView,
    FixedIncomeHistoryDeleteView,
    FixedIncomeProfitsReceiptView,
    )
from .direct_treasure import (
    DirectTreasureView,
    DirectTreasureRegisterView,
    DirectTreasureEditView,
    DirectTreasureDetailsView,
    DirectTreasureApplyView,
    DirectTreasureRedeemView,
    DirectTreasureHistoryView,
    DirectTreasureHistoryEditView,
)
