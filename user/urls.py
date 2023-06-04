from django.urls import path
from . import views


app_name: str = 'user'


urlpatterns: list = [
    path('registrar/',
         views.UserRegister.as_view(),
         name='register'),
    path('registrar/register_create/',
         views.UserRegister.as_view(),
         name='register_create'),
    path('registrar/register_confirmation/',
         views.UserRegister.user_register_confirmation,
         name='register_confirmation'),
    path('activate/<uidb64>/<token>', views.activate, name='activate')
]
