from django.urls import path
from . import views


app_name: str = 'dashboard'


urlpatterns: list = [
    path('', views.HomeView.as_view(), name='home'),
    path('dashboard/', views.LoginView.as_view(),
         name='user_dashboard',
         ),
    path('dashboard/criar_perfil/',
         views.CreateProfile.as_view(),
         name='create_profile',
         )
]
