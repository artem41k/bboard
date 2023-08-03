from django.urls import path

from .views import (
    IndexView, OtherView, BBLoginView,
    ProfileView, BBLogoutView, ChangeUserInfoView,
    BBPasswordChangeView, RegisterUserView,
    RegisterDoneView
)

app_name = 'main'
urlpatterns = [
    path(
        'accounts/register/done',
        RegisterDoneView.as_view(),
        name='register'
    ),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path(
        'accounts/password/change/',
        BBPasswordChangeView.as_view(),
        name='password_change'
    ),
    path(
        'accounts/profile/change/',
        ChangeUserInfoView.as_view(),
        name='profile_change'
    ),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('<str:page>/', OtherView.as_view(), name='other'),
    path('', IndexView.as_view(), name='index'),
]