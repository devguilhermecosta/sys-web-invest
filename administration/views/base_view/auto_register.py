from .register import Register
from product.models import FII, Action
from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
import requests
import re


class AutoRegister(Register):
    def format_response(self, message: str) -> str:
        return re.sub(r"[\[\]'\"]", '', str(message))

    def get_api_data(self, data_api: list) -> dict[str]:
        stock = str(data_api['stock']).lower()
        name = str(data_api['name']).lower()
        logo = str(data_api['logo']).lower()
        return stock, name, logo

    def auto_register_fiis(self,
                           registered_objs: list[str | FII],
                           data_api: list,
                           ) -> HttpResponse:
        list_of_fiis = []
        tot = 0

        try:
            for data in data_api:
                code, name, logo = self.get_api_data(data)

                if code in registered_objs:
                    continue

                if 'fii' in name or 'fii' in logo:
                    FII.objects.create(
                        code=code,
                        description=name,
                    )
                    list_of_fiis.append(f'{code.upper()} - {name.capitalize()}')  # noqa: E501
                    tot += 1

            tags = ['fiis', 'registradas'] if tot > 1 else ['fii', 'registrada']  # noqa: E501
            formated_list = self.format_response(list_of_fiis)

            message_success = (
                f'{tot} {tags[0]} {tags[1]} com sucesso. FIIs registradas: '
                f'{formated_list}'
                )

            if tot == 0:
                message_success = 'nenhum novo FII à registrar'

            messages.success(
                self.request,
                message_success,
            )
        except Exception as error:
            message_error = f'Erro ao cadastras os FIIs: {error}'
            messages.error(
                self.request,
                message_error,
            )

        return redirect(
            reverse(self.reverse_url_redirect_response)
        )

    def auto_register_stocks(self,
                             registered_objs: list[str | Action],
                             data_api: list,
                             ) -> HttpResponse:
        list_of_stocks = []
        tot = 0

        try:
            for data in data_api:
                code, name, logo = self.get_api_data(data)

                # excludes the fracionary market
                if code in registered_objs or '3f' in code or '4f' in code:
                    continue

                # the api does not have groups to separate fii and stocks.
                # i tried to delete the fiis through the data provided
                # in the api
                if 'fii' in name or 'fii' in logo:
                    continue

                # register the stock without cnpj
                # because the api does not provide cnpj
                Action.objects.create(
                    code=code,
                    description=name,
                )
                list_of_stocks.append(f'{code.upper()} - {name.capitalize()}')
                tot += 1

            tags = ['ações', 'registradas'] if tot > 1 else ['ação', 'registrada']  # noqa: E501
            formated_list = self.format_response(list_of_stocks)

            message_success = (
                f'{tot} {tags[0]} {tags[1]} com sucesso. Ações registradas: '
                f'{formated_list}')

            if tot == 0:
                message_success = 'nenhuma nova ação à registrar'

            messages.success(
                self.request,
                message_success,
            )
        except Exception as error:
            message_error = f'Erro ao cadastras as ações: {error}'
            messages.error(
                self.request,
                message_error,
            )

        return redirect(
            reverse(self.reverse_url_redirect_response)
        )

    def get(self, *args, **kwargs) -> None:
        raise Http404()

    def post(self, *args, **kwargs) -> HttpResponse:
        codes = [obj.code for obj in self.model.objects.all()]
        request = requests.get('https://brapi.dev/api/quote/list')
        data = request.json()['stocks']

        if self.model == Action:
            return self.auto_register_stocks(codes, data)

        if self.model == FII:
            return self.auto_register_fiis(codes, data)
