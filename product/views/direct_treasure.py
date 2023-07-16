from django.views import View
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from product.models import DirectTreasure
from product.forms.direct_treasure import (
    DirectTreasureRegisterForm,
    DirectTreasureEditForm,
    )
from product.forms.fixed_income import FixedIncomeApplyRedeemForm
from django.contrib import messages


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
            }
        )


class DirectTreasureRegisterView(DirectTreasureView):
    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('direct-treasure-apply', None)
        form = DirectTreasureRegisterForm(session)

        return render(
            self.request,
            'product/pages/direct_treasure/register.html',
            context={
                'form': form,
                'button_submit_value': 'investir',
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['direct-treasure-apply'] = post
        form = DirectTreasureRegisterForm(post)

        if form.is_valid():
            data = form.cleaned_data
            user = self.request.user

            new_object = DirectTreasure.objects.create(
                user=user,
                **data,
            )
            new_object.save()

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
    def get_product(self, id: int = None) -> DirectTreasure:
        product = None
        if id is not None:
            product = get_object_or_404(
                DirectTreasure,
                user=self.request.user,
                pk=id,
            )
        return product

    def get(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product(kwargs.get('id', None))
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
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        obj = self.get_product(kwargs.get('id', None))
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

        return render(
            self.request,
            'product/pages/direct_treasure/details.html',
            context={
                'product': product,
            }
        )


class DirectTreasureApplyView(DirectTreasureView):
    ...


class DirectTreasureRedeemView(DirectTreasureView):
    ...
