from django.urls import path
from administration import views

app_name = 'admin'

urlpatterns = [
    path('cadastrar/fii/',
         views.FIIRegister.as_view(),
         name='fii_register',
         ),
    path('cadastrar/acao/',
         views.ActionRegister.as_view(),
         name='action_register',
         ),
]
