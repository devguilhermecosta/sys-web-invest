from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=11, unique=True)
    adress = models.CharField(max_length=255)
    number = models.CharField(max_length=15)
    city = models.CharField(max_length=255)
    uf = models.CharField(max_length=30)
    cep = models.CharField(max_length=10)

    def __str__(self) -> str:
        return f'Perfil de {self.user}'
