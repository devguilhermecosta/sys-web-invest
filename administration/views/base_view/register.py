from typing import Any, Dict
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from administration.forms import FIIRegisterForm, ActionRegisterForm
from product.models import FII, Action


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch',
)
class Register(TemplateView):
    model: FII | Action
    form: FIIRegisterForm | ActionRegisterForm
    form_title: str = ''
    template_name = 'administration/pages/product_register.html'
    success_message: str
    reverse_url_redirect_response: str

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        session = self.request.session.get('admin-register', None)
        form = self.form(session)
        products = self.model.objects.all().order_by('-id')

        context_data.update({
            'form': form,
            'form_title': self.form_title,
            'button_submit_value': 'registrar',
            'products': products,
            'default_message': 'nenhum produto cadastrado',
            'is_main_page': True,
        })

        return context_data

    def get(self, *args, **kwargs) -> HttpResponse:
        if not self.request.user.is_staff:
            return redirect(
                reverse('dashboard:user_dashboard')
            )
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['admin-register'] = post
        form = self.form(post)

        if form.is_valid():
            form.save()

            messages.success(
                self.request,
                self.success_message,
            )

            del self.request.session['admin-register']

            return redirect(
                reverse(self.reverse_url_redirect_response)
            )

        return redirect(
            reverse(self.reverse_url_redirect_response)
        )
