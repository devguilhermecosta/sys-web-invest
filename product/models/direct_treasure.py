from django.db import models
from django.contrib.auth.models import User


class DirectTreasure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, choices=(
        ('selic', 'selic'),
        ('ipca', 'ipca'),
        ('prefixado', 'prefixado'),
    ))
    interest_receipt = models.CharField(max_length=255, choices=(
        ('não há', 'não há'),
        ('mensal', 'mensal'),
        ('trimestral', 'trimestral'),
        ('semestral', 'semestral'),
        ('anual', 'anual'),
    ))
    profitability = models.CharField(max_length=255)
    maturity_date = models.DateField(default='2023-07-02')
    value = models.FloatField()
    description = models.TextField()

    def __str__(self) -> str:
        return self.name
