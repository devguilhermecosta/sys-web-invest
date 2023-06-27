from product.models import Action
import c2validator as c2


def make_action(code: str, desc: str, cnpj: str) -> Action:
    ''' create a new Action object '''
    new_action = Action.objects.create(
        code=code,
        description=desc,
        cnpj=cnpj or c2.create_cnpj(),
    )
    new_action.save()

    return new_action
