# coding: utf-8
"""
 @Topic:

 @Date: 2021-09-05

 @Author: lette.xiao

"""
from rest_framework import filters
from django_filters.rest_framework import FilterSet, DateFilter, CharFilter
from . import models


class TaskNameSearchFilter(filters.SearchFilter):
    """
    任务名称搜索类
    """
    # 自定义url中的模糊搜索参数名
    search_param = "task_name"


class WeekPlanFilter(FilterSet):
    # 开始时间
    start_date = DateFilter(field_name='start_date', lookup_expr='gte')
    # 结束时间
    end_date = DateFilter(field_name='end_date', lookup_expr='lte')
    # 任务名称
    task_name = CharFilter(field_name='task_name', lookup_expr='icontains')

    class Meta:
        model = models.WeekPlan
        fields = ['start_date', 'end_date', 'task_type', 'status']