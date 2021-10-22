from django.db import models
from apps.user.models import OmpUser


class DailyTimeCollect(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, db_column='FuiId', verbose_name='ID')
    user = models.ForeignKey(OmpUser, on_delete=models.CASCADE, db_column='FuiUserId', verbose_name='用户', help_text='用户')

    year = models.CharField(db_column='FstrYear', max_length=4, verbose_name='年', help_text='年', default='2000')
    month = models.CharField(db_column='FstrMonth', max_length=2, verbose_name='月', help_text='月', default='01')
    day = models.CharField(db_column='FstrDay', max_length=2, verbose_name='日', help_text='日', default='01')

    total_time_work = models.IntegerField(db_column='FuiTotalTimeWork', verbose_name='工作总时间', help_text='工作总时间', default=0)
    total_time_study = models.IntegerField(db_column='FuiTotalTimeStudy', verbose_name='学习总时间', help_text='学习总时间', default=0)
    total_time_read = models.IntegerField(db_column='FuiTotalTimeRead', verbose_name='阅读总时间', help_text='阅读总时间', default=0)
    total_time_exercise = models.IntegerField(db_column='FuiTotalTimeExercise', verbose_name='运动总时间', help_text='运动总时间', default=0)
    total_time_plan = models.IntegerField(db_column='FuiTotalTimePlan', verbose_name='规划总时间', help_text='规划总时间', default=0)
    total_time_all = models.IntegerField(db_column='FuiTotalTimeAll', verbose_name='总耗时', help_text='总耗时', default=0)
    average_time_all = models.IntegerField(db_column='FuiAverageTimeall', verbose_name='平均耗时', help_text='平均耗时', default=0)

    status = models.SmallIntegerField(db_column='FuiStatus', verbose_name='状态', help_text='状态 1:有效,2:无效', default=1)
    create_time = models.DateTimeField(db_column='FuiCreateTime', verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(db_column='FuiUpdateTime', verbose_name='更新时间', help_text='更新时间', auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 't_daily_time_collect'
        ordering = ['id']


class OperationRecord(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, db_column='FuiId', verbose_name='ID')

    object_id = models.BigIntegerField(db_column='FuiObjectId', verbose_name='操作对象ID', default=0, null=False)
    object_category = models.SmallIntegerField(db_column='FuiObjectCategory', verbose_name='操作对象类别 1:月任务; 2:周任务', default=0, null=False)

    operation_type = models.SmallIntegerField(db_column='FuiOpType', verbose_name='操作类型 1:创建; 2:更新; 3:删除', default=0, null=False)
    operation_remark = models.TextField(db_column='FuiOpRemark', verbose_name='操作备注', null=True, blank=True)

    status = models.SmallIntegerField(db_column='FuiStatus', verbose_name='状态', help_text='状态 1:有效,2:无效', default=1)
    operator = models.CharField(db_column='FstrOperator', verbose_name='操作者', max_length=200, default='', null=False)

    create_time = models.DateTimeField(db_column='FuiCreateTime', verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(db_column='FuiUpdateTime', verbose_name='更新时间', help_text='更新时间', auto_now=True)

    objects = models.Manager()

    @property
    def operation_type_name(self):
        name_list = ['none', '创建操作', '更新操作', '删除操作']
        return name_list[self.operation_type]

    class Meta:
        db_table = 't_operation_record'
        ordering = ['id']
