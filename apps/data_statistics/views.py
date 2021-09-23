from rest_framework.viewsets import ModelViewSet
from apps.data_statistics import models, serializers
from utils.index import get_request_user_id
from rest_framework.filters import OrderingFilter


class DailyTimeCollect(ModelViewSet):
    queryset = models.DailyTimeCollect.objects.all()
    serializer_class = serializers.DailyTimeCollectSerializer

    filter_backends = (OrderingFilter,)
    # ordering_fields = ('id')

    def get_queryset(self):
        user_id = get_request_user_id(self.request)
        return models.DailyTimeCollect.objects.filter(status=1, user=user_id).order_by("year", "month", "day")
