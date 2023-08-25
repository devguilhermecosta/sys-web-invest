from ..buy import Buy
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from product.forms import FIIReceiptProfitsForm, ActionsReceivProfitsForm
from product.models import UserAction, UserFII


class ReceiveProfits(Buy):
    profits_form: ActionsReceivProfitsForm | FIIReceiptProfitsForm
    template_path: str
    form_custom_id: str
    reverse_url_history_profits: str
    reverse_url_receive_profits: str
    reverse_url_total_profits: str

    def get_product_or_404(self, id: int) -> UserAction | UserFII:
        userproduct = get_object_or_404(
            self.user_product_model,
            pk=id,
            user=self.request.user,
        )
        return userproduct

    def choices(self) -> tuple:
        choices = [('---', '---')]

        objects = self.user_product_model.objects.filter(
            user=self.request.user
        )

        for obj in objects:
            choices.append(
                (obj.id, obj.product.code.upper())
            )

        return choices

    def get(self, *args, **kwargs) -> HttpResponse:
        form = self.profits_form()
        form.fields.get('userproduct').widget.choices = self.choices()

        return render(
            self.request,
            self.template_path,
            context={
                'form': form,
                'form_title': 'lançar rendimento',
                'custom_id': self.form_custom_id,
                'button_submit_value': 'salvar',
                'url_history_profits': reverse(
                    self.reverse_url_history_profits,
                ),
                'url_receive_profits': reverse(
                    self.reverse_url_receive_profits,
                ),
                'url_total_profits': reverse(
                    self.reverse_url_total_profits,
                ),
                'is_main_page': True,
                'back_to_page': reverse(self.reverse_url_back_to_page),
                'data_profits': 'profits',
            }
        )

    def post(self, *args, **kwargs) -> JsonResponse:
        post = self.request.POST
        form = self.profits_form(post)

        if form.is_valid():
            data = form.cleaned_data
            userproduct = self.get_product_or_404(data['userproduct'])
            data.pop('userproduct')
            userproduct.receive_profits(**data)

            return JsonResponse({'data': 'success request'})

        return JsonResponse({'error': 'form errors'})
