# coding: utf-8
"""
 @Topic:

 @Date: 2021-09-16

 @Author: lette.xiao

 @Copyright（C）: 2014-2021 X-Financial Inc. All rights reserved.
"""
from .CookiesToDict import cookies_to_dict
from apps.user import models
import logging


def get_request_user_id(request):
    cookie_dict = cookies_to_dict(request.META.get('HTTP_COOKIE'))
    email = cookie_dict['user_email']
    logging.debug("email: " + email)
    user = models.OmpUser.objects.get(email=email)
    return user.id
