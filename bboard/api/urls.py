from django.urls import path

from .views import BbList

urlpatterns = [
    path('bbs/', BbList.as_view()),
]
