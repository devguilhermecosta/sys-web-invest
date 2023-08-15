from django.urls import path
from administration import views

app_name = 'admin'

urlpatterns = [
    path('cadastrar/fii/',
         views.FIIRegister.as_view(),
         name='fii_register',
         ),
    path('cadastrar/fii/<str:code>/editar/',
         views.FIIEdit.as_view(),
         name='fii_edit',
         ),
    path('cadastrar/acao/',
         views.ActionRegister.as_view(),
         name='action_register',
         ),
    path('cadastrar/acao/<str:code>/editar/',
         views.ActionEdit.as_view(),
         name='action_edit',
         ),
]
