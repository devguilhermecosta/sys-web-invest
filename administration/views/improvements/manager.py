from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from .list import ImprovementsList
from ...forms.improvement import ImprovementManagerForm
from improvement.models import Improvement


class ImprovementMaganer(ImprovementsList):
    def get_improvement(self, id: int | str | None = None) -> Improvement | None:  # noqa: E501
        obj = None
        if id is not None:
            obj = get_object_or_404(Improvement,
                                    pk=id,
                                    )
        return obj

    def get(self, *args, **kwargs) -> HttpResponse:
        if not self.request.user.is_staff:
            raise Http404()

        obj = self.get_improvement(kwargs.get('id'))
        s = self.request.session.get('improvement-manager', None)
        form = ImprovementManagerForm(s, instance=obj)

        return render(
            self.request,
            'administration/pages/improvement_manager.html',
            context={
                'improvement': obj,
                'form': form,
                'button_submit_value': 'salvar',
                'back_to_page': reverse('admin:improvements_list'),
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        if not self.request.user.is_staff:
            raise Http404()

        pk = kwargs.get('id', None)
        obj = self.get_improvement(pk)

        if not obj:
            raise Http404()

        post = self.request.POST
        self.request.session['improvement-manager'] = post
        form = ImprovementManagerForm(post, instance=obj)

        if form.is_valid():
            form.save()

            messages.success(
                self.request,
                'alteração salva com sucesso',
            )

        return redirect(
            reverse('admin:improvements_manager', args=(pk,))
        )
