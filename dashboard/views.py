from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from dashboard.forms.login_form import LoginForm
from user.models import Profile
from product.models import (
    UserAction,
    UserFII,
    ProductFixedIncome,
    DirectTreasure,
    )


class LoginView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        session = self.request.session.get('login', None)
        form = LoginForm(session)

        return render(
            self.request,
            'dashboard/pages/home.html',
            context={
                'form': form,
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        post = self.request.POST
        self.request.session['login'] = post
        form = LoginForm(post)

        if form.is_valid():
            user = authenticate(
                self.request,
                username=post.get('user'),
                password=post.get('password'),
                )

            if user is not None:
                del self.request.session['login']
                profile = Profile.objects.filter(user=user).exists()
                login(self.request, user)

                if not profile:
                    return redirect(
                        reverse('user:create_profile')
                        )

                messages.success(
                    self.request,
                    'login realizado com sucesso'
                )
                return redirect(
                    reverse('dashboard:user_dashboard')
                )

            messages.error(
                self.request,
                'Usuário ou senha incorretos',
            )
            return redirect(
                reverse('dashboard:home')
            )

        return redirect(
            reverse('dashboard:home')
        )


class LogoutView(View):
    def post(self, *args, **kwargs):
        logout(self.request)

        messages.warning(
            self.request,
            'Logout realizado com sucesso'
        )

        return redirect(
            reverse('dashboard:home')
        )


@method_decorator(
    login_required(
        redirect_field_name='next',
        login_url='/',
    ),
    name='dispatch'
)
class DashboardView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        user = self.request.user

        actions = UserAction.objects.filter(user=user)
        total_actions = sum(
            [action.get_current_value_invested() for action in actions]
            )
        profits_actions = UserAction.get_total_profits(user)
        actions_tax = UserAction.get_total_tax(user)

        fiis = UserFII.objects.filter(user=user)
        total_fiis = sum([fii.get_current_value_invested() for fii in fiis])
        profits_fiis = UserFII.get_total_profits(user)

        fixed_income = ProductFixedIncome.objects.filter(user=user)
        total_f_inc = sum([finc.get_current_value() for finc in fixed_income])
        profits_f_inc = ProductFixedIncome.get_total_profits(user)
        fixed_inc_tax = ProductFixedIncome.get_total_tax(user)

        direct_treasure = DirectTreasure.objects.filter(user=user)
        total_d_t = sum([dt.get_current_value() for dt in direct_treasure])
        profits_d_t = DirectTreasure.get_total_profits(user)
        direct_t_tax = DirectTreasure.get_total_tax(user)

        grand_total = total_actions + total_fiis + total_f_inc + total_d_t
        total_tax = actions_tax + fixed_inc_tax + direct_t_tax

        return render(
            self.request,
            'dashboard/pages/dashboard.html',
            context={
                'total_actions': total_actions,
                'total_fiis': total_fiis,
                'total_fixed_income': total_f_inc,
                'total_direct_treasure': total_d_t,
                'grand_total': grand_total,
                'profits_fiis': profits_fiis,
                'profits_actions': profits_actions,
                'profits_fixed_income': profits_f_inc,
                'profits_direct_treasue': profits_d_t,
                'total_tax': total_tax,
            }
        )


TODO = 'verificar se pode-se melhorar as consultas SQL'
