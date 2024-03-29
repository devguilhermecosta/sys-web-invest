from django.views import View
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Improvement


@method_decorator(
    login_required(redirect_field_name='next', login_url='/'),
    name='dispatch',
)
class ImprovementList(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        improvements = Improvement.objects.filter(
            user=self.request.user
            ).order_by('-id')

        return render(
            self.request,
            'improvement/pages/improvements.html',
            context={
                'improvements': improvements,
                'back_to_page': reverse('dashboard:user_dashboard'),
            }
        )


class ImprovementCreate(ImprovementList):
    def get(self, *args, **kwargs) -> None:
        raise Http404()

    def post(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user
        data = self.request.POST
        subject = data.get('subject')
        user_message = data.get('content')

        if subject and user_message:
            message = render_to_string(
                'improvement/pages/mail_message.html',
                {
                    'user_full_name': user.first_name + ' ' + user.last_name,
                    'username': user.username,
                    'user_email': user.email,
                    'ticket_name': subject,
                    'ticket_description': user_message,
                }
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=True,
            )

            new_task = Improvement.objects.create(
                user=user,
                title=subject,
                description=user_message,
                status='enviado',
            )
            new_task.save()

            messages.success(
                self.request,
                'Solicitação enviada com sucesso.'
            )

            return redirect(
                reverse('improvement:list')
            )

        messages.error(
            self.request,
            'preencha todos os campos do formulário'
        )

        return redirect(
            reverse('dashboard:user_dashboard')
        )
