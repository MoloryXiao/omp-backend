# coding: utf-8
"""
 @Topic:

 @Date: 2021-09-05

 @Author: lette.xiao

 @Copyright（C）: 2014-2021 X-Financial Inc. All rights reserved.
"""


def response_ok(code=0, msg='ok', data=None):
    return {
        'basic': {
            'code': code,
            'msg': msg
        },
        'data': data
    }


def response_error(code=-1, msg='error', data=None):
    return {
        'basic': {
            'code': code,
            'msg': msg
        },
        'data': data
    }


