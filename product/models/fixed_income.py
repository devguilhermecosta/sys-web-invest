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
    value = models.FloatField()
    grace_period = models.DateField(default='2023-07-01')
    maturity_date = models.DateField(default='2023-07-01')
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
    description = models.TextField()

    def __str__(self) -> str:
        return self.name

    def get_total_applied(self) -> float:
        return self.value

    def make_history(self, state: str, date: date, value: float) -> None:
        new_history = FixedIncomeHistory.objects.create(
            product=self,
            state=state,
            date=date,
            value=value
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
            tax_and_irpf=tax_and_irpf if tax_and_irpf else 0,
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
        return self.value - self.tax_and_irpf

    def __str__(self) -> str:
        history = (
            f'{self.product.name} - {self.date} - {self.state} - {self.value}'
            )
        return history
