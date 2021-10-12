from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from apps.plan import models, serializers, filter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, DateFilter
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from utils import BaseResponse
from utils.index import get_request_user_id
import logging

logging.basicConfig(level=logging.DEBUG, format='\n|%(asctime)s|%(name)s|%(levelname)s|%(filename)s|'
                                                '%(funcName)s[%(lineno)d]|%(message)s\n')
logger = logging.getLogger(__name__)


class MonthPlanPageNum(PageNumberPagination):
    # 查询字符串中代表页码的参数名，有默认值：page
    page_query_param = 'page'
    # 查询字符串中代表每页返回数据数量的参数名，默认值：None
    page_size_query_param = 'limit'
    # 默认页大小
    page_size = 10


class MonthPlan(ModelViewSet):
    queryset = models.MonthPlan.objects.all()
    serializer_class = serializers.MonthPlanSerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    pagination_class = MonthPlanPageNum
    filter_backends = (DjangoFilterBackend, OrderingFilter, filter.TaskNameSearchFilter)
    ordering_fields = ('id',)
    filterset_fields = ('user', 'year', 'month', 'task_type', 'status')
    search_fields = ('task_name',)

    def get_queryset(self):
        user_id = get_request_user_id(self.request)
        return models.MonthPlan.objects.filter(status__in=(0, 1), user=user_id).order_by("-status", "task_type")

    def create(self, request, *args, **kwargs):
        request.data['user'] = get_request_user_id(self.request)
        logging.debug(request.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 软删除
        instance.status = 2
        instance.save()
        logging.debug("plan_id: "+str(instance.id)+" soft deleted.")
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def increase_times(self, request, pk):
        month_plan = self.get_object()
        logging.debug(month_plan)
        logging.debug("当前已完成次数/目标次数："+str(month_plan.completed_times)+"/"+str(month_plan.target_times))
        if month_plan.completed_times + 1 > month_plan.target_times:
            response_data = {
                "completed_times": month_plan.completed_times,
                "target_times": month_plan.target_times
            }
            return Response(data=BaseResponse.response_error(msg='加1失败|完成次数不能超过目标次数', data=response_data),
                            status=status.HTTP_400_BAD_REQUEST)
        month_plan.completed_times += 1
        month_plan.save()
        serializer = self.get_serializer(month_plan, data=request.data)
        serializer.is_valid()
        logging.debug("已增加，当前已完成次数/目标次数："+str(month_plan.completed_times)+"/"+str(month_plan.target_times))
        return Response(data=BaseResponse.response_ok(),status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def decrease_times(self, request, pk):
        month_plan = self.get_object()
        logging.debug(month_plan)
        logging.debug("当前已完成次数/目标次数：" + str(month_plan.completed_times) + "/" + str(month_plan.target_times))
        if month_plan.completed_times - 1 < 0:
            response_data = {
                "completed_times": month_plan.completed_times,
                "target_times": month_plan.target_times
            }
            return Response(data=BaseResponse.response_error(msg='减1失败|完成次数不能低于0', data=response_data),
                            status=status.HTTP_400_BAD_REQUEST)
        month_plan.completed_times -= 1
        month_plan.save()
        serializer = self.get_serializer(month_plan, data=request.data)
        serializer.is_valid()
        logging.debug("已减少，当前已完成次数/目标次数：" + str(month_plan.completed_times) + "/" + str(month_plan.target_times))
        return Response(data=BaseResponse.response_ok(),status=status.HTTP_200_OK)


class WeekPlanFilter(FilterSet):
    # 开始时间
    start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    # 结束时间
    end_date = DateFilter(field_name='end_date', lookup_expr='lte')


class WeekPlan(ModelViewSet):
    queryset = models.WeekPlan.objects.all()
    serializer_class = serializers.WeekPlanSerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    pagination_class = MonthPlanPageNum
    filter_backends = (DjangoFilterBackend, OrderingFilter, filter.TaskNameSearchFilter)
    filterset_class = WeekPlanFilter
    ordering_fields = ('id',)
    filterset_fields = ('user', 'task_type', 'status')
    search_fields = ('task_name',)

    def get_queryset(self):
        user_id = get_request_user_id(self.request)
        return models.WeekPlan.objects.filter(status__in=(0, 1), user=user_id).order_by("status", "task_type")

    def create(self, request, *args, **kwargs):
        request.data['user'] = get_request_user_id(self.request)
        logging.debug(request.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 软删除
        instance.status = 2
        instance.save()
        logging.debug("plan_id: "+str(instance.id)+" soft deleted.")
        return Response(status=status.HTTP_204_NO_CONTENT)