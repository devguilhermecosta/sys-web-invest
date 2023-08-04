from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from typing import TypeVar, List
from datetime import datetime as dt
from decimal import Decimal


date = '2023-07-04'
PDF = TypeVar('PDF', bytes, None)
QuerySet = TypeVar('QuerySet', list, None)


class FII(models.Model):
    code = models.CharField(max_length=6, unique=True)
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

    def get_total_price(self) -> Decimal:
        return Decimal((self.quantity * self.unit_price))

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

    def receive_profits(self, value: float, date: str) -> None:
        new_history = FiiHistory.objects.create(
            userproduct=self,
            handler='profits',
            date=date,
            quantity=1,
            unit_price=value,
            total_price=value,
        )
        new_history.save()
        self.save()

    def get_partial_history(self, handler: str) -> QuerySet:
        history = FiiHistory.objects.filter(
            userproduct=self,
            handler=handler,
        )
        return history

    def get_partial_profits(self) -> float:
        history = self.get_partial_history(handler='profits')
        total = sum([h.total_price for h in history])
        return total

    @classmethod
    def get_total_amount_invested(cls, user: User) -> float:
        uf_query_set = cls.objects.filter(
            user=user
        )
        total = sum([uf.get_total_price() for uf in uf_query_set])
        return total

    @classmethod
    def get_total_profits(cls, user: User) -> float:
        products = UserFII.objects.filter(user=user)
        total = sum([p.get_partial_profits() for p in products])
        return total

    @classmethod
    def get_full_history(cls, user: User, handler: str) -> List[dict] | None:
        ''' handler: buy, redeem or profits  '''
        history = []

        products = UserFII.objects.filter(
            user=user,
        )

        for product in products:
            for h in product.get_partial_history(handler):
                history.append({
                    'date': h.date,
                    'history_id': h.pk,
                    'product': product.product.code,
                    'value': h.total_price,
                    'handler': h.handler,
                })

        history.sort(
            key=lambda item: dt.strptime(str(item['date']), '%Y-%m-%d',),
            reverse=True,
        )

        return history


class FiiHistory(models.Model):
    upload = 'trading-notes/fiis/'
    userproduct = models.ForeignKey(UserFII, on_delete=models.CASCADE)
    handler = models.CharField(max_length=255, choices=(
        ('B', 'buy'),
        ('S', 'sell'),
        ('P', 'profits'),
    ))
    date = models.DateField(default=date, auto_now=False, auto_now_add=False)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=15, decimal_places=2)
    total_price = models.DecimalField(max_digits=15, decimal_places=2)
    trading_note = models.FileField(blank=True, null=True, upload_to=upload)

    def __str__(self) -> str:
        handler = ''
        match self.handler:
            case 'buy':
                handler = 'compra'
            case 'sell':
                handler = 'venda'
            case 'profits':
                handler = 'lucros'
            case _:
                ''

        return (
            f'{handler} de {self.quantity} unidade(s) de '
            f'{self.userproduct.product.code} do usuário '
            f'{self.userproduct.user.username} realizada '
            f'no dia {self.date}')
