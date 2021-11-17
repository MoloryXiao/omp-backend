from django.db import models
from apps.user.models import OmpUser


class MonthPlan(models.Model):
    """
    月计划
    """
    id = models.BigAutoField(auto_created=True, primary_key=True, db_column='FuiId', verbose_name='ID')
    user = models.ForeignKey(OmpUser, on_delete=models.CASCADE, db_column='FuiUserId', verbose_name='用户')
    year = models.IntegerField(db_column='FuiYear', verbose_name='年份', default=2000)
    month = models.IntegerField(db_column='FuiMonth', verbose_name='月份', default=1)
    task_name = models.CharField(db_column='FstrTaskName', verbose_name='任务项名称', max_length=256, null=False, blank=False)
    task_type = models.SmallIntegerField(db_column='FuiTaskType', verbose_name='任务项类型 1:学习 2:工作 3:生活 4:规划',
                                         default=0, null=False)
    target_times = models.IntegerField(db_column='FuiTargetTimes', verbose_name='目标次数', default=0)
    completed_times = models.IntegerField(db_column='FuiCompletedTimes', verbose_name='完成次数', default=0)
    reward_mechanism = models.SmallIntegerField(db_column='FuiRewardMechanism', verbose_name='奖励机制 1:一次性 2:阶段性',
                                                default=0, null=False)
    multi_stages = models.CharField(db_column='FstrMultiStages', verbose_name='阶段性目标 json格式', max_length=512,
                                    null=True, blank=True)
    todo_list = models.TextField(db_column='FstrTodoList', verbose_name='Todo清单 json格式', null=True, blank=True)
    remark = models.TextField(db_column='FstrRemark', verbose_name='备注', null=True, blank=True)

    status = models.SmallIntegerField(db_column='FuiStatus', verbose_name='状态 0:关闭 1:开启,2:废弃', default=1)
    # editor = models.CharField(db_column='FstrEditor', verbose_name='最后修改人', max_length=200, default='', null=False)
    create_time = models.DateTimeField(db_column='FuiCreateTime', verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(db_column='FuiUpdateTime', verbose_name='更新时间', auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 't_monthly_plan'
        ordering = ['id']

    def __str__(self):
        return str(self.id)+'-'+str(self.task_name)


class WeekPlan(models.Model):
    """
    周计划
    """
    id = models.BigAutoField(auto_created=True, primary_key=True, db_column='FuiId', verbose_name='ID')
    user = models.ForeignKey(OmpUser, on_delete=models.CASCADE, db_column='FuiUserId', verbose_name='用户')

    task_name = models.CharField(db_column='FstrTaskName', verbose_name='任务项名称', max_length=256, null=False, blank=False)
    task_type = models.SmallIntegerField(db_column='FuiTaskType', verbose_name='任务项类型 1:学习 2:工作 3:生活 4:规划',
                                         default=0, null=False)
    start_date = models.DateField(db_column='FdtStartDate', verbose_name='开始时间', null=False, blank=False)
    end_date = models.DateField(db_column='FdtEndDate', verbose_name='结束时间', null=False, blank=False)
    remark = models.TextField(db_column='FstrRemark', verbose_name='备注', null=True, blank=True)

    status = models.SmallIntegerField(db_column='FuiStatus', verbose_name='状态 0:未完成 1:已完成,2:废弃', default=1)
    # editor = models.CharField(db_column='FstrEditor', verbose_name='最后修改人', max_length=200, default='', null=False)
    create_time = models.DateTimeField(db_column='FuiCreateTime', verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(db_column='FuiUpdateTime', verbose_name='更新时间', auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 't_weekly_plan'
        ordering = ['id']

    def __str__(self):
        return str(self.id)+'-'+str(self.task_name)
