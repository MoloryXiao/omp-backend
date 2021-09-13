from rest_framework import serializers
from apps.user import models


class OmpUserSerializer(serializers.ModelSerializer):
    """登录用户序列化器"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.OmpUser
        fields = "__all__"

