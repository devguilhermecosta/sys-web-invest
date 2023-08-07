from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.urls import reverse
from django.test.client import Client
from pathlib import Path
from product.models import (
    Action,
    FII,
    UserAction,
    UserFII,
    ActionHistory,
    FiiHistory,
    ProductFixedIncome,
    DirectTreasure,
    )
from datetime import date
from typing import NewType, Dict
import c2validator as c2


LoginFunction = NewType('LoginFunction', HttpRequest)


def make_action(code: str, desc: str, cnpj: str = None) -> Action:
    ''' create a new Action object '''
    new_action = Action.objects.create(
        code=code,
        description=desc,
        cnpj=cnpj or c2.create_cnpj(),
    )
    new_action.save()

    return new_action


def make_user_action(user: User,
                     qty: int,
                     unit_price: float,
                     code: str,
                     desc: str,
                     **kwargs,
                     ) -> UserAction:
    new_obj = UserAction.objects.create(
        user=user,
        product=make_action(code, desc, cnpj=c2.create_cnpj()),
        quantity=qty,
        unit_price=unit_price,
        date=date.today().strftime('%Y-%m-%d'),
        handler=kwargs.get('handler', 'buy'),
    )
    new_obj.save()
    return new_obj


def make_fii(code: str, desc: str, cnpj: str = None) -> FII:
    ''' create a new FII object '''
    new_fii = FII.objects.create(
        code=code,
        description=desc,
        cnpj=cnpj or c2.create_cnpj(),
    )
    new_fii.save()

    return new_fii


def make_user_fii(user: User,
                  qty: int,
                  unit_price: float,
                  code: str,
                  desc: str,
                  **kwargs,
                  ) -> UserFII:
    new_obj = UserFII.objects.create(
        user=user,
        product=make_fii(code, desc, cnpj=c2.create_cnpj()),
        quantity=qty,
        unit_price=unit_price,
        date=date.today().strftime('%Y-%m-%d'),
        handler=kwargs.get('handler', 'buy'),
    )
    new_obj.save()
    return new_obj


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

        kwargs opts: category, name, value, interest_receipt, tax,
        profits_value

        if you can create an tax, you need set the profits_value argument
    '''
    new_object = ProductFixedIncome.objects.create(
        user=user,
        category=kwargs.pop('category', 'cdb'),
        name=kwargs.pop('name', 'cdb bb 2035'),
        grace_period='2023-07-04',
        maturity_date='2035-01-01',
        liquidity='no vencimento',
        profitability='102% cdi',
        interest_receipt=kwargs.get('interest_receipt', 'não há'),
        description='cdb muito legal'
    )
    new_object.save()

    value = kwargs.get('value', None)
    tax = kwargs.get('tax', None)
    profits_value = kwargs.get('profits_value', None)

    if value:
        if tax and profits_value:
            new_object.receive_profits(
                date='2023-07-02',
                value=profits_value,
                tax_and_irpf=tax,
            )

        new_object.apply('2023-07-02', value)

    return new_object


def make_direct_treasure(user: User, **kwargs) -> DirectTreasure:
    '''
        create a new direct treasure object

        kwargs: value, interest_receipt, tax, profits_value

        if value, a new history will be created
        if tax and profits_value, a new profits history
        is created
    '''
    new_object = DirectTreasure.objects.create(
        user=user,
        name=kwargs.get('name', 'tesouro ipca+ 2024'),
        category='ipca',
        interest_receipt=kwargs.get('interest_receipt', 'não há'),
        profitability='ipca + 4,9% a.a.',
        maturity_date='2024-12-31',
        description='tesouro ipca sem pagamento de juros'
    )
    new_object.save()

    value = kwargs.get('value', 1)
    tax = kwargs.get('tax', None)
    profits_value = kwargs.get('profits_value', None)

    # create a history profits
    if tax and profits_value:
        new_object.receive_profits(
            date='2023-07-02',
            value=profits_value,
            tax_and_irpf=tax,
        )

    # create a history apply
    if value:
        new_object.apply('2023-07-02', value)

    return new_object


def create_profits_history(client: Client,
                           login_function: LoginFunction,
                           **kwargs) -> Dict:  # noqa: E501
    """ this function creates a new user, user_fii and
        a new profits history.

        if you need create a custom history, set the following
        kwargs.

        kwargs:
            code: make a new UserFII with this code
            desc: make a new UserFII with this description
            value_aplication: make a new UserFII with
            this unit_price
            profits_value: make a new History Profits
            with this value

    returns a instance of User, UserFII, FiiHistory(QuerySet)
    and a HttpResponse
    """
    # make login
    _, user = login_function()

    # create the user fii
    user_product = make_user_fii(user,
                                 1,
                                 kwargs.get('value_aplication', 1),
                                 kwargs.get('code', 'mxrf11'),
                                 kwargs.get('desc', 'maxi renda'),
                                 )

    # add a profits
    response = client.post(
        reverse('product:fiis_manage_income_receipt'),
        {
            'userproduct': user_product.id,
            'total_price': kwargs.get('profits_value', 10),
            'date': '2023-07-02',
        },
        follow=True,
    )

    history = FiiHistory.objects.filter(
        userproduct=user_product,
        handler='profits',
    )

    return {
        'user': user,
        'user_fii': user_product,
        'history': history,
        'response': response,
    }


def create_actions_history(client: Client,
                           login_function: LoginFunction,
                           **kwargs) -> Dict:  # noqa: E501
    """ this function creates a new user, user_action and
        a new profits history.

        if you need create a custom history, set the following
        kwargs.

        kwargs:
            code: make a new UserAction with this code
            desc: make a new UserAction with this description
            value_aplication: make a new UserAction with
            this unit_price


            date: received date
            handler: name of handler: ex: 'dividends, jscp...'
            tax_and_irpf: value of tax
            gross_value: total value received

    returns a instance of User, UserAction, FiiHistory(QuerySet)
    and a HttpResponse
    """
    # make login
    _, user = login_function()

    # create the user fii
    user_product = make_user_action(user,
                                    1,
                                    kwargs.get('value_aplication', 1),
                                    kwargs.get('code', 'bbas3'),
                                    kwargs.get('desc', 'banco do brasil'),
                                    )

    # add a profits
    response = client.post(
        reverse('product:actions_manage_profits'),
        {
            'userproduct': user_product.id,
            'handler': kwargs.get('handler', 'dividends'),
            'date': kwargs.get('date', '2023-07-02'),
            'tax_and_irpf': kwargs.get('tax_and_irpf', 0),
            'total_price': kwargs.get('gross_value', 10),
        },
        follow=True,
    )

    history = ActionHistory.objects.filter(
        userproduct=user_product,
    )

    return {
        'user': user,
        'user_action': user_product,
        'history': history,
        'response': response,
    }
