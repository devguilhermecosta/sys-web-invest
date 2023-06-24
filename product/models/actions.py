from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from typing import TypeVar
from datetime import date as dt

date = dt.today().strftime('%Y-%m-%d')

PDF = TypeVar('PDF', bytes, None)


class Action(models.Model):
    code = models.CharField(max_length=5, unique=True)
    description = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=18, unique=True)

    def __str__(self) -> str:
        return self.description


class UserAction(models.Model):
    upload = 'trading-notes/actions/'
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    date = models.DateField(default=date, auto_now=False, auto_now_add=False)
    trading_note = models.FileField(blank=True, null=True, upload_to=upload)
    handler = models.CharField(max_length=255, default='buy')

    def __str__(self):
        return f'{self.action.code} de {self.user.username}'

    def buy(self, date: str, quantity: int, unit_price: float, trading_note: PDF = None) -> None:  # noqa: E501
        """ create the new history """
        history = ActionHistory.objects.create(
            useraction=self,
            handler='buy',
            date=date,
            quantity=quantity,
            unit_price=unit_price,
            total_price=quantity * unit_price,
            trading_note=trading_note,
        )
        history.save()
        self.quantity += quantity
        self.unit_price = (self.unit_price + unit_price) / 2
        self.save()

    def sell(self, quantity: int) -> None:
        if quantity > self.quantity:
            raise ValidationError(
                {'quantity': 'quantidade insuficiente para venda'},
                code='invalid'
            )
        self.quantity -= quantity
        self.save()

    def get_total_price(self) -> float:
        return round(self.quantity * float(self.unit_price), 2)


class ActionHistory(models.Model):
    upload = 'trading-notes/actions/'
    useraction = models.ForeignKey(UserAction, on_delete=models.CASCADE)
    handler = models.CharField(max_length=255, choices=(
        ('B', 'buy'),
        ('S', 'sell'),
        ('J', 'jscp'),
        ('P', 'proceeds'),
    ))
    date = models.DateField(default=date, auto_now=False, auto_now_add=False)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    total_price = models.FloatField()
    trading_note = models.FileField(blank=True, null=True, upload_to=upload)

    def __str__(self) -> str:
        return (
            f'compra de {self.quantity} unidade(s) de '
            f'{self.useraction.action.code} do usuário '
            f'{self.useraction.user.username} realizada '
            f'no dia {self.date}')

    def get_total_price(self):
        return self.quantity * self.unit_price
