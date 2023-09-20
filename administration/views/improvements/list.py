from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View
from improvement.models import Improvement


@method_decorator(
    login_required(redirect_field_name='next', login_url='/'),
    name='dispatch',
)
class ImprovementsList(View):
    def get(self, *args, **kwrags) -> HttpResponse:
        if not self.request.user.is_staff:
            raise Http404()

        improvements = Improvement.objects.all().order_by("-id")

        return render(
            self.request,
            'administration/pages/improvements_list.html',
            context={
                'improvements': improvements,
                'back_to_page': reverse('dashboard:user_dashboard'),
            }
        )
