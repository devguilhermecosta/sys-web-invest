from product.models import ProductFixedIncome, FixedIncomeHistory
from product.forms.fixed_income import (
    FixedIncomeRegisterForm,
    FixedIncomeEditForm,
    FixedIncomeHistoryEditForm,
)
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


class FixedIncomeView(FixedIncomeBaseView):
    model = ProductFixedIncome
    template_title = 'renda fixa'
    template_path = 'product/partials/_dt_and_fi_intro.html'
    reverse_url_register = 'product:fixed_income_register'
    reverse_url_back_to_page = 'dashboard:user_dashboard'


class FixedIncomeRegisterView(Register):
    model = ProductFixedIncome
    form = FixedIncomeRegisterForm
    template_path = 'product/partials/_dt_and_fi_register.html'
    reverse_url_back_to_page = 'product:fixed_income'
    reverse_url_if_form_invalid = 'product:fixed_income_register'


class FixedIncomeEditView(Update):
    model = ProductFixedIncome
    form = FixedIncomeEditForm
    template_path = 'product/partials/_dt_and_fi_edit.html'
    reverse_url_if_form_invalid = 'product:fixed_income_edit'


class FixedIncomeDeleteView(Delete):
    model = ProductFixedIncome
    reverse_url_redirect = 'product:fixed_income'


class FixedIncomeDetailsView(Details):
    model = ProductFixedIncome
    template_path = 'product/partials/_dt_and_fi_details.html'
    reverse_url_back_to_page = 'product:fixed_income'
    reverse_url_edit = 'product:fixed_income_edit'
    reverse_url_history = 'product:fixed_income_history'
    reverse_url_delete = 'product:fixed_income_delete'
    reverse_url_profits = 'product:fixed_income_profits_receipt'
    reverse_url_apply = 'product:fixed_income_apply'
    reverse_url_redeem = 'product:fixed_income_redeem'


class FixedIncomeApplyView(Apply):
    model = ProductFixedIncome


class FixedIncomeRedeemView(Redeem):
    model = ProductFixedIncome


class FixedIncomeProfitsReceiptView(ReceiveProfits):
    model = ProductFixedIncome
    template_path = 'product/partials/_dt_and_fi_profits_receipt.html'
    reverse_url_if_form_invalid = 'product:fixed_income_profits_receipt'


class FixedIncomeHistoryView(History):
    model = ProductFixedIncome
    history_model = FixedIncomeHistory
    template_path = 'product/partials/_history_dt_and_fi.html'
    fixed_income = True


class FixedIncomeHistoryEditView(HistoryUpdate):
    model = ProductFixedIncome
    history_model = FixedIncomeHistory
    history_form = FixedIncomeHistoryEditForm
    template_path = 'product/partials/_dt_and_fi_history_edit.html'


class FixedIncomeHistoryDeleteView(HistoryDelete):
    model = ProductFixedIncome
    history_model = FixedIncomeHistory
