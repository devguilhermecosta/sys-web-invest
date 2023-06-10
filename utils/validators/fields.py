from django.core.exceptions import ValidationError


def length_validate(field) -> str:
    '''
        if len(field) <= 0 -> raise ValidationError,
        else return field.
    '''
    if len(field) <= 0 or field == '':
        raise ValidationError(
            ('Campo obrigatório'),
            code='required',
        )

    return field
