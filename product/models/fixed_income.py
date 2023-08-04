from django.db import models
from django.contrib.auth.models import User
from datetime import date


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

    def get_current_value(self) -> float:
        history = FixedIncomeHistory.objects.filter(product=self)
        total = sum([h.get_final_value() for h in history])
        return total

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


class FixedIncomeHistory(models.Model):
    product = models.ForeignKey(ProductFixedIncome,
                                on_delete=models.CASCADE,
                                )
    state = models.CharField(max_length=255, default='apply', choices=(
        ('apply', 'apply'),
        ('redeem', 'redeem'),
        ('profits', 'profits'),
    ))
    date = models.DateField(default='2023-07-02')
    tax_and_irpf = models.FloatField(default=0, blank=True, null=True)
    value = models.FloatField()

    def get_final_value(self) -> float:
        return self.value - abs(self.tax_and_irpf)

    def __str__(self) -> str:
        history = (
            f'{self.product.name} - {self.date} - {self.state} - {self.value}'
            )
        return history
