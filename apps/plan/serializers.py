from rest_framework import serializers
from apps.plan import models


class MonthPlanSerializer(serializers.ModelSerializer):
    """月度计划序列化器"""
    class Meta:
        model = models.MonthPlan
        fields = "__all__"
        extra_kwargs = {
            'user': {
                'write_only': True
            }
        }


class CompletedTimesSerializer(serializers.ModelSerializer):
    """完成次数化器"""

    class Meta:
        model = models.MonthPlan
        fields = ('completed_times', 'target_times')
        extra_kwargs = {
            'user': {
                'write_only': True
            }
        }
