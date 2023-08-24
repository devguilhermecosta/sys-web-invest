from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.urls import reverse
from typing import TypeVar, List
from datetime import datetime as dt
from decimal import Decimal


date = '2023-07-04'
PDF = TypeVar('PDF', bytes, None)
QuerySet = TypeVar('QuerySet', list, None)


class FII(models.Model):
    code = models.CharField(max_length=6,
                            unique=True,
                            error_messages={
                                'unique': 'Este código já está em uso',
                            })
    description = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=18,
                            unique=True,
                            error_messages={
                                'unique': 'Este CNPJ já está em uso',
                            })
    last_close = models.DecimalField(blank=True,
                                     null=True,
                                     default=1,
                                     max_digits=15,
                                     decimal_places=2,
                                     )

    def __str__(self) -> str:
        return self.code

    def get_url_update(self) -> str:
        return reverse('admin:fii_edit', args=(self.code,))

    def get_url_delete(self) -> str:
        return reverse('admin:fii_delete', args=(self.code,))

    def update_last_close(self, last_close: Decimal) -> None:
        self.last_close = last_close
        self.save()


class UserFII(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(FII, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.product.code} de {self.user.username}'

    def get_url_delete(self) -> str:
        return reverse('product:fiis_delete', args=(self.id,))

    def buy(self, date: str, quantity: int, unit_price: float, trading_note: PDF = None) -> None:  # noqa: E501
        """ create the new history """
        new_history = FiiHistory.objects.create(
            userproduct=self,
            handler='buy',
            date=date,
            quantity=quantity,
            unit_price=unit_price,
            trading_note=trading_note,
        )
        new_history.save()

    def sell(self, date: str, quantity: int, unit_price: float, trading_note: PDF = None) -> None:  # noqa: E501
        if quantity > self.get_quantity():
            raise ValidationError(
                {'quantity': 'quantidade insuficiente para venda'},
                code='invalid'
            )
        new_history = FiiHistory.objects.create(
            userproduct=self,
            handler='sell',
            date=date,
            quantity=-abs(quantity),
            unit_price=unit_price,
            trading_note=trading_note,
        )
        new_history.save()

    def receive_profits(self, unit_price: float, date: str) -> None:
        new_history = FiiHistory.objects.create(
            userproduct=self,
            handler='profits',
            date=date,
            quantity=1,
            unit_price=unit_price,
        )
        new_history.save()

    def get_quantity(self) -> int:
        handler = ('buy', 'sell')
        history = FiiHistory.objects.filter(userproduct=self)
        total = sum([h.quantity for h in history if h.handler in handler])
        return total

    def get_middle_price(self) -> Decimal:
        history = FiiHistory.objects.filter(userproduct=self, handler='buy')
        total = sum([h.unit_price for h in history])
        return Decimal(total / len(history)) if total != 0 else 0

    def previous_close(self) -> Decimal:
        return self.product.last_close

    def get_current_value_invested(self) -> Decimal:
        total = self.get_quantity() * self.previous_close()
        return Decimal(total) if total >= 0 else 0

    def get_partial_history(self, handler: str) -> QuerySet:
        history = FiiHistory.objects.filter(
            userproduct=self,
            handler=handler,
        )
        return history

    def get_partial_profits(self) -> float:
        history = self.get_partial_history(handler='profits')
        total = sum([h.get_final_value() for h in history])
        return total

    @classmethod
    def get_total_amount_invested(cls, user: User) -> float:
        uf_query_set = cls.objects.filter(
            user=user
        )
        total = sum([uf.get_current_value_invested() for uf in uf_query_set])
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
                    'value': h.get_final_value(),
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

    def get_final_value(self) -> Decimal:
        quantity = abs(self.quantity) if self.quantity != 0 else 1
        total = quantity * self.unit_price
        return Decimal(total)

    def get_url_delete(self) -> str:
        return reverse(
            'product:fiis_history_delete',
            kwargs={
                'h_id': self.id,
                'p_id': self.userproduct.id,
            }
        )

    def update(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
