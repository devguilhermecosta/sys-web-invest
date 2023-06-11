from django.urls import path
from . import views


app_name: str = 'dashboard'


urlpatterns: list = [
    path('', views.LoginView.as_view(), name='home'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('dashboard/painel-do-usuario/', views.DashboardView.as_view(),
         name='user_dashboard',
         ),
]
