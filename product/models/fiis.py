from django.db import models
from django.contrib.auth.models import User


class FIIS(models.Model):
    code = models.CharField(max_length=5, unique=True)
    description = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=18, unique=True)


class UserFII(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fii = models.ForeignKey(FIIS, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()

    def get_total_price(self) -> float:
        return round(self.quantity * float(self.unit_price), 2)
