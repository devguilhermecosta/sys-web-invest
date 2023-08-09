from product.models import DirectTreasure, DirectTreasureHistory
from product.views.base_views.fixed_income import (
    FixedIncomeBaseView,
    Register,
    Update,
    Delete,
    Details,
    Apply,
    Redeem,
    ReceiveProfits,
    )
from product.views.base_views.fixed_income.history import (
    History,
    HistoryUpdate,
    HistoryDelete,
)
from product.forms.direct_treasure import (
    DirectTreasureRegisterForm,
    DirectTreasureEditForm,
    DirectTreasureHistoryForm,
    )


class DirectTreasureView(FixedIncomeBaseView):
    model = DirectTreasure
    template_title = 'tesouro direto'
    template_path = 'product/partials/_dt_and_fi_intro.html'
    reverse_url_register = 'product:direct_treasure_register'
    reverse_url_back_to_page = 'dashboard:user_dashboard'


class DirectTreasureRegisterView(Register):
    model = DirectTreasure
    form = DirectTreasureRegisterForm
    template_path = 'product/partials/_dt_and_fi_register.html'
    reverse_url_back_to_page = 'product:direct_treasure'
    reverse_url_if_form_invalid = 'product:direct_treasure_register'


class DirectTreasureEditView(Update):
    model = DirectTreasure
    form = DirectTreasureEditForm
    template_path = 'product/partials/_dt_and_fi_edit.html'
    reverse_url_if_form_invalid = 'product:direct_treasure_edit'


class DirectTreasureDeleteView(Delete):
    model = DirectTreasure
    reverse_url_redirect = 'product:direct_treasure'


class DirectTreasureDetailsView(Details):
    model = DirectTreasure
    template_path = 'product/partials/_dt_and_fi_details.html'
    reverse_url_back_to_page = 'product:direct_treasure'
    reverse_url_edit = 'product:direct_treasure_edit'
    reverse_url_history = 'product:direct_treasure_history'
    reverse_url_delete = 'product:direct_treasure_delete'
    reverse_url_profits = 'product:direct_treasure_profits_receipt'
    reverse_url_apply = 'product:direct_treasure_apply'
    reverse_url_redeem = 'product:direct_treasure_redeem'


class DirectTreasureApplyView(Apply):
    model = DirectTreasure


class DirectTreasureRedeemView(Redeem):
    model = DirectTreasure


class DirectTreasureProfitsReceiptView(ReceiveProfits):
    model = DirectTreasure
    template_path = 'product/partials/_dt_and_fi_profits_receipt.html'
    reverse_url_if_form_invalid = 'product:direct_treasure_profits_receipt'


class DirectTreasureHistoryView(History):
    model = DirectTreasure
    history_model = DirectTreasureHistory
    template_path = 'product/partials/_history_dt_and_fi.html'
    direct_treasure = True


class DirectTreasureHistoryEditView(HistoryUpdate):
    model = DirectTreasure
    history_model = DirectTreasureHistory
    history_form = DirectTreasureHistoryForm
    template_path = 'product/partials/_dt_and_fi_history_edit.html'


class DirectTreasureHistoryDeleteView(HistoryDelete):
    model = DirectTreasure
    history_model = DirectTreasureHistory
