from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from typing import TypeVar


date = '2023-07-04'
PDF = TypeVar('PDF', bytes, None)


class FII(models.Model):
    code = models.CharField(max_length=5, unique=True)
    description = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=18, unique=True)

    def __str__(self) -> str:
        return self.code


class UserFII(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(FII, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    date = models.DateField(default=date, auto_now=False, auto_now_add=False)
    handler = models.CharField(max_length=255, default='buy')

    def __str__(self) -> str:
        return f'{self.product.code} de {self.user.username}'

    def get_total_price(self) -> float:
        return round(self.quantity * float(self.unit_price), 2)

    def buy(self, date: str, quantity: int, unit_price: float, trading_note: PDF = None) -> None:  # noqa: E501
        """ create the new history """
        new_history = FiiHistory.objects.create(
            userproduct=self,
            handler='buy',
            date=date,
            quantity=quantity,
            unit_price=unit_price,
            total_price=quantity * unit_price,
            trading_note=trading_note,
        )
        new_history.save()
        self.quantity += quantity
        self.unit_price = (self.unit_price + unit_price) / 2
        self.save()

    def sell(self, date: str, quantity: int, unit_price: float, trading_note: PDF = None) -> None:  # noqa: E501
        if quantity > self.quantity:
            raise ValidationError(
                {'quantity': 'quantidade insuficiente para venda'},
                code='invalid'
            )
        new_history = FiiHistory.objects.create(
            userproduct=self,
            handler='sell',
            date=date,
            quantity=quantity,
            unit_price=unit_price,
            total_price=quantity * unit_price,
            trading_note=trading_note,
        )
        new_history.save()
        self.quantity -= quantity
        self.unit_price = (self.unit_price + unit_price) / 2
        self.save()


class FiiHistory(models.Model):
    upload = 'trading-notes/fiis/'
    userproduct = models.ForeignKey(UserFII, on_delete=models.CASCADE)
    handler = models.CharField(max_length=255, choices=(
        ('B', 'buy'),
        ('S', 'sell'),
        ('P', 'proceeds'),
    ))
    date = models.DateField(default=date, auto_now=False, auto_now_add=False)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    total_price = models.FloatField()
    trading_note = models.FileField(blank=True, null=True, upload_to=upload)

    def __str__(self) -> str:
        handler = ''
        match self.handler:
            case 'buy':
                handler = 'compra'
            case 'sell':
                handler = 'venda'
            case 'proceeds':
                handler = 'aluguel'
            case _:
                ''

        return (
            f'{handler} de {self.quantity} unidade(s) de '
            f'{self.userproduct.product.code} do usuário '
            f'{self.userproduct.user.username} realizada '
            f'no dia {self.date}')
