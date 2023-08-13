from .receive_profits import ReceiveProfits
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from product.models import UserAction, UserFII, ActionHistory, FiiHistory


class ReceiveProfitsEdit(ReceiveProfits):
    reverse_url_success_response: str
    reverse_url_invalid_form: str

    def get_history_or_404(self, id: int) -> ActionHistory | FiiHistory:
        history = get_object_or_404(
            self.history_model,
            pk=id,
        )
        if history.userproduct.user != self.request.user:
            raise Http404()

        return history

    def get(self, *args, **kwargs) -> HttpResponse:
        history = self.get_history_or_404(kwargs.get('id', None))

        session = self.request.session.get('profits-edit', None)

        if isinstance(self.user_product_model(), UserFII):
            form = self.profits_form(
                session,
                initial={
                    'userproduct': history.userproduct.id,
                    'date': str(history.date),
                    'unit_price': history.get_final_value(),
                    }
                )

        if isinstance(self.user_product_model(), UserAction):
            form = self.profits_form(
                session,
                initial={
                    'userproduct': history.userproduct.id,
                    'handler': history.handler,
                    'date': str(history.date),
                    'tax_and_irpf': abs(history.tax_and_irpf),
                    'unit_price': history.get_gross_value(),
                }
                )

        form.fields.get('userproduct').widget.choices = self.choices()

        return render(
            self.request,
            self.template_path,
            context={
                'form': form,
                'form_title': 'editar rendimento',
                'button_submit_value': 'salvar',
                'is_main_page': False,
                'back_to_page': reverse(self.reverse_url_back_to_page),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        pk = kwargs.get('id', None)
        history = self.get_history_or_404(id=pk)
        post = self.request.POST
        self.request.session['profits-edit'] = post
        form = self.profits_form(post)

        if form.is_valid():
            data = form.cleaned_data
            userproduct = self.get_product_or_404(data['userproduct'])
            data.update({'userproduct': userproduct})
            history.update(**data)

            del self.request.session['profits-edit']

            messages.success(
                self.request,
                'rendimento salvo com sucesso',
            )

            return redirect(
                reverse(self.reverse_url_success_response)
            )

        return redirect(
            reverse(
                self.reverse_url_invalid_form, args=(pk,)
                )
        )
