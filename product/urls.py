from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name: str = 'product'


urlpatterns = [
    path('acoes/', views.ActionsView.as_view(), name='actions'),
    path('acoes/lista/', views.AllActionsView.as_view(), name='actions_list'),
    path('acoes/comprar/', views.ActionsBuyView.as_view(), name='actions_buy'),
    path('fiis/', views.FIIsView.as_view(), name='fiis'),
    path('fiis/comprar/', views.FIISBuyView.as_view(), name='fiis_buy'),
    path('renda-fixa/', TemplateView.as_view(
        template_name='product/pages/fixed_income.html',
        ), name='fixed_income'),
    path('tesouro-direto/', TemplateView.as_view(
        template_name='product/pages/direct_treasure.html',
        ), name='direct_treasure'),
]
