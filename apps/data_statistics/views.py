from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from apps.data_statistics import models, serializers
from utils.index import get_request_user_id
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination


class DataStatisticsPageNum(PageNumberPagination):
    # 查询字符串中代表页码的参数名，有默认值：page
    page_query_param = 'page'
    # 查询字符串中代表每页返回数据数量的参数名，默认值：None
    page_size_query_param = 'limit'
    # 默认页大小
    page_size = 365


class DailyTimeCollect(ModelViewSet):
    pagination_class = DataStatisticsPageNum
    queryset = models.DailyTimeCollect.objects.all()
    serializer_class = serializers.DailyTimeCollectSerializer

    filter_backends = (OrderingFilter,)
    # ordering_fields = ('id')

    def get_queryset(self):
        user_id = get_request_user_id(self.request)
        return models.DailyTimeCollect.objects.filter(status=1, user=user_id).order_by("year", "month", "day")


class OperationRecordModelView(ModelViewSet):
    queryset = models.OperationRecord.objects.all()
    serializer_class = serializers.OpRecordSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('object_category', 'object_id')

    def get_queryset(self):
        return models.OperationRecord.objects.filter(status=1).order_by('-create_time')
