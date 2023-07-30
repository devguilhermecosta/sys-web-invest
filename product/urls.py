from django.urls import path
from . import views


app_name: str = 'product'


urlpatterns = [
    path('acoes/',
         views.ActionsView.as_view(),
         name='actions',
         ),
    path('acoes/lista/',
         views.AllActionsView.as_view(),
         name='actions_list',
         ),
    path('acoes/comprar/',
         views.ActionsBuyView.as_view(),
         name='actions_buy',
         ),
    path('acoes/vender/',
         views.ActionsSellView.as_view(),
         name='actions_sell',
         ),
    path('acoes/gerenciar-proventos/',
         views.ActionsManageIncomeView.as_view(),
         name='actions_manage_income',
         ),
    path('acoes/<str:code>/',
         views.ActionHistoryDetails.as_view(),
         name='action_history',
         ),
    path('fiis/',
         views.FIIsView.as_view(),
         name='fiis',
         ),
    path('fiis/lista/',
         views.AllFIIsView.as_view(),
         name='fiis_list'),
    path('fiis/comprar/',
         views.FIISBuyView.as_view(),
         name='fiis_buy',
         ),
    path('fiis/vender/',
         views.FIIsSellView.as_view(),
         name='fiis_sell',
         ),
    path('fiis/gerenciar-proventos/',
         views.FIIManageIncomeReceipt.as_view(),
         name='fiis_manage_income',
         ),
    path('fiis/<str:code>/',
         views.FIIHistoryDetails.as_view(),
         name='fii_history',
         ),
    path('fiis/gerenciar-proventos/historico/json/',
         views.FIIManageIncomeReceiptHistory.as_view(),
         name='fii_history_json',
         ),
    path('fiis/gerenciar-proventos/total-recebido/json/',
         views.GetTotalProfitsView.as_view(),
         name='fii_total_profits_json',
         ),
    path('fiis/gerenciar-proventos/receber/',
         views.FIIManageIncomeReceipt.as_view(),
         name='fiis_manage_income_receipt',
         ),
    path('fiis/gerenciar-proventos/historico/<int:id>/editar/',
         views.FIIManageIncomeReceiptEditHistory.as_view(),
         name='fii_manage_income_receipt_edit',
         ),
    path('fiis/gerenciar-proventos/historico/<int:id>/deletar/',
         views.FIIManageIncomeReceiptDeleteHistory.as_view(),
         name='fii_manage_income_receipt_delete',
         ),
    path('renda-fixa/',
         views.FixedIncomeView.as_view(),
         name='fixed_income',
         ),
    path('renda-fixa/registrar/',
         views.FixedIncomeRegisterView.as_view(),
         name='fixed_income_register',
         ),
    path('renda-fixa/<int:id>/detalhes/',
         views.FixedIncomeDetailsView.as_view(),
         name='fixed_income_details',
         ),
    path('renda-fixa/<int:id>/editar/',
         views.FixedIncomeEditView.as_view(),
         name='fixed_income_edit',
         ),
    path('renda-fixa/<int:id>/aplicar/',
         views.FixedIncomeApplyView.as_view(),
         name='fixed_income_apply',
         ),
    path('renda-fixa/<int:id>/resgatar/',
         views.FixedIncomeRedeemView.as_view(),
         name='fixed_income_redeem',
         ),
    path('renda-fixa/<int:id>/historico/',
         views.FixedIncomeHistoryView.as_view(),
         name='fixed_income_history',
         ),
    path('tesouro-direto/',
         views.DirectTreasureView.as_view(),
         name='direct_treasure',
         ),
    path('tesouro-direto/registrar/',
         views.DirectTreasureRegisterView.as_view(),
         name='direct_treasure_register',
         ),
    path('tesouro-direto/<int:id>/editar/',
         views.DirectTreasureEditView.as_view(),
         name='direct_treasure_edit',
         ),
    path('tesouro-direto/<int:id>/detalhes/',
         views.DirectTreasureDetailsView.as_view(),
         name='direct_treasure_details',
         ),
    path('tesouro-direto/<int:id>/aplicar/',
         views.DirectTreasureApplyView.as_view(),
         name='direct_treasure_apply'),
    path('tesouro-direto/<int:id>/resgatar/',
         views.DirectTreasureRedeemView.as_view(),
         name='direct_treasure_redeem'),
    path('tesouro-direto/<int:id>/historico/',
         views.DirectTreasureHistoryView.as_view(),
         name='direct_treasure_history'),
]
