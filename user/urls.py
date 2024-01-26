from django.urls import path
from . import views


app_name: str = 'user'


urlpatterns: list = [
    path('api/register/',
         views.UserRegisterAPIVire.as_view(),
         name='api-register',
         ),
    path('api/list/',
         views.UserListAPIView.as_view(),
         name='api-list',
         ),
    path('api/<int:pk>/',
         views.UserDetailsAPIView.as_view(),
         name='api-details',
         ),
    path('registrar/',
         views.UserRegister.as_view(),
         name='register'),
    path('registrar/register_create/',
         views.UserRegister.as_view(),
         name='register_create'),
    path('registrar/register_confirmation/',
         views.UserRegister.user_register_confirmation,
         name='register_confirmation'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('registrar/criar_perfil/',
         views.CreateProfile.as_view(),
         name='create_profile',
         ),
]
