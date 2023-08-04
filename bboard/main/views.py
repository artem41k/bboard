from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import TemplateView

from .forms import ChangeUserInfoForm, RegisterUserForm
from .models import AdvUser
from .utilities import signer


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

class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'auth/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:register_done')

class RegisterDoneView(TemplateView):
    template_name = 'auth/register_done.html'

class ActivateUserView(TemplateView):
    def get_template_names(self):
        try:
            username = signer.unsign(self.kwargs['sign'])
        except BadSignature:
            return ['auth/bad_signature.html']
        
        user = get_object_or_404(AdvUser, username=username)
        if user.is_activated:
            return ['auth/user_is_activated.html']
        else:
            user.is_active = True
            user.is_activated = True
            user.save()
            return ['auth/activation_done.html']