from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from user.models import Profile
from utils.browser import make_chrome_browser
from selenium.webdriver.common.by import By
from product.models import Action
from time import sleep
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
            is_staff=kwargs.get('is_staff', False),
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
    def make_login(self, create_user: bool = True, **kwargs) -> HttpResponse:
        '''
            Returns an HttpResponse and a new User object.
            Create the new user and make login

            kwargs opts: is_staff: bool, username: str, password: str
        '''

        # create the user
        user = None
        if create_user:
            user = self.create_user(
                with_profile=True,
                is_staff=kwargs.get('is_staff', False),
                username=kwargs.get('username', 'user'),
                )

        # make login
        response = self.client.post(
            reverse('dashboard:home'),
            {
                'user': kwargs.get('username', 'user'),
                'password': kwargs.get('password', 'password'),
            },
            follow=True,
        )
        return response, user


class StaticTestCaseWithLogin(StaticLiveServerTestCase):
    def wait(self, time: float) -> None:
        return sleep(time)

    def create_superuser(self) -> User:
        '''
            Create a new superuser Object.
        '''
        new_user = User.objects.create_superuser(
            username='username',
            email='user@email.com',
            password='password',
        )
        new_user.save()

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

    def setUp(self, *args, **kwargs) -> None:
        self.browser = make_chrome_browser()
        return super().setUp(*args, **kwargs)

    def tearDown(self, *args, **kwargs) -> None:
        self.browser.quit()
        return super().tearDown(*args, **kwargs)

    def make_login(self) -> None:
        # create a super user
        self.create_superuser()

        # make get request
        self.browser.get(self.live_server_url + reverse('dashboard:home'))

        # get the input username and password
        username = self.browser.find_element(By.XPATH, '//*[@id="id_user"]')
        username.send_keys('username')
        password = self.browser.find_element(By.XPATH,
                                             '//*[@id="id_password"]',
                                             )
        password.send_keys('password')
        form = self.browser.find_element(By.XPATH,
                                         '/html/body/main/section/form',
                                         )
        form.submit()

    def create_action(self) -> Action:
        """
            Create the bbas3 action.
            The login method is called with this method.
        """
        self.make_login()

        self.browser.get(
            self.live_server_url + reverse('admin:action_register')
            )

        # get the action code input
        code = self.browser.find_element(By.XPATH, '//*[@id="id_code"]')
        code.send_keys('bbas3')

        # get the action description input
        desc = self.browser.find_element(By.XPATH, '//*[@id="id_description"]')
        desc.send_keys('banco do brasil')

        # get the action cnpj input
        cnpj = self.browser.find_element(By.XPATH, '//*[@id="id_cnpj"]')
        cnpj.send_keys('00.000.000/0001-91')

        # get the form
        form = self.browser.find_element(
            By.XPATH, '/html/body/main/section[1]/form',
            )

        # register the action
        form.submit()
