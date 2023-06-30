from product.models import Action, FII
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
