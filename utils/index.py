# coding: utf-8
"""
 @Topic:

 @Date: 2021-09-16

 @Author: lette.xiao

"""
from .CookiesToDict import cookies_to_dict
from apps.user.models import OmpUser
from apps.data_statistics.models import OperationRecord
from datetime import date
import logging


def get_request_user_id(request):
    cookie_dict = cookies_to_dict(request.META.get('HTTP_COOKIE'))
    email = cookie_dict['user_email']
    logging.debug("email: " + email)
    user = OmpUser.objects.get(email=email)
    return user.id


def get_request_user_email(request):
    cookie_dict = cookies_to_dict(request.META.get('HTTP_COOKIE'))
    email = cookie_dict['user_email']
    logging.debug("email: " + email)
    return email


def insert_operation_log(ob_id, ob_category, op_type, op_remark, operator, op_time=None):
    """
    记录页面操作
    :param ob_id: 操作对象ID
    :param ob_category: 操作对象类别
    :param op_type: 操作类型
    :param op_remark: 操作备注
    :param operator: 操作人
    :param op_time: 操作时间
    :return: 新增记录ID
    """
    logging.debug('插入操作记录：' + str(ob_id) + ' | ' + str(op_remark))
    if op_time and op_time != date.today().strftime('%Y-%m-%d'):
        logging.debug('插入操作路径1，带日期保存')
        new_record = OperationRecord.objects.create(object_id=ob_id,
                                                    object_category=ob_category,
                                                    operation_type=op_type,
                                                    operation_remark=op_remark,
                                                    status=1,
                                                    operator=operator)
        new_record.create_time = op_time
        new_record.save()
    else:
        logging.debug('插入操作路径2，无日期保存')
        new_record = OperationRecord.objects.create(object_id=ob_id,
                                                    object_category=ob_category,
                                                    operation_type=op_type,
                                                    operation_remark=op_remark,
                                                    status=1,
                                                    operator=operator)
    return new_record.id
