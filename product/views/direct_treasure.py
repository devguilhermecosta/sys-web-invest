from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from product.models import DirectTreasure, DirectTreasureHistory
from product.forms.direct_treasure import (
    DirectTreasureRegisterForm,
    DirectTreasureEditForm,
    DirectTreasureHistoryForm,
    )

from product.forms.fixed_income import (
    FixedIncomeApplyRedeemForm,
    FixedIncomeProfitsReceivForm,
    )
from datetime import date as dt


@method_decorator(
    login_required(redirect_field_name='next',
                   login_url='/',
                   ),
    name='dispatch',
)
class DirectTreasureView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user
        products = DirectTreasure.objects.filter(
            user=user,
        )

        return render(
            self.request,
            'product/pages/direct_treasure/direct_treasure.html',
            context={
                'products': products,
                'back_to_page': reverse('dashboard:user_dashboard'),
                'total_applied': DirectTreasure.get_total_amount_invested(
                    user=self.request.user,
                ),
                'total_received_in_profits': DirectTreasure.get_total_profits(
                    user=self.request.user,
                ),
                'total_tax': DirectTreasure.get_total_tax(
                    user=self.request.user,
                ),
            }
        )


class DirectTreasureRegisterView(DirectTreasureView):
    date = dt.today().strftime('%Y-%m-%d')

    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('direct-treasure-apply', None)
        form = DirectTreasureRegisterForm(session)

        return render(
            self.request,
            'product/pages/direct_treasure/register.html',
            context={
                'form': form,
                'button_submit_value': 'investir',
                'back_to_page': reverse('product:direct_treasure'),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['direct-treasure-apply'] = post
        form = DirectTreasureRegisterForm(post)

        if form.is_valid():
            data = form.cleaned_data

            new_object = DirectTreasure.objects.create(
                user=self.request.user,
                name=data['name'],
                category=data['category'],
                interest_receipt=data['interest_receipt'],
                profitability=data['profitability'],
                maturity_date=data['maturity_date'],
                description=data['description'],
            )
            new_object.save()
            new_object.apply(data['date'], data['value'])

            del self.request.session['direct-treasure-apply']

            messages.success(
                self.request,
                'Aplicação criada com sucesso',
            )

            return redirect(
                reverse('product:direct_treasure'),
            )

        return redirect(
            reverse('product:direct_treasure_register'),
        )


class DirectTreasureEditView(DirectTreasureView):
    def get_product_or_404(self, id: int = None) -> DirectTreasure:
        product = None
        if id is not None:
            product = get_object_or_404(
                DirectTreasure,
                user=self.request.user,
                pk=id,
            )
        return product

    def get(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(kwargs.get('id', None))
        session = self.request.session.get('direct-treasure-edit', None)
        form = DirectTreasureEditForm(
            session,
            instance=product,
            )

        return render(
            self.request,
            'product/pages/direct_treasure/edit.html',
            context={
                'form': form,
                'button_submit_value': 'salvar',
                'back_to_page': reverse(
                    'product:direct_treasure_details',
                    args=(product.id,)
                    ),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        obj = self.get_product_or_404(kwargs.get('id', None))
        post = self.request.POST
        self.request.session['direct-treasure-edit'] = post
        form = DirectTreasureEditForm(
            post,
            instance=obj,
        )

        if form.is_valid():
            product = form.save(commit=False)
            product.user = self.request.user
            product.save()

            del self.request.session['direct-treasure-edit']

            messages.success(
                self.request,
                'Salvo com sucesso',
            )

            return redirect(
                reverse('product:direct_treasure_details', args=(obj.id,))
            )

        return redirect(
            reverse('product:direct_treasure_edit', args=(obj.id,))
        )


class DirectTreasureDetailsView(DirectTreasureView):
    def get(self, *args, **kwargs) -> HttpResponse:
        product = get_object_or_404(
            DirectTreasure,
            user=self.request.user,
            pk=kwargs.get('id', None),
        )
        s_apply = self.request.session.get('direct-treasure-apply-h', None)
        form_apply = FixedIncomeApplyRedeemForm(s_apply)

        s_redeem = self.request.session.get('direct-treasure-redeem-h', None)
        form_redeem = FixedIncomeApplyRedeemForm(s_redeem)

        return render(
            self.request,
            'product/partials/_dt_and_fi_details.html',
            context={
                'product': product,
                'form_apply': form_apply,
                'form_redeem': form_redeem,
                'url_edit': reverse(
                    'product:direct_treasure_edit',
                    args=(product.id,),
                    ),
                'url_history': reverse(
                    'product:direct_treasure_history',
                    args=(product.id,),
                    ),
                'url_delete': '',
                'url_profits': reverse(
                    'product:direct_treasure_profits_receipt',
                    args=(product.id,),
                    ),
                'url_apply': reverse(
                    'product:direct_treasure_apply', args=(product.id,)
                    ),
                'url_redeem': reverse(
                    'product:direct_treasure_redeem', args=(product.id,)
                    ),
                'profits_payment': (
                    True if product.interest_receipt != 'não há' else False
                ),
                'back_to_page': reverse('product:direct_treasure'),
            }
        )


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
