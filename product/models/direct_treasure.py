from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
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

    def get_absolute_url(self) -> str:
        return reverse(
            'product:direct_treasure_details',
            args=(self.pk,),
            )

    def get_current_value(self) -> Decimal:
        history = DirectTreasureHistory.objects.filter(product=self)
        total = sum(
            [h.get_final_value() for h in history if h.state != 'profits']
            )
        return Decimal(total)

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

    def receive_profits(self,
                        date: date,
                        value: float,
                        tax_and_irpf: float = 0) -> None:
        new_history = DirectTreasureHistory.objects.create(
            product=self,
            state='profits',
            date=date,
            tax_and_irpf=-abs(tax_and_irpf) if tax_and_irpf else 0,
            value=value,
        )
        new_history.save()

    def get_tax(self) -> Decimal:
        history = DirectTreasureHistory.objects.filter(product=self)
        total = sum([h.tax_and_irpf for h in history])
        return Decimal(total)

    def get_total_profits_received(self) -> Decimal:
        history = DirectTreasureHistory.objects.filter(
            product=self,
            state='profits',
        )
        total = sum([h.get_final_value() for h in history])
        return Decimal(total)

    @classmethod
    def get_total_amount_invested(cls, user: User) -> Decimal:
        products = cls.objects.filter(user=user)
        total = sum([p.get_current_value() for p in products])
        return Decimal(total)

    @classmethod
    def get_total_profits(cls, user: User) -> Decimal:
        products = cls.objects.filter(user=user)
        total = sum([p.get_total_profits_received() for p in products])
        return Decimal(total)

    @classmethod
    def get_total_tax(cls, user: User) -> Decimal:
        products = cls.objects.filter(user=user)
        total = sum([p.get_tax() for p in products])
        return Decimal(abs(total))


class DirectTreasureHistory(models.Model):
    product = models.ForeignKey(DirectTreasure, on_delete=models.CASCADE)
    date = models.DateField(default='2023-07-02')
    state = models.CharField(max_length=255, choices=(
        ('apply', 'apply'),
        ('redeem', 'redeem'),
        ('profits', 'recebimento de juros'),
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

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def save(self, *args, **kwargs) -> None:
        self.tax_and_irpf = -abs(self.tax_and_irpf)
        self.value = abs(self.value) if self.state != 'redeem' else -abs(self.value)  # noqa: E501
        return super().save(*args, **kwargs)
