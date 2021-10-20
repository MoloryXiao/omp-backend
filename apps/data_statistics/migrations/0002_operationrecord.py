# Generated by Django 3.2.3 on 2021-10-20 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_statistics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, db_column='FuiId', primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.BigIntegerField(db_column='FuiObjectId', default=0, verbose_name='操作对象ID')),
                ('object_category', models.SmallIntegerField(db_column='FuiObjectCategory', default=0, verbose_name='操作对象类别 1:月任务; 2:周任务')),
                ('operation_type', models.SmallIntegerField(db_column='FuiOpType', default=0, verbose_name='操作类型 1:创建; 2:更新; 3:删除')),
                ('operation_remark', models.TextField(blank=True, db_column='FuiOpRemark', null=True, verbose_name='操作备注')),
                ('status', models.SmallIntegerField(db_column='FuiStatus', default=1, help_text='状态 1:有效,2:无效', verbose_name='状态')),
                ('operator', models.CharField(db_column='FstrOperator', default='', max_length=200, verbose_name='操作者')),
                ('create_time', models.DateTimeField(auto_now_add=True, db_column='FuiCreateTime', help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, db_column='FuiUpdateTime', help_text='更新时间', verbose_name='更新时间')),
            ],
            options={
                'db_table': 't_operation_record',
                'ordering': ['id'],
            },
        ),
    ]