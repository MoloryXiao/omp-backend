from rest_framework import serializers
from apps.diary import models


class DiarySerializer(serializers.ModelSerializer):
    """月度计划序列化器"""
    class Meta:
        model = models.Diary
        fields = "__all__"
        extra_kwargs = {
            'user': {
                'write_only': True
            }
        }


class DiaryListSerializer(serializers.ModelSerializer):
    """月度计划序列化器"""
    class Meta:
        model = models.Diary
        fields = "__all__"
        extra_kwargs = {
            'user': {
                'write_only': True
            },
            'content': {
                'write_only': True
            }
        }
