from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date
from decimal import Decimal


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
    grace_period = models.DateField(default='')
    maturity_date = models.DateField(default='')
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
    description = models.TextField(default='', blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse(
            'product:fixed_income_details',
            args=(self.pk,),
            )

    def get_history_url(self) -> str:
        return reverse(
            'product:fixed_income_history',
            args=(self.id,)
            )

    def get_current_value(self) -> Decimal:
        history = FixedIncomeHistory.objects.filter(product=self)
        total = sum(
            [h.get_final_value() for h in history if h.state != 'profits']
            )
        return Decimal(total)

    def get_total_profits_received(self) -> Decimal:
        history = FixedIncomeHistory.objects.filter(
            product=self,
            state='profits',
            )
        total = sum([h.get_final_value() for h in history])
        return Decimal(total)

    def get_tax(self) -> Decimal:
        history = FixedIncomeHistory.objects.filter(product=self)
        total = sum([h.tax_and_irpf for h in history])
        return Decimal(total)

    def apply(self, date: date, value: float) -> None:
        new_history = FixedIncomeHistory.objects.create(
            product=self,
            state='apply',
            date=date,
            value=abs(value),
        )
        new_history.save()

    def redeem(self, date: date, value: float) -> None:
        new_history = FixedIncomeHistory.objects.create(
            product=self,
            state='redeem',
            date=date,
            value=-abs(value),
        )
        new_history.save()

    def receive_profits(self,
                        date: date,
                        value: float,
                        tax_and_irpf: float = 0) -> None:
        new_history = FixedIncomeHistory.objects.create(
            product=self,
            state='profits',
            date=date,
            tax_and_irpf=-abs(tax_and_irpf) if tax_and_irpf else 0,
            value=value,
        )
        new_history.save()

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


class FixedIncomeHistory(models.Model):
    product = models.ForeignKey(ProductFixedIncome,
                                on_delete=models.CASCADE,
                                )
    state = models.CharField(max_length=255, default='apply', choices=(
        ('apply', 'aplicação'),
        ('redeem', 'resgate'),
        ('profits', 'recebimento de juros'),
    ))
    date = models.DateField(default='2023-07-02')
    tax_and_irpf = models.DecimalField(default=0,
                                       max_digits=15,
                                       blank=True, null=True,
                                       decimal_places=2,
                                       )
    value = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.product.name} - {self.date} - {self.state} - {self.value}'  # noqa: E501

    def get_absolute_url(self) -> str:
        return reverse(
            'product:fixed_income_history_edit',
            kwargs={
                'product_id': self.product.id,
                'history_id': self.id,
                }
            )

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
