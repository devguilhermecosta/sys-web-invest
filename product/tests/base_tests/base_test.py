from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from pathlib import Path
from product.models import (
    Action,
    FII,
    ProductFixedIncome,
    DirectTreasure,
    )
import c2validator as c2


def make_action(code: str, desc: str, cnpj: str = None) -> Action:
    ''' create a new Action object '''
    new_action = Action.objects.create(
        code=code,
        description=desc,
        cnpj=cnpj or c2.create_cnpj(),
    )
    new_action.save()

    return new_action


def make_fii(code: str, desc: str, cnpj: str = None) -> FII:
    ''' create a new FII object '''
    new_fii = FII.objects.create(
        code=code,
        description=desc,
        cnpj=cnpj or c2.create_cnpj(),
    )
    new_fii.save()

    return new_fii


def make_simple_file() -> SimpleUploadedFile:
    path = Path(__file__).parent.parent.parent.parent
    file_path = ''.join(
        (str(path), '/product/tests/base_tests/file_test.pdf')
    )
    simple_file = SimpleUploadedFile(
        name='file_test.pdf',
        content=open(file_path, 'rb').read(),
        content_type='file/pdf'
    )
    return simple_file


def make_fixed_income_product(user: User, **kwargs) -> ProductFixedIncome:
    '''
        create a new fixed income object

        kwargs opts: category, name
    '''
    new_object = ProductFixedIncome.objects.create(
        user=user,
        category=kwargs.pop('category', 'cdb'),
        name=kwargs.pop('name', 'cdb bb 2035'),
        value=kwargs.pop('value', 1250),
        grace_period='2023-07-04',
        maturity_date='2035-01-01',
        liquidity='no vencimento',
        profitability='102% cdi',
        interest_receipt='não há',
        description='cdb muito legal'
    )
    new_object.save()
    return new_object


def make_direct_treasure(user: User, **kwargs) -> DirectTreasure:
    '''
        create a new direct treasure object
    '''
    new_object = DirectTreasure.objects.create(
        user=user,
        name='tesouro ipca+ 2024',
        category='ipca',
        interest_receipt='não há',
        profitability='ipca + 4,9% a.a.',
        maturity_date='2024-12-31',
        value=kwargs.get('value', 1500),
        description='tesouro ipca sem pagamento de juros'
    )
    new_object.save()
    return new_object
