from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date
from decimal import Decimal


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

    def redeem(self, date: date, value: float) -> None:
        if self.get_current_value() < value:
            raise ValidationError(
                ('saldo insuficiente para resgate'),
                code='invalid',
            )
        new_history = DirectTreasureHistory.objects.create(
            product=self,
            date=date,
            state='redeem',
            value=-abs(value),
        )
        new_history.save()

    def get_current_value(self) -> Decimal:
        history = DirectTreasureHistory.objects.filter(
            product=self
        )
        total = sum([h.get_final_value() for h in history])
        return Decimal(total)

    def get_total_profits_received(self) -> Decimal:
        return Decimal(0)


class DirectTreasureHistory(models.Model):
    product = models.ForeignKey(DirectTreasure, on_delete=models.CASCADE)
    date = models.DateField(default='2023-07-02')
    state = models.CharField(max_length=255, choices=(
        ('apply', 'apply'),
        ('redeem', 'redeem'),
    ))
    tax_and_irpf = models.DecimalField(max_digits=15,
                                       decimal_places=2,
                                       default=0,
                                       blank=True,
                                       null=True,
                                       )
    value = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.state} of R$ {self.value:.2f} in {self.date}'

    def get_final_value(self) -> float:
        return self.value - abs(self.tax_and_irpf)
