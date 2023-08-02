from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from typing import TypeVar, List
from datetime import datetime as dt
from functools import reduce


date = '2023-07-04'
PDF = TypeVar('PDF', bytes, None)
QuerySet = TypeVar('QuerySet', list, None)


class Action(models.Model):
    code = models.CharField(max_length=5, unique=True)
    description = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=18, unique=True)

    def __str__(self) -> str:
        return self.description


class UserAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Action, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    date = models.DateField(default=date, auto_now=False, auto_now_add=False)
    handler = models.CharField(max_length=255, default='buy')

    def __str__(self):
        return f'{self.product.code} de {self.user.username}'

    def get_total_price(self) -> float:
        return round(self.quantity * float(self.unit_price), 2)

    def buy(self, date: str, quantity: int, unit_price: float, trading_note: PDF = None) -> None:  # noqa: E501
        """ create the new history """
        new_history = ActionHistory.objects.create(
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
        new_history = ActionHistory.objects.create(
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

    def receiv_profits(self,
                       handler: str,
                       date: str,
                       total_price: float,
                       tax_and_irpf: float | None = '',
                       ) -> None:
        new_history = ActionHistory.objects.create(
            userproduct=self,
            handler=handler,
            date=date,
            quantity=1,
            tax_and_irpf=tax_and_irpf,
            unit_price=total_price,
            total_price=total_price,
        )
        new_history.save()

    def get_history(self) -> QuerySet | None:
        ''' param: handler '''
        history = ActionHistory.objects.filter(
            userproduct=self,
        )
        return history

    def get_partial_profits(self) -> float | None:
        handler = ('dividends', 'jscp', 'remuneration', 'renting')
        history = []

        for h in self.get_history():
            if h.handler in handler:
                history.append(h.total_price)

        total = sum([value for value in history])
        return total

    def get_partial_tax(self) -> float | None:
        history = ActionHistory.objects.filter(
            userproduct=self,
        )

        total = reduce(lambda acc, num: acc + num,
                       [h.tax_and_irpf for h in history if h.tax_and_irpf],
                       0,
                       )
        return total

    @classmethod
    def get_total_profits(cls, user: User) -> float | None:
        queryset = cls.objects.filter(user=user)
        total = sum([item.get_partial_profits() for item in queryset])
        return total

    @classmethod
    def get_full_profits_history(cls, user: User) -> List[dict]:
        handler = ('dividends', 'jscp', 'remuneration', 'renting')
        history = []
        products = cls.objects.filter(user=user)

        for product in products:
            for h in product.get_history():
                if h.handler in handler:
                    tax = h.tax_and_irpf
                    total = h.total_price
                    history.append({
                        'date': h.date,
                        'product': product.product.code,
                        'handler': h.handler,
                        'tax': tax if tax else 0,
                        'gross_value': h.total_price,
                        'final_value': (total - tax) if tax else total,
                        'history_id': h.pk,
                    })

        history.sort(
            key=lambda item: dt.strptime(str(item['date']), '%Y-%m-%d',),
            reverse=True,
        )

        return history

    @classmethod
    def get_total_amount_invested(cls, user: User) -> float | None:
        queryset = cls.objects.filter(user=user)
        total = sum([item.get_total_price() for item in queryset])
        return total

    @classmethod
    def get_total_tax(cls, user: User) -> float | None:
        queryset = cls.objects.filter(user=user)
        total = sum([item.get_partial_tax() for item in queryset])
        return total


class ActionHistory(models.Model):
    upload = 'trading-notes/actions/'
    userproduct = models.ForeignKey(UserAction, on_delete=models.CASCADE)
    handler = models.CharField(max_length=255, choices=(
        ('B', 'buy'),
        ('S', 'sell'),
        ('D', 'dividends'),
        ('J', 'jscp'),
        ('R', 'remuneration'),
        ('rnt', 'renting'),
    ))
    date = models.DateField(default=date, auto_now=False, auto_now_add=False)
    quantity = models.IntegerField()
    tax_and_irpf = models.FloatField(blank=True, null=True)
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
            case 'dividends':
                handler = 'dividendos'
            case 'jscp':
                handler = 'jscp'
            case 'remuneration':
                handler = 'remuneração'
            case 'renting':
                handler = 'aluguel'
            case _:
                ''

        return (
            f'{handler} de {self.quantity} unidade(s) de '
            f'{self.userproduct.product.code} do usuário '
            f'{self.userproduct.user.username} realizada '
            f'no dia {self.date}')
