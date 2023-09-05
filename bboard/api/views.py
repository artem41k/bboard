from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q

from .serializers import (BbDetailSerializer, BbSerializer, CommentSerializer,
                          RubricSerializer)
from main.models import Bb, Comment, SuperRubric, Rubric


class BbListView(ListAPIView):
    serializer_class = BbSerializer
    queryset = Bb.objects.select_related('rubric').filter(is_active=True)[:10]


class BbDetailView(RetrieveAPIView):
    serializer_class = BbDetailSerializer
    queryset = Bb.objects.select_related('rubric').filter(is_active=True)


class CommentsView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(is_active=True, bb=self.kwargs['pk'])


class RubricsListView(ListAPIView):
    serializer_class = RubricSerializer
    queryset = SuperRubric.objects.prefetch_related('rubrics')


class RubricInfoView(RetrieveAPIView):
    serializer_class = RubricSerializer
    queryset = Rubric.objects.all()


class ByRubricView(ListAPIView):
    serializer_class = BbSerializer

    def get_queryset(self):
        bbs = Bb.objects.select_related('rubric').filter(
            is_active=True, rubric=self.kwargs['pk']
        )
        if keyword := self.request.GET.get('keyword'):
            # There's a bug with case-insensitive search in SQLite-type
            # databases, but it works properly in PostgreSQL, and other dbs
            q = Q(title__icontains=keyword) | Q(content__icontains=keyword)
            bbs = bbs.filter(q)
        return bbs
