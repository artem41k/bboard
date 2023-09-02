from rest_framework.generics import (ListAPIView, ListCreateAPIView,
                                     RetrieveAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import (BbDetailSerializer, BbSerializer, CommentSerializer,
                          RubricSerializer)
from main.models import Bb, Comment, SuperRubric


class BbListView(ListAPIView):
    serializer_class = BbSerializer
    queryset = Bb.objects.filter(is_active=True)[:10]


class BbDetailView(RetrieveAPIView):
    serializer_class = BbDetailSerializer
    queryset = Bb.objects.filter(is_active=True)


class CommentsView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(is_active=True, bb=self.kwargs['pk'])


class RubricsListView(ListAPIView):
    serializer_class = RubricSerializer
    queryset = SuperRubric.objects.prefetch_related("rubrics")
