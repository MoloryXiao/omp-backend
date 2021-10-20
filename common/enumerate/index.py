# coding: utf-8
"""
 @Topic:

 @Date: 2021-10-20

 @Author: lette.xiao

 @Copyright（C）: 2014-2021 X-Financial Inc. All rights reserved.
"""
import enum


class ObjectCategory(enum.Enum):
    MONTH_PLAN_TASK = 1
    WEEK_PLAN_TASK = 2


class OperationType(enum.Enum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3
