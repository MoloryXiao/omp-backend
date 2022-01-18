# coding: utf-8
"""
 @Topic:

 @Date: 2021-09-05

 @Author: lette.xiao

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


