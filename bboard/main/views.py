from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetView,
    PasswordResetDoneView,  PasswordResetConfirmView,
    PasswordResetCompleteView)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import (
    UpdateView, CreateView, DeleteView, FormMixin
)
from django.views.generic.list import ListView

from .forms import ChangeUserInfoForm, RegisterUserForm, SearchForm
from .models import AdvUser, Bb, SubRubric
from .utilities import signer


class IndexView(TemplateView):
    template_name = 'main/index.html'


class OtherView(TemplateView):
    def get_template_names(self):
        return [f"main/{self.kwargs['page']}.html"]

# Auth & Profile Views


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


class BBPasswordResetView(PasswordResetView):
    template_name = "auth/password_reset.html"
    email_template_name = "email/password_reset.html"
    subject_template_name = "email/password_reset_subject.txt"
    success_url = reverse_lazy('main:password_reset_done')


class BBPasswordResetDoneView(PasswordResetDoneView):
    template_name = "auth/password_reset_done.html"


class BBPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "auth/password_reset_confirm.html"
    success_url = reverse_lazy('main:password_reset_complete')


class BBPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "auth/password_reset_complete.html"


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


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'auth/delete_user.html'
    success_url = reverse_lazy('main:index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удалён')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class ByRubricView(FormMixin, ListView):
    form_class = SearchForm
    template_name = 'main/by_rubric.html'
    paginate_by = 2
    context_object_name = 'bbs'

    def get_queryset(self):
        bbs = Bb.objects.filter(is_active=True, rubric=self.kwargs['pk'])
        if keyword := self.request.GET.get('keyword'):
            # There's a bug with case-insensitive search in SQLite-type
            # databases, but it works properly in PostgreSQL, and other dbs
            q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
            bbs = bbs.filter(q)
        return bbs

    def get_initial(self):
        return {'keyword': self.request.GET.get('keyword', '')}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubric'] = get_object_or_404(SubRubric, pk=self.kwargs['pk'])
        return context


class BBDetailView(DetailView):
    model = Bb
    template_name = 'main/detail.html'
    context_object_name = 'bb'

    def get_queryset(self):
        return Bb.objects.prefetch_related('additionalimage_set')
