from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from apps.plan import models, serializers, filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.plan.filter import WeekPlanFilter
from utils import BaseResponse
from utils.index import get_request_user_id, get_request_user_email, insert_operation_log
from common.enumerate.index import ObjectCategory, OperationType
import logging
import json

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

    # 重写perform_create，获取新记录ID值
    def perform_create(self, serializer):
        new_object = serializer.save()
        return new_object.id

    def create(self, request, *args, **kwargs):
        request.data['user'] = get_request_user_id(self.request)
        logging.debug(request.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_object_id = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 插入操作记录日志
        insert_operation_log(ob_id=new_object_id,
                             ob_category=ObjectCategory.MONTH_PLAN_TASK.value,
                             op_type=OperationType.CREATE.value,
                             op_remark='新建月计划任务',
                             operator=get_request_user_email(self.request))
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        # 插入操作记录日志
        insert_operation_log(ob_id=instance.id,
                             ob_category=ObjectCategory.MONTH_PLAN_TASK.value,
                             op_type=OperationType.UPDATE.value,
                             op_remark='更新月计划任务',
                             operator=get_request_user_email(self.request))
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 软删除
        instance.status = 2
        instance.save()
        logging.debug("plan_id: "+str(instance.id)+" soft deleted.")
        # 插入操作记录日志
        insert_operation_log(ob_id=instance.id,
                             ob_category=ObjectCategory.MONTH_PLAN_TASK.value,
                             op_type=OperationType.DELETE.value,
                             op_remark='删除月计划任务',
                             operator=get_request_user_email(self.request))
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def increase_times(self, request, pk):
        month_plan = self.get_object()
        logging.debug(request.data.get('date'))
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
        insert_operation_log(ob_id=month_plan.id,
                             ob_category=ObjectCategory.MONTH_PLAN_TASK.value,
                             op_type=OperationType.UPDATE.value,
                             op_remark='月计划任务当前次数+1',
                             operator=get_request_user_email(self.request),
                             op_time=request.data.get('date'))
        return Response(data=BaseResponse.response_ok(),status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def decrease_times(self, request, pk):
        month_plan = self.get_object()
        logging.debug(request.data.get('date'))
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
        # 插入操作记录日志
        insert_operation_log(ob_id=month_plan.id,
                             ob_category=ObjectCategory.MONTH_PLAN_TASK.value,
                             op_type=OperationType.UPDATE.value,
                             op_remark='月计划任务当前次数-1',
                             operator=get_request_user_email(self.request),
                             op_time=request.data.get('date'))
        return Response(data=BaseResponse.response_ok(),status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def save_todo_list(self, request, pk):
        month_plan = self.get_object()
        logging.debug(month_plan)
        logging.debug(request.data.get('todo_list'))
        todo_list = json.loads(month_plan.todo_list)
        logging.debug(todo_list["todo_list_detail"])

        todo_list["todo_list_detail"] = request.data.get('todo_list')

        month_plan.todo_list = json.dumps(todo_list)
        month_plan.save()

        # 插入操作记录日志
        insert_operation_log(ob_id=month_plan.id,
                             ob_category=ObjectCategory.MONTH_PLAN_TASK.value,
                             op_type=OperationType.UPDATE.value,
                             op_remark='修改月计划任务TodoList',
                             operator=get_request_user_email(self.request))
        return Response(data=BaseResponse.response_ok(), status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def get_todo_list(self, request, pk):
        month_plan = self.get_object()
        logging.debug(month_plan)
        return Response(data=BaseResponse.response_ok(data=month_plan.todo_list), status=status.HTTP_200_OK)


class WeekPlan(ModelViewSet):
    queryset = models.WeekPlan.objects.all()
    serializer_class = serializers.WeekPlanSerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    pagination_class = MonthPlanPageNum
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('id',)
    filterset_class = WeekPlanFilter

    def get_queryset(self):
        user_id = get_request_user_id(self.request)
        return models.WeekPlan.objects\
            .filter(status__in=(0, 1), user=user_id)\
            .order_by("status", "task_type", "start_date", "end_date")

    # 重写perform_create，获取新记录ID值
    def perform_create(self, serializer):
        new_object = serializer.save()
        return new_object.id

    def create(self, request, *args, **kwargs):
        request.data['user'] = get_request_user_id(self.request)
        logging.debug(request.data)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_object_id = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 插入操作记录日志
        insert_operation_log(ob_id=new_object_id,
                             ob_category=ObjectCategory.WEEK_PLAN_TASK.value,
                             op_type=OperationType.CREATE.value,
                             op_remark='新建周计划任务',
                             operator=get_request_user_email(self.request))
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        # 插入操作记录日志
        insert_operation_log(ob_id=instance.id,
                             ob_category=ObjectCategory.WEEK_PLAN_TASK.value,
                             op_type=OperationType.UPDATE.value,
                             op_remark='更新周计划任务',
                             operator=get_request_user_email(self.request))
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 软删除
        instance.status = 2
        instance.save()
        logging.debug("plan_id: "+str(instance.id)+" soft deleted.")
        # 插入操作记录日志
        insert_operation_log(ob_id=instance.id,
                             ob_category=ObjectCategory.WEEK_PLAN_TASK.value,
                             op_type=OperationType.DELETE.value,
                             op_remark='删除周计划任务',
                             operator=get_request_user_email(self.request))
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=True)
    def status_inversion(self, request, *args, **kwargs):
        instance = self.get_object()
        logger.debug(str(instance) + ' before: ' + str(instance.status))
        op_remark = ''
        # 状态取反
        if instance.status == 1:
            instance.status = 0
            instance.save()
            op_remark = '更新周计划任务状态为未完成'
        elif instance.status == 0:
            instance.status = 1
            instance.save()
            op_remark = '更新周计划任务状态为已完成'
        # 插入操作记录日志
        insert_operation_log(ob_id=instance.id,
                             ob_category=ObjectCategory.WEEK_PLAN_TASK.value,
                             op_type=OperationType.UPDATE.value,
                             op_remark=op_remark,
                             operator=get_request_user_email(self.request),
                             op_time=request.data.get('date'))
        logger.debug(str(instance) + ' after: ' + str(instance.status))
        return Response(status=status.HTTP_204_NO_CONTENT)