from rest_framework.generics import ListAPIView

from .serializers import BbSerializer
from main.models import Bb


class BbList(ListAPIView):
    serializer_class = BbSerializer

    def get_queryset(self):
        return Bb.objects.filter(is_active=True)[:10]
