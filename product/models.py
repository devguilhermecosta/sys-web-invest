from django.db import models
from django.contrib.auth.models import User


'''
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
