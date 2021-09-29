from django.db import models
from apps.user.models import OmpUser


class Diary(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, db_column='FuiId', verbose_name='ID')
    user = models.ForeignKey(OmpUser, on_delete=models.CASCADE, db_column='FuiUserId', verbose_name='用户', help_text='用户')

    year = models.CharField(db_column='FstrYear', max_length=4, verbose_name='年', help_text='年', default='2000')
    month = models.CharField(db_column='FstrMonth', max_length=2, verbose_name='月', help_text='月', default='01')
    day = models.CharField(db_column='FstrDay', max_length=2, verbose_name='日', help_text='日', default='01')

    content = models.TextField(db_column='FstrContent', verbose_name='富文本框内容(HTML)', null=True, blank=True)

    status = models.SmallIntegerField(db_column='FuiStatus', verbose_name='状态 1:开启,2:关闭', default=1)
    # editor = models.CharField(db_column='FstrEditor', verbose_name='最后修改人', max_length=200, default='', null=False)
    create_time = models.DateTimeField(db_column='FuiCreateTime', verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(db_column='FuiUpdateTime', verbose_name='更新时间', auto_now=True)

    objects = models.Manager()

    class Meta:
        db_table = 't_diary_record'
        ordering = ['id']
