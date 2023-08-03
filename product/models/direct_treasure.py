from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date


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

    def make_initial_history(self, date: date, value: float) -> None:
        new_history = DirectTreasureHistory.objects.create(
            product=self,
            date=date,
            state='apply',
            value=value,
        )
        new_history.save()

    def apply(self, date: date, value: float) -> None:
        new_history = DirectTreasureHistory.objects.create(
            product=self,
            date=date,
            state='apply',
            value=value,
        )
        new_history.save()
        self.value += value
        self.save()

    def redeem(self, date: date, value: float) -> None:
        if self.value < value:
            raise ValidationError(
                ('saldo insuficiente para resgate'),
                code='invalid',
            )
        new_history = DirectTreasureHistory.objects.create(
            product=self,
            date=date,
            state='redeem',
            value=value,
        )
        new_history.save()
        self.value -= value
        self.save()

    def get_total_value(self) -> float:
        return self.value


class DirectTreasureHistory(models.Model):
    product = models.ForeignKey(DirectTreasure, on_delete=models.CASCADE)
    date = models.DateField(default='2023-07-02')
    state = models.CharField(max_length=255, choices=(
        ('apply', 'apply'),
        ('redeem', 'redeem'),
    ))
    tax_and_irpf = models.FloatField(default=0, blank=True, null=True)
    value = models.FloatField()

    def __str__(self) -> str:
        return f'{self.state} of R$ {self.value:.2f} in {self.date}'

    def get_final_value(self) -> float:
        return self.value - self.tax_and_irpf
