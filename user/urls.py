from django.urls import path
from . import views


app_name: str = 'user'


urlpatterns: list = [
    path('registrar/', views.UserRegister.as_view(), name="register"),
    path('register_create/',
         views.user_register,
         name="register_create"),
    path('register_session/',
         views.user_create,
         name="register_session"),
]
