from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import (CreateView, DeleteView, FormMixin,
                                       UpdateView)
from django.views.generic.list import ListView

from .forms import (AddImgFormSet, BbForm, ChangeUserInfoForm,
                    GuestCommentForm, RegisterUserForm, SearchForm,
                    UserCommentForm)
from .models import AdvUser, Bb, SubRubric
from .utilities import signer


class IndexView(ListView):
    template_name = 'main/index.html'
    model = Bb
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(is_active=True)[:10]


class OtherView(TemplateView):
    def get_template_names(self):
        return [f"main/{self.kwargs['page']}.html"]

# Auth & Profile Views


class BBLoginView(LoginView):
    template_name = 'auth/login.html'


class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'main/profile.html'
    model = Bb
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(author=self.request.user.pk)


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


class BBDetailView(FormMixin, SuccessMessageMixin, DetailView):
    model = Bb
    template_name = 'main/detail.html'
    context_object_name = 'bb'
    success_message = 'Комментарий добавлен'

    def get_queryset(self):
        return Bb.objects.prefetch_related(
            'additionalimage_set', 'comment_set'
        )

    def get_success_url(self):
        return reverse(
            'main:detail', kwargs={
                'rubric_pk': self.object.rubric.pk,
                'pk': self.object.pk
            }
        )

    # Redefinition of the post method, needed to mix FormMixin and DetailView
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        if self.request.user.is_authenticated:
            form_class = UserCommentForm
        else:
            form_class = GuestCommentForm
        return super().get_form(form_class)

    def get_initial(self):
        initial = {'bb': self.object}
        if self.request.user.is_authenticated:
            initial['author'] = self.request.user.username

        return initial


class BBCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Bb
    template_name = 'main/profile_bb_add.html'
    form_class = BbForm
    success_message = 'Объявление добавлено'
    success_url = reverse_lazy('main:profile')

    def form_valid(self, form):
        self.object = form.save()
        formset = AddImgFormSet(
            self.request.POST, self.request.FILES, instance=self.object
        )
        if formset.is_valid():
            formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self):
        init_dict = super().get_initial()
        init_dict['author'] = self.request.user.pk
        return init_dict

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = AddImgFormSet()
        return context


class BBChangeView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Bb
    template_name = 'main/profile_bb_change.html'
    form_class = BbForm
    success_message = 'Объявление изменено'

    def get_success_url(self) -> str:
        return reverse(
            'main:detail', kwargs={
                'rubric_pk': self.object.pk, 'pk': self.object.pk
            }
        )

    def form_valid(self, form):
        self.object = form.save()
        formset = AddImgFormSet(
            self.request.POST, self.request.FILES, instance=self.object
        )
        if formset.is_valid():
            formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = AddImgFormSet(instance=self.object)
        return context


class BBDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Bb
    template_name = 'main/profile_bb_delete.html'
    success_message = 'Объявление удалено'
    success_url = reverse_lazy('main:profile')
    context_object_name = 'bb'
