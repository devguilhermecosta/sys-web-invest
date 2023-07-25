from django.urls import path
from administration import views

app_name = 'admin'

urlpatterns = [
    path('cadastrar/fii/', views.FIIRegister.as_view(), name='fii_register'),
]
