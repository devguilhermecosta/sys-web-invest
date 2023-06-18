from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse
from user.models import Profile
import c2validator as c2


class UserNotFoundError(BaseException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class UserMixin:
    def create_user(self, with_profile: bool = False, **kwargs) -> User:
        '''
            Create a new user Object.
            If with_profile attribute == True, returns a new user with
            profile.
            The user has this attributes:
            username='user', email='user@email.com', password='password'.

            optional kwargs = with_profile, username, email.
        '''
        new_user = User.objects.create_user(
            username=kwargs.pop('username', 'user'),
            email=kwargs.pop('email', 'user@email.com'),
            password='password',
        )
        new_user.save()

        if with_profile:
            profile = Profile.objects.create(
                user=new_user,
                cpf=c2.create_cpf(),
                adress='street 11',
                number='11',
                city='new york',
                uf='ny',
                cep='00000000'
            )
            profile.save()

        return new_user

    def get_user(self, username: str) -> User:
        """
            Returns the User object.

            raise: UserNotFoundError
        """
        user = User.objects.filter(username=username).first()
        if not user:
            raise UserNotFoundError(
                'Usuário não encontrado'
            )
        return user


class TestCaseWithLogin(UserMixin, TestCase):
    def make_login(self) -> HttpResponse:
        ''' We will create the new user and make login '''
        # create the user
        self.create_user(with_profile=True)

        # make login
        response = self.client.post(
            reverse('dashboard:home'),
            {
                'user': 'user',
                'password': 'password',
            },
            follow=True,
        )
        return response
