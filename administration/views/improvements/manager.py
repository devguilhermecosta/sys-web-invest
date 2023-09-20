from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
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
        form = ImprovementManagerForm(instance=obj)

        return render(
            self.request,
            'administration/pages/improvement_manager.html',
            context={
                'improvement': obj,
                'form': form,
                'button_submit_value': 'salvar',
            }
        )
