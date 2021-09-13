# coding: utf-8
"""
 @Topic:

 @Date: 2021-09-05

 @Author: lette.xiao

 @Copyright（C）: 2014-2021 X-Financial Inc. All rights reserved.
"""
from rest_framework import filters


class TaskNameSearchFilter(filters.SearchFilter):
    """
    任务名称搜索类
    """
    # 自定义url中的模糊搜索参数名
    search_param = "task_name"
