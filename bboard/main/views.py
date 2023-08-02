from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView

from .forms import ChangeUserInfoForm
from .models import AdvUser


class IndexView(TemplateView):
    template_name = 'main/index.html'

class OtherView(TemplateView):
    def get_template_names(self):
        return [f"main/{self.kwargs['page']}.html"]

class BBLoginView(LoginView):
    template_name = 'auth/login.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'auth/profile.html'

class BBLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'auth/logout.html'

class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'auth/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('main:profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

class BBPasswordChangeView(
    SuccessMessageMixin,
    LoginRequiredMixin,
    PasswordChangeView
):
    template_name = 'auth/password_change.html'
    success_url = reverse_lazy('main:profile')
    success_message = 'Пароль пользователя изменен'