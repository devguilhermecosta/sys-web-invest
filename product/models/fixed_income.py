from django.db import models
from django.contrib.auth.models import User


class ProductFixedIncome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, choices=(
        ('cdb', 'cdb'),
        ('cra', 'cra'),
        ('cri', 'cri'),
        ('lc', 'lc'),
        ('lci', 'lci'),
        ('lca', 'lca'),
        ('lf', 'lf'),
        ('lfsn', 'lfsn'),
        ('debêntures', 'debêntures'),
    ))
    name = models.CharField(max_length=255)
    value = models.FloatField()
    grace_period = models.DateField(default='2023-07-01')
    maturity_date = models.DateField(default='2023-07-01')
    liquidity = models.CharField(max_length=255, choices=(
        ('no vencimento', 'no vencimento'),
        ('diária', 'diária'),
        ('30 dias', '30 dias'),
        ('30 dias +', '30 dias +'),
        ('30 dias -', '30 dias -'),
    ))
    profitability = models.CharField(max_length=255)
    interest_receipt = models.CharField(max_length=255, choices=(
        ('não há', 'não há'),
        ('mensal', 'mensal'),
        ('trimestral', 'trimestral'),
        ('semestral', 'semestral'),
        ('anual', 'anual'),
    ))
    description = models.TextField()

# métodos: aplicar, resgatar, receber juros, histórico.
