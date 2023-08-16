from django.urls import path

from .views import (
    IndexView, OtherView, BBLoginView,
    ProfileView, BBLogoutView, ChangeUserInfoView,
    BBPasswordChangeView, RegisterUserView,
    RegisterDoneView, ActivateUserView, DeleteUserView,
    BBPasswordResetView, BBPasswordResetDoneView,
    BBPasswordResetConfirmView, BBPasswordResetCompleteView,
    ByRubricView, BBDetailView,
)

app_name = 'main'
urlpatterns = [
    path(
        'accounts/reset-password/complete',
        BBPasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
    path(
        'accounts/reset/<str:uidb64>/<str:token>/',
        BBPasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'accounts/reset-password/done',
        BBPasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'accounts/reset-password',
        BBPasswordResetView.as_view(),
        name='reset_password',
    ),
    path(
        'accounts/register/activate/<str:sign>/',
        ActivateUserView.as_view(),
        name='register_activate',
    ),
    path(
        'accounts/register/done',
        RegisterDoneView.as_view(),
        name='register_done',
    ),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path(
        'accounts/password/change/',
        BBPasswordChangeView.as_view(),
        name='password_change',
    ),
    path(
        'accounts/profile/delete',
        DeleteUserView.as_view(),
        name='profile_delete',
    ),
    path(
        'accounts/profile/change/',
        ChangeUserInfoView.as_view(),
        name='profile_change',
    ),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('<int:rubric_pk>/<int:pk>/', BBDetailView.as_view(), name='detail'),
    path('<int:pk>/', ByRubricView.as_view(), name='by_rubric'),
    path('<str:page>/', OtherView.as_view(), name='other'),
    path('', IndexView.as_view(), name='index'),
]
