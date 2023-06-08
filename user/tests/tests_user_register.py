from django.test import TestCase
from django.test import Client
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core import mail
from user import views


class UserRegisterTests(TestCase):

    def setUp(self) -> None:
        self.url: str = reverse('user:register')
        self.c = Client()
        self.user_data = {
            'first_name': 'jhon',
            'last_name': 'dhoe',
            'username': 'jhondoe',
            'email': 'jhon@email.com',
            'email_repeat': 'jhon@email.com',
            'password': 'Jhon1234',
            'password_repeat': 'Jhon1234',
        }
        return super().setUp()

    def test_url_user_register_is_correct(self) -> None:
        self.assertEqual(self.url, '/usuario/registrar/')

    def test_user_register_load_correct_view(self) -> None:
        response = self.client.get(self.url)
        self.assertEqual(
            response.resolver_match.func.view_class,
            views.UserRegister
            )

    def test_user_register_load_correct_template(self) -> None:
        response: HttpResponse = self.client.get(self.url)
        self.assertTemplateUsed(response, 'user/pages/register.html')

    def test_user_register_status_code_200(self) -> None:
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_user_register_create_a_new_user_if_form_data_is_valid(self) -> None:  # noqa: E501
        response: HttpResponse = self.c.post(
            self.url,
            {**self.user_data},
            follow=True,
        )
        content = response.content.decode('utf-8')
        url_to_redirect = response.redirect_chain[0][0]
        status_code_redirect = response.redirect_chain[0][1]

        self.assertIn(
            (
                f'Prezado(a) {self.user_data["first_name"].capitalize()}. '
                'Um email de confirmação foi enviado para '
                'jhon@email.com. Acesse o link para ativar sua conta. Caso '
                'não tenha recebido o email, verifique sua caixa de spam.'
            ),
            content,
        )
        self.assertEqual(len(User.objects.all()), 1)
        self.assertEqual(
            url_to_redirect,
            '/usuario/registrar/register_confirmation/',
            )
        self.assertEqual(status_code_redirect, 302)

    def test_user_register_sends_a_confirmation_mail_if_user_is_created(self) -> None:  # noqa: E501
        # 1) Create a new user
        self.c.post(
            self.url,
            {**self.user_data},
            follow=True,
        )

        # 2) Get the mail confirmation
        mail_confirmation = mail.outbox
        mail_body = mail_confirmation[0].body

        self.assertEqual(len(mail_confirmation), 1)
        self.assertEqual(mail_confirmation[0].subject, 'Ativação de conta')
        self.assertIn(
            f'Olá {self.user_data["first_name"].capitalize()}',
            mail_body,
            )
        self.assertIn(
            'Por favor, acesse o link abaixo para ativar sua conta.',
            mail_body,
        )
        self.assertIn(
            'http://testserver/usuario/activate/',
            mail_body,
        )

    def test_user_register_not_receives_confirmation_mail_if_form_register_is_not_valid(self) -> None:  # noqa: E501
        self.user_data['email'] = ''
        response = self.c.post(
            self.url,
            {**self.user_data},
            follow=True,
        )
        form = response.context['form']
        mail_confirmation = mail.outbox

        self.assertEqual(len(mail_confirmation), 0)
        self.assertFalse(form.is_valid())

    def test_user_register_the_new_user_is_initially_disabled(self) -> None:
        self.c.post(
            self.url,
            {**self.user_data},
            follow=True,
        )
        user = User.objects.first()

        self.assertFalse(user.is_active)

    def test_user_register_is_activate_after_click_on_the_actvation_link(self) -> None:  # noqa: E501
        '''
        This tests the entire account creation and activation process.
        '''

        # 1) Create the account and send the activation email
        self.c.post(
            self.url,
            {**self.user_data},
            follow=True,
        )

        # 2) Get the uid and token sent in the email
        send_email = mail.outbox
        uid = send_email[0].body[104:106]
        token = send_email[0].body[107:-2]

        # 3) At this momento the user is inactive
        user_before_activation = User.objects.first()
        self.assertFalse(user_before_activation.is_active)

        # 4) Make get request for 'user:activate' using uid and token
        request_user_activation = self.c.get(
            reverse(
                'user:activate',
                kwargs={
                    'uidb64': uid,
                    'token': token
                }),
            follow=True,
        )

        # 5) Now the user is active
        user_after_activation = User.objects.first()
        self.assertTrue(user_after_activation.is_active)

        # 6) An activation message is rendered
        self.assertIn(
            ('Obrigado por confirmar seu e-mail. '
             'Agora você pode fazer login em sua conta.'),
            request_user_activation.content.decode('utf-8')
        )

    def test_user_register_returns_an_error_message_if_the_activation_link_has_already_been_used(self) -> None:  # noqa: E501
        # 1) Create the account and send the activation email
        self.c.post(
            self.url,
            {**self.user_data},
            follow=True,
        )

        # 2) Get the uid and token sent in the email
        send_email = mail.outbox
        uid = send_email[0].body[104:106]
        token = send_email[0].body[107:-2]

        # 3) Make get request for 'user:activate' using uid and token
        self.c.get(
            reverse(
                'user:activate',
                kwargs={
                    'uidb64': uid,
                    'token': token
                }),
            follow=True,
        )

        # 4) Make get request again for 'user:activate'
        new_request_with_same_url = self.c.get(
            reverse(
                'user:activate',
                kwargs={
                    'uidb64': uid,
                    'token': token
                }),
            follow=True,
        )

        # 5) Now we have a error message
        self.assertIn(
            'Este link de ativação é inválido',
            new_request_with_same_url.content.decode('utf-8')
        )

        # 6) The user is redirected to the home page
        self.assertRedirects(new_request_with_same_url,
                             expected_url='/',
                             status_code=302,
                             )
