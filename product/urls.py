from django.urls import path
from django.views.generic import TemplateView


app_name: str = 'product'


urlpatterns = [
    path('acoes/', TemplateView.as_view(
        template_name='product/pages/acoes.html',
        ), name='actions'),
    path('fiis/', TemplateView.as_view(
        template_name='product/pages/fiis.html',
        ), name='fiis'),
    path('renda-fixa/', TemplateView.as_view(
        template_name='product/pages/fixed_income.html',
        ), name='fixed_income'),
    path('tesouro-direto/', TemplateView.as_view(
        template_name='product/pages/direct_treasure.html',
        ), name='direct_treasure'),
]
