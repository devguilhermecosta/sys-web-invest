from django import forms
from django.core.exceptions import ValidationError
from user.models import Profile
from utils.forms.style import add_css_class
from utils.validators.fields import length_validate
import c2validator as c2
import re


def validate_cep(cep) -> str:
    regex = re.compile(r'^[0-9]{8}$')

    if not regex.match(cep):
        raise ValidationError(
            ('O cep deve ser composto somente por números '
             'e ter 8 catacteres.'
             ),
            code='invalid',
        )


class ProfileForm(forms.ModelForm):
    cpf = forms.CharField(
        required=False,
        label='cpf',
    )
    add_css_class(cpf, 'C-login_input')

    cep = forms.CharField(
        required=False,
        label='cep',
        validators=[validate_cep, ],
    )
    add_css_class(cep, 'C-login_input')

    adress = forms.CharField(
        required=False,
        label='endereço',
    )
    add_css_class(adress, 'C-login_input')

    number = forms.CharField(
        required=False,
        label='número',
    )
    add_css_class(number, 'C-login_input')

    city = forms.CharField(
        required=False,
        label='cidade',
    )
    add_css_class(city, 'C-login_input')

    uf = forms.CharField(
        required=False,
        label='estado',
    )
    add_css_class(uf, 'C-login_input')

    class Meta:
        model = Profile
        fields = [
            'cpf',
            'cep',
            'adress',
            'number',
            'city',
            'uf',
        ]

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]
        f_cpf = c2.validate(cpf)

        if len(cpf) <= 0 or cpf == '':
            raise ValidationError(
                ('Campo obrigatório'),
                code='required',
            )

        if not f_cpf.is_valid():
            raise ValidationError(
                ('CPF inválido'),
                code='invalid',
            )

        profile = Profile.objects.filter(cpf=f_cpf.formatted()).exists()

        if profile:
            raise ValidationError(
                ('CPF já cadastrado'),
                code='invalid',
            )

        return f_cpf.formatted()

    def clean_adress(self):
        adress = self.cleaned_data["adress"]
        length_validate(adress)
        return adress

    def clean_number(self):
        number = self.cleaned_data["number"]
        length_validate(number)
        return number

    def clean_city(self):
        city = self.cleaned_data["city"]
        length_validate(city)
        return city

    def clean_uf(self):
        uf = self.cleaned_data["uf"]
        length_validate(uf)
        return uf

    def clean_cep(self):
        cep = self.cleaned_data["cep"]
        length_validate(cep)
        return cep
