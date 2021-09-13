from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from apps.user import models
from apps.user import serializers
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework_jwt.utils import jwt_decode_handler
from utils import BaseResponse
import datetime

from utils.CookiesToDict import cookies_to_dict


class UserInfoModelView(ModelViewSet):
    queryset = models.OmpUser.objects.all()
    serializer_class = serializers.OmpUserSerializer

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('id',)
    filterset_fields = ('email',)

    def list(self, request, *args, **kwargs):
        # import jwt
        # try:
        #     token = request.META.get('HTTP_AUTHORIZATION')[3:]
        #     token_user = jwt_decode_handler(token)
        #     print(token_user)
        #     date_array = datetime.datetime.fromtimestamp(token_user['exp'])
        #     other_style_time = date_array.strftime("%Y-%m-%d %H:%M:%S")
        #     print("用户邮箱：" + str(token_user['email']))
        #     print("用户过期时间：" + other_style_time)
        # except jwt.exceptions.ExpiredSignatureError:
        #     return Response(BaseResponse.response_error(msg='登录过期'), status=status.HTTP_403_FORBIDDEN)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)



        return Response(serializer.data)


class UserRegister(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        name = request.data['name']
        person = models.OmpUser.objects.filter(email=email)
        res = {
            "code": 0,
            "msg": "",
            "data": {}
        }
        if any(person):
            res["code"] = -1
            res["msg"] = "用户名重复，创建失败！"
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        models.OmpUser.objects.create_user(email=email,name=name,password=password)
        res["code"] = 0
        res["msg"] = "用户创建成功！"
        res["data"] = {"email": email}
        return Response(data=res, status=status.HTTP_200_OK)
