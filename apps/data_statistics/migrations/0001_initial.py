# Generated by Django 3.2.3 on 2021-09-16 23:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyTimeCollect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, db_column='FuiId', primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(db_column='FstrYear', default='2000', help_text='年', max_length=4, verbose_name='年')),
                ('month', models.CharField(db_column='FstrMonth', default='01', help_text='月', max_length=2, verbose_name='月')),
                ('day', models.CharField(db_column='FstrDay', default='01', help_text='日', max_length=2, verbose_name='日')),
                ('total_time_work', models.IntegerField(db_column='FuiTotalTimeWork', default=0, help_text='工作总时间', verbose_name='工作总时间')),
                ('total_time_study', models.IntegerField(db_column='FuiTotalTimeStudy', default=0, help_text='学习总时间', verbose_name='学习总时间')),
                ('total_time_read', models.IntegerField(db_column='FuiTotalTimeRead', default=0, help_text='阅读总时间', verbose_name='阅读总时间')),
                ('total_time_exercise', models.IntegerField(db_column='FuiTotalTimeExercise', default=0, help_text='运动总时间', verbose_name='运动总时间')),
                ('total_time_plan', models.IntegerField(db_column='FuiTotalTimePlan', default=0, help_text='规划总时间', verbose_name='规划总时间')),
                ('total_time_all', models.IntegerField(db_column='FuiTotalTimeAll', default=0, help_text='总耗时', verbose_name='总耗时')),
                ('average_time_all', models.IntegerField(db_column='FuiAverageTimeall', default=0, help_text='平均耗时', verbose_name='平均耗时')),
                ('status', models.SmallIntegerField(db_column='FuiStatus', default=1, help_text='状态 1:有效,2:无效', verbose_name='状态')),
                ('create_time', models.DateTimeField(auto_now_add=True, db_column='FuiCreateTime', help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, db_column='FuiUpdateTime', help_text='更新时间', verbose_name='更新时间')),
                ('user', models.ForeignKey(db_column='FuiUserId', help_text='用户', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'db_table': 't_daily_time_collect',
                'ordering': ['id'],
            },
        ),
    ]
