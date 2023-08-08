from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.core.exceptions import ValidationError
from product.models import DirectTreasure, DirectTreasureHistory
from product.views.base_views.fixed_income import (
    FixedIncomeBaseView,
    Register,
    Update,
    Delete,
    Details,
    )
from product.forms.direct_treasure import (
    DirectTreasureRegisterForm,
    DirectTreasureEditForm,
    DirectTreasureHistoryForm,
    )
from product.forms.fixed_income import (
    FixedIncomeApplyRedeemForm,
    FixedIncomeProfitsReceivForm,
    )


class DirectTreasureView(FixedIncomeBaseView):
    model = DirectTreasure
    template_title = 'tesouro direto'
    template_path = 'product/partials/_dt_and_fi_intro.html'
    reverse_url_register = 'product:direct_treasure_register'
    reverse_url_back_to_page = 'dashboard:user_dashboard'


class DirectTreasureRegisterView(Register):
    model = DirectTreasure
    form = DirectTreasureRegisterForm
    template_path = 'product/partials/_dt_and_fi_register.html'
    reverse_url_back_to_page = 'product:direct_treasure'
    reverse_url_if_form_invalid = 'product:direct_treasure_register'


class DirectTreasureEditView(Update):
    model = DirectTreasure
    form = DirectTreasureEditForm
    template_path = 'product/partials/_dt_and_fi_edit.html'


class DirectTreasureDeleteView(Delete):
    model = DirectTreasure
    reverse_url_redirect = 'product:direct_treasure'


class DirectTreasureDetailsView(Details):
    model = DirectTreasure
    template_path = 'product/partials/_dt_and_fi_details.html'
    reverse_url_back_to_page = 'product:direct_treasure'
    reverse_url_edit = 'product:direct_treasure_edit'
    reverse_url_history = 'product:direct_treasure_history'
    reverse_url_delete = 'product:direct_treasure_delete'
    reverse_url_profits = 'product:direct_treasure_profits_receipt'
    reverse_url_apply = 'product:direct_treasure_apply'
    reverse_url_redeem = 'product:direct_treasure_redeem'


