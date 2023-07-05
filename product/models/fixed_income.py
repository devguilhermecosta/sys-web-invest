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
        ('db', 'debêntures'),
    ))
    name = models.CharField(max_length=255)
    value = models.FloatField()
    grace_period = models.DateField(default='2023-07-01')
    maturity_date = models.DateField(default='2023-07-01')
    liquidity = models.CharField(max_length=255, choices=(
        ('nv', 'no vencimento'),
        ('di', 'diária'),
        ('30d', '30 dias'),
        ('30d+', '30 dias +'),
        ('30d-', '30 dias -'),
    ))
    profitability = models.CharField(max_length=255)
    interest_receipt = models.CharField(max_length=255, choices=(
        ('nh', 'não há'),
        ('m', 'mensal'),
        ('tm', 'trimestral'),
        ('sm', 'semestral'),
        ('a', 'anual'),
    ))
    description = models.TextField()

# métodos: aplicar, resgatar, receber juros, histórico.
