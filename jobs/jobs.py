from django.conf import settings
from django.core.mail import send_mail
from administration import views


def update_stocks():
    updater = views.ActionsUpdateLastCloseView()
    up = updater.update_all()

    subject = 'Atualização do valor do último fechamento - Ações'
    message = up.get('message_f', '')
    fr = settings.EMAIL_HOST_USER
    to = [settings.EMAIL_HOST_USER]
    send_mail(subject, message, fr, to)
    print('email enviado')


def update_fiis():
    updater = views.FIIsUpdateLastCloseView()
    up = updater.update_all()

    subject = 'Atualização do valor do último fechamento - FIIs'
    message = up.get('message_f', '')
    fr = settings.EMAIL_HOST_USER
    to = [settings.EMAIL_HOST_USER]
    send_mail(subject, message, fr, to)
