from rest_framework import serializers
from apps.data_statistics import models


class DailyTimeCollectSerializer(serializers.ModelSerializer):
    """日常时间统计序列化器"""
    class Meta:
        model = models.DailyTimeCollect
        fields = "__all__"
        extra_kwargs = {
            'user': {
                'write_only': True
            }
        }


class OpRecordSerializer(serializers.ModelSerializer):
    operation_type_name = serializers.CharField(required=False)
    """日常时间统计序列化器"""
    class Meta:
        model = models.OperationRecord
        fields = "__all__"