class DirectTreasureApplyView(DirectTreasureEditView):
    def redirect_response(self, product_id: int) -> HttpResponse:
        return redirect(
            reverse('product:direct_treasure_details', args=(product_id,)),
        )

    def get(self, *args, **kwargs) -> None:
        raise Http404()

    def post(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(id=kwargs.get('id', None))
        post = self.request.POST
        self.request.session['direct-treasure-apply-h'] = post
        form = FixedIncomeApplyRedeemForm(post)

        if form.is_valid():
            data = form.cleaned_data
            product.apply(
                date=data['date'],
                value=data['value'],
            )

            del self.request.session['direct-treasure-apply-h']

            messages.success(
                self.request,
                'Aplicação realizada com sucesso'
            )

        return self.redirect_response(product.id)


class DirectTreasureRedeemView(DirectTreasureApplyView):
    def post(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(id=kwargs.get('id', None))
        post = self.request.POST
        self.request.session['direct-treasure-redeem-h'] = post
        form = FixedIncomeApplyRedeemForm(post)

        if form.is_valid():
            data = form.cleaned_data
            try:
                product.redeem(
                    date=data['date'],
                    value=data['value'],
                )
            except ValidationError:
                messages.error(
                    self.request,
                    'Saldo insuficiente para resgate',
                )

                return self.redirect_response(product.id)

            del self.request.session['direct-treasure-redeem-h']
            messages.success(
                self.request,
                'Resgate realizado com sucesso',
            )

        return self.redirect_response(product.id)


class DirectTreasureProfitsReceiptView(DirectTreasureView):
    def get_product_or_404(self, id: int) -> DirectTreasure:
        product = get_object_or_404(
            DirectTreasure,
            pk=id,
            user=self.request.user,
        )
        return product

    def get(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(kwargs.get('id', None))
        session = self.request.session.get(
            'direct-treasure-profits-receive',
            None,
            )
        form = FixedIncomeProfitsReceivForm(session)

        return render(
            self.request,
            'product/partials/_dt_and_fi_profits_receipt.html',
            context={
                'form': form,
                'form_title': product.name.upper(),
                'button_submit_value': 'receber',
                'back_to_page': reverse(
                    'product:direct_treasure_details',
                    args=(product.id,)
                    ),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(kwargs.get('id', None))
        post = self.request.POST
        self.request.session['direct-treasure-profits-receive'] = post
        form = FixedIncomeProfitsReceivForm(post)

        if form.is_valid():
            data = form.cleaned_data
            product.receive_profits(**data)

            del self.request.session['direct-treasure-profits-receive']

            messages.success(
                self.request,
                'Recebimento de juros salvo com sucesso',
            )

            return redirect(
                reverse('product:direct_treasure_details', args=(product.id,))
            )

        return redirect(
            reverse(
                'product:direct_treasure_profits_receipt',
                args=(product.id,),
                )
        )


class DirectTreasureHistoryView(DirectTreasureEditView):
    def get(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(id=kwargs.get('id', None))
        history = DirectTreasureHistory.objects.filter(
            product=product,
            ).order_by('-date')

        return render(
            self.request,
            'product/partials/_history_dt_and_fi.html',
            context={
                'product': product,
                'history': history,
                'direct_treasure': True,
                'profits_payment': (
                    True if product.interest_receipt != 'não há' else False
                    ),
                'back_to_page': reverse(
                    'product:direct_treasure_details',
                    args=(product.id,),
                    ),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        return Http404()


class DirectTreasureHistoryEditView(DirectTreasureEditView):
    def get_history_or_404(self, id: int) -> DirectTreasureHistory:
        history = get_object_or_404(
            DirectTreasureHistory,
            pk=id,
        )
        if history.product.user != self.request.user:
            raise Http404()

        return history

    def choices(self, history: DirectTreasureHistory) -> list:
        choices = [
            ('apply', 'aplicação'),
            ('redeem', 'resgate'),
        ]

        if history.product.interest_receipt != 'não há':
            choices.append(
                ('profits', 'recebimento de juros')
            )
        return choices

    def get(self, *args, **kwargs) -> HttpResponse:
        history = self.get_history_or_404(kwargs.get('history_id', None))
        history.tax_and_irpf = abs(history.tax_and_irpf)
        history.value = abs(history.value)

        session = self.request.session.get(
            'direct-treasure-history-edit',
            None,
            )
        form = DirectTreasureHistoryForm(
            session,
            instance=history,
            )
        form.fields['state'].widget.choices = self.choices(history)

        return render(
            self.request,
            'product/partials/_dt_and_fi_history_edit.html',
            context={
                'form': form,
                'button_submit_value': 'salvar',
                'back_to_page': reverse(
                    'product:direct_treasure_history',
                    args=(history.product.id,),
                    ),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        history = self.get_history_or_404(kwargs.get('history_id', None))
        post = self.request.POST
        self.request.session['direct-treasure-history-edit'] = post
        form = DirectTreasureHistoryForm(post)

        if form.is_valid():
            data = form.cleaned_data
            history.update(**data)

            messages.success(
                self.request,
                'histórico salvo com sucesso',
            )

            del self.request.session['direct-treasure-history-edit']

            return redirect(
                reverse('product:direct_treasure_history',
                        args=(history.product.id,),
                        )
            )

        return redirect(
            reverse(
                'product:direct_treasure_history_edit',
                kwargs={
                    'history_id': history.id,
                    'product_id': history.product.id,
                }
            )
        )


class DirectTreasureHistoryDeleteView(DirectTreasureHistoryEditView):
    def get(self, *args, **kwargs) -> None:
        raise Http404()

    def post(self, *args, **kwargs) -> HttpResponse:
        history = self.get_history_or_404(kwargs.get('history_id', None))
        history.delete()

        messages.success(
            self.request,
            'histórico deletado com sucesso',
        )

        return redirect(
            reverse(
                'product:direct_treasure_history',
                args=(history.product.id,),
                )
        )
