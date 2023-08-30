from django.conf import settings  # noqa: F401
from django.core.mail import send_mail
from administration import views


def update():
    updater = views.ActionsUpdateLastCloseView()
    up = updater.update_all()
    subject = 'Atualização da última cotação de ações'
    message = up.get('message_f', '')
    fr = settings.EMAIL_HOST_USER
    to = [settings.EMAIL_HOST_USER]
    send_mail(subject, message, fr, to)


# criar também a task para os fiis
