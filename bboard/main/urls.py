from django.urls import path

from .views import IndexView, OtherView

app_name = 'main'
urlpatterns = [
    path('<str:page>/', OtherView.as_view(), name='other'),
    path('', IndexView.as_view(), name='index'),
]