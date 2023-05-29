from django.urls import path
from . import views


app_name: str = 'user'


urlpatterns: list = [
    path('registrar/', views.UserRegister.as_view(), name="register")
]
