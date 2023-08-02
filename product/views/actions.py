from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.forms import ActionBuyAndSellForm, ActionsReceivProfitsForm
from product.models import Action, UserAction, ActionHistory
from .base_views.variable_income import Buy, Sell, History


login_url = '/'


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url=login_url,
    ),
    name='dispatch',
)
class ActionsView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        return render(
            self.request,
            'product/pages/actions/actions.html',
        )


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url=login_url,
    ),
    name='dispatch',
)
class AllActionsView(ListView):
    model = UserAction
    template_name = 'product/pages/actions/actions_list.html'
    ordering = ['-id']
    context_object_name = 'actions'

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset(*args, **kwargs)
        user = self.request.user
        query_set = query_set.filter(user=user)

        return query_set


class ActionsBuyView(Buy):
    success_response_url_redirect = 'product:actions'
    error_response_url_redirect = 'product:actions_buy'
    form = ActionBuyAndSellForm
    template_get_request = 'product/pages/actions/actions_buy.html'
    product_model = Action
    user_product_model = UserAction
    history_model = ActionHistory


class ActionsSellView(Sell):
    success_response_url_redirect = 'product:actions'
    error_response_url_redirect = 'product:actions_sell'
    form = ActionBuyAndSellForm
    template_get_request = 'product/pages/actions/actions_sell.html'
    product_model = Action
    user_product_model = UserAction


class ActionHistoryDetails(History):
    template_to_render_response = 'product/partials/_history_variable_income.html'  # noqa: E501
    product_model = Action
    user_product_model = UserAction
    history_model = ActionHistory


class ActionsManageProfitsView(ActionsView):
    def choices(self) -> tuple:
        choices = [('---', '---')]

        objects = UserAction.objects.filter(
            user=self.request.user
        )

        for user_action in objects:
            choices.append(
                (user_action.id, user_action.product.code.upper())
            )

        return choices

    def get(self, *args, **kwargs) -> HttpResponse:
        form = ActionsReceivProfitsForm()
        form.fields.get('user_product_id').widget.choices = self.choices()

        return render(
            self.request,
            'product/pages/actions/actions_profits.html',
            context={
                'form': form,
                'form_title': 'lançar rendimento',
                'custom_id': 'actions-receive-profits-form',
                'button_submit_value': 'salvar',
                'url_history_profits': reverse(
                    'product:action_history_json'
                ),
                'url_receive_profits': reverse(
                    'product:actions_manage_profits',
                ),
                'is_main_page': True,
            }
        )

    def post(self, *args, **kwargs) -> JsonResponse:
        post = self.request.POST
        form = ActionsReceivProfitsForm(post)

        if form.is_valid():
            data = form.cleaned_data

            user_action = get_object_or_404(
                UserAction,
                pk=data['user_product_id'],
            )

            if user_action.user != self.request.user:
                raise Http404()

            user_action.receiv_profits(
                handler=data['profits_type'],
                date=data['date'],
                total_price=data['total_price'],
                tax_and_irpf=data.get('tax_and_irpf', ''),
            )

            return JsonResponse({'data': 'success request'})

        return JsonResponse({'error': 'form errors'})


class ActionsManageProfitsHistoryView(ActionsView):
    def get(self, *args, **kwargs) -> JsonResponse:
        history = UserAction.get_full_profits_history(
            user=self.request.user
        )
        return JsonResponse({'data': history})

    def post(self, *args, **kwargs) -> None:
        raise Http404()


class ActionsManageProfitsHistoryDeleteView(ActionsView):
    def get(self, *args, **kwargs) -> None:
        raise Http404()

    def post(self, *args, **kwargs) -> HttpResponse:
        history = get_object_or_404(
            ActionHistory,
            pk=kwargs.get('id', None)
        )

        if history.userproduct.user != self.request.user:
            raise Http404()

        history.delete()

        return redirect(
            reverse('product:actions_manage_profits')
        )


class ActionsManageProfitsHistoryEditView(ActionsManageProfitsView):
    def get_product_history_or_404(self, id: int) -> ActionHistory:
        history = get_object_or_404(
            ActionHistory,
            pk=id
        )

        if history.userproduct.user != self.request.user:
            raise Http404()

        return history

    def get(self, *args, **kwargs) -> HttpResponse:
        history = self.get_product_history_or_404(kwargs.get('id', None))
        session = self.request.session.get('actions-profits-edit', None)
        tax = history.tax_and_irpf
        form = ActionsReceivProfitsForm(
            session,
            initial={
                'user_product_id': history.userproduct.id,
                'profits_type': history.handler,
                'date': history.date,
                'tax_and_irpf': f'{tax:.2f}' if tax else '',
                'total_price': f'{history.total_price:.2f}',
            }
            )
        form.fields.get('user_product_id').widget.choices = self.choices()

        return render(
            self.request,
            'product/pages/actions/actions_profits.html',
            context={
                'form': form,
                'form_title': 'editar rendimento',
                'custom_id': 'actions-receive-profits-edit-form',
                'button_submit_value': 'salvar',
                'is_main_page': False,
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        history = self.get_product_history_or_404(kwargs.get('id', None))
        post = self.request.POST
        self.request.session['actions-profits-edit'] = post
        form = ActionsReceivProfitsForm(post)

        if form.is_valid():
            data = form.cleaned_data
            tax = data['tax_and_irpf'] if data['tax_and_irpf'] != 0 else ''
            user_action = UserAction.objects.get(pk=data['user_product_id'])

            history.userproduct = user_action
            history.handler = data['profits_type']
            history.date = data['date']
            history.tax_and_irpf = tax
            history.total_price = data['total_price']

            history.save()

            messages.success(
                self.request,
                'rendimento salvo com sucesso'
            )

            del self.request.session['actions-profits-edit']

            return redirect(
                reverse('product:actions_manage_profits'),
            )

        return redirect(
            reverse('product:action_manage_profits_edit', args=(history.id,))
        )
