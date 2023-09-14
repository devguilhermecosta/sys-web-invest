from django.urls import path
from . import views


app_name = 'improvement'

urlpatterns = [
    path('', views.ImprovementCreate.as_view(), name='create'),
    path('minha-lista/', views.ImprovementList.as_view(), name='list'),
]
