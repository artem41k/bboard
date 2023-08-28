from django.urls import path

from .views import BbListView, BbDetailView, CommentsView

urlpatterns = [
    path("bbs/<int:pk>/comments", CommentsView.as_view()),
    path('bbs/<int:pk>/', BbDetailView.as_view()),
    path('bbs/', BbListView.as_view()),
]
