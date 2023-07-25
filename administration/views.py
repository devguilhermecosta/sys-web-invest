from typing import Any, Dict
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from administration.forms import FIIRegisterForm


class FIIRegister(TemplateView):
    template_name = 'administration/pages/product_register.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        session = self.request.session.get('fii-admin-register', None)
        form = FIIRegisterForm(session)

        context_data.update({
            'form': form,
            'form_title': 'Registrar novo FII',
            'button_submit_value': 'registrar',
        })

        return context_data

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['fii-admin-register'] = post
        form = FIIRegisterForm(post)

        if form.is_valid():
            form.save()

            messages.success(
                self.request,
                'FII criado com sucesso',
            )

            del self.request.session['fii-admin-register']

            return redirect(
                reverse('admin:fii_register')
            )

        return redirect(
            reverse('admin:fii_register')
        )
