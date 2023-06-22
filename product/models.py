from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


'''
- permitir anexar nota de compra e venda;
- cada ativo terá um usuário;
- o mesmo ativo pode ser cadastrado por diferentes usuários;
- mas o ativo não pode ser registrado duas vezes pelo
- mesmo usuário;
- se o ativo tiver registro de proventos, não poderá ser deletado;
- cada ativo terá os seguintes métodos:
- cadastrar;
- comprar;
- vender;
- acertar;
- deletar;
- editar;
- lançar provento;
'''
'''
ações - código b3, cnpj, descrição, categoria
fiis - cógio b3, cnpj, descrição, categoria
renda fixa - cnpj da corretora, descrição,
            rentabilidade, pagamento de proventos (periodicidade), categoria;
tesouro ditero - cnpj da corretora, descrição, rentabilidade,
pagamento de proventos (periodicidade), categoria.
'''


class Action(models.Model):
    code = models.CharField(max_length=5, unique=True)
    description = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=18, unique=True)

    def __str__(self) -> str:
        return self.description


class FIIS(models.Model):
    code = models.CharField(max_length=5, unique=True)
    description = models.CharField(max_length=50)
    cnpj = models.CharField(max_length=18, unique=True)


class UserAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()

    def buy(self, quantity: int, unit_price: float) -> None:
        self.quantity += quantity
        self.unit_price = (self.unit_price + unit_price) / 2
        self.save()

    def sell(self, quantity) -> None:
        if quantity > self.quantity:
            raise ValidationError(
                {
                    'quantity': 'quantidade insuficiente para venda',
                },
                code='invalid'
            )

        if quantity <= 0:
            raise ValidationError(
                ('informe uma quantidade maior que zero'),
                code='invalid'
            )

        self.quantity -= quantity
        self.save()

    def get_total_price(self) -> float:
        return round(self.quantity * float(self.unit_price), 2)


class UserFII(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fii = models.ForeignKey(FIIS, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.FloatField()

    def get_total_price(self) -> float:
        return round(self.quantity * float(self.unit_price), 2)
