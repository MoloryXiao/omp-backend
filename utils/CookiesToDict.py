# coding: utf-8
"""
 @Topic:

 @Date: 2021-09-12

 @Author: lette.xiao

 @Copyright（C）: 2014-2021 X-Financial Inc. All rights reserved.
"""


def cookies_to_dict(cookie):
    cookie_dic = {}
    for i in cookie.split('; '):
        cookie_dic[i.split('=')[0]] = i.split('=')[1]
    return cookie_dic