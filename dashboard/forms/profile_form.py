from django import forms
from dashboard.models import Profile
from utils.forms.style import add_css_class


class ProfileForm(forms.ModelForm):
    cpf = forms.CharField(
        label='cpf',
    )
    add_css_class(cpf, 'C-login_input')

    adress = forms.CharField(
        label='endereço',
    )
    add_css_class(adress, 'C-login_input')

    number = forms.CharField(
        label='número',
    )
    add_css_class(number, 'C-login_input')

    city = forms.CharField(
        label='cidade',
    )
    add_css_class(city, 'C-login_input')

    uf = forms.CharField(
        label='estado',
    )
    add_css_class(uf, 'C-login_input')

    cep = forms.CharField(
        label='cep',
    )
    add_css_class(cep, 'C-login_input')

    class Meta:
        model = Profile
        fields = [
            'cpf',
            'adress',
            'number',
            'city',
            'uf',
            'cep',
        ]
