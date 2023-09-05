from django.urls import path

from .views import (BbListView, BbDetailView, ByRubricView, CommentsView,
                    RubricInfoView, RubricsListView)

urlpatterns = [
    path('rubrics/<int:pk>/info/', RubricInfoView.as_view()),
    path('rubrics/<int:pk>/', ByRubricView.as_view()),
    path('rubrics/', RubricsListView.as_view()),
    path('bbs/<int:pk>/comments/', CommentsView.as_view()),
    path('bbs/<int:pk>/', BbDetailView.as_view()),
    path('bbs/', BbListView.as_view()),
]
