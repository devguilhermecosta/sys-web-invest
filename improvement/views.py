from django.views import View
from django.http import Http404, HttpResponse
from django.core.mail import send_mail


class SendEmailView(View):
    def get(self, *args, **kwargs) -> None:
        raise Http404()

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        print(post)
        return HttpResponse('este é o content')
