from django.http import HttpResponse, Http404
from django.shortcuts import render
from ..update import Update
from product.models import FixedIncomeHistory, DirectTreasureHistory


class History(Update):
    history_model: FixedIncomeHistory | DirectTreasureHistory
    fixed_income: bool | None = None
    direct_treasure: bool | None = None

    def get(self, *args, **kwargs) -> HttpResponse:
        product = self.get_product_or_404(kwargs.get('id', None))
        history = self.history_model.objects.filter(
            product=product
        ).order_by('-date')

        return render(
            self.request,
            self.template_path,
            context={
                'product': product,
                'history': history,
                'profits_payment': (
                    False if product.interest_receipt == 'não há' else True
                    ),
                'direct_treasure': True if self.direct_treasure else None,
                'fixed_income': True if self.fixed_income else None,
                'back_to_page': product.get_absolute_url(),
            }
        )

    def post(self, *args, **kwargs) -> None:
        raise Http404()
