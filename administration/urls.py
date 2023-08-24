from django.urls import path
from administration import views

app_name = 'admin'

urlpatterns = [
    path('cadastrar/fii/',
         views.FIIRegister.as_view(),
         name='fii_register',
         ),
    path('cadastrar/fii/<str:code>/editar/',
         views.FIIUpdate.as_view(),
         name='fii_edit',
         ),
    path('cadastrar/fii/<str:code>/deletar/',
         views.FIIDelete.as_view(),
         name='fii_delete',
         ),
    path('cadastrar/acao/',
         views.ActionRegister.as_view(),
         name='action_register',
         ),
    path('cadastrar/acao/<str:code>/editar/',
         views.ActionUpdate.as_view(),
         name='action_edit',
         ),
    path('cadastrar/action/<str:code>/deletar/',
         views.ActionDelete.as_view(),
         name='action_delete',
         ),
    path('atualizar/precos/acoes/',
         views.ActionsUpdateLastCloseView.as_view(),
         name='update_actions_prices',
         ),
    path('atualizar/precos/fiis/',
         views.FIIsUpdateLastCloseView.as_view(),
         name='update_fiis_prices',
         ),
]
