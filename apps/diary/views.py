import math

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from bs4 import BeautifulSoup
from datetime import datetime
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.user.models import OmpUser
from utils.index import get_request_user_id
from . import models, serializers
from rest_framework.viewsets import ModelViewSet
from utils.BaseResponse import response_ok, response_error
from apps.data_statistics.models import DailyTimeCollect


class Diary(ModelViewSet):
    queryset = models.Diary.objects.all()
    serializer_class = serializers.DiarySerializer
    authentication_classes = (JSONWebTokenAuthentication,)

    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('year', 'month', 'day')
    search_fields = ('task_name',)

    def get_queryset(self):
        user_id = get_request_user_id(self.request)
        return models.Diary.objects.filter(status__in=(0, 1), user=user_id).order_by("-year", "-month", "-day")

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = get_request_user_id(self.request)
        data['status'] = 1

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # 查询当天是否已有日志记录
        diary = models.Diary.objects.filter(status=1, user=data['user'], year=data['year'], month=data['month'], day=data['day'])
        print(diary)
        # 如果已有记录，则将原有记录设置为失效态
        if diary:
            diary[0].status = 2
            diary[0].save()
        # 插入新的记录
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # 插入首页数据视图记录
        insert_daily_time_collect(data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # 软删除
        instance.status = 2
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TimeRecord:
    def __init__(self, start_time, end_time, task_type, task_name):
        self.start_time = start_time
        self.end_time = end_time
        if start_time and end_time:
            st = datetime.strptime(start_time, "%H:%M")
            et = datetime.strptime(end_time, "%H:%M")
            self.interval_seconds = (et - st).seconds
        else:
            self.interval_seconds = 0
        self.task_type = task_type
        self.task_name = task_name

    def __str__(self):
        return str(str(self.start_time)+" "+str(self.end_time)+" "+str(self.task_type)+" "+
                   self.task_name)+" —— "+str(self.interval_seconds/60)


class DiaryHandler(APIView):
    def post(self, request):
        diary_year = request.data['year']
        diary_month = request.data['month']
        diary_day = request.data['day']
        html_code = request.data['content']
        print(diary_year, '-', diary_month, '-', diary_day)

        [time_record_list, time_distribution] = handle_time_distribution(html_code)

        hotpot_list = build_time_hotpot(time_record_list)
        # 展示二维数组内容
        # for li in hotpot_list:
        #     print(li)
        time_distribution["hotpot"] = hotpot_list

        return Response(data=response_ok(data=time_distribution), status=status.HTTP_200_OK)


def handle_time_distribution(html_code):
    soup = BeautifulSoup(html_code, 'html.parser', from_encoding='utf-8')
    diary_table = soup.find_all("div")

    column_count = 0
    start_time = ''
    end_time = ''
    task_type = ''
    time_record_list = []

    # 分析日记表格，创建TimeRecord记录
    for item in diary_table:
        column_count += 1
        if column_count == 1:
            time_str_list = item.string.split("-")
            if len(time_str_list) == 1:
                start_time = time_str_list[0]
                end_time = ''
            elif len(time_str_list) == 2:
                start_time = time_str_list[0]
                end_time = time_str_list[1]
            else:
                return Response(data=response_error(msg="时间样式异常", data=str(time_str_list)),
                                status=status.HTTP_400_BAD_REQUEST)
        elif column_count == 2:
            task_type = item.string
        else:
            task_name = item.string
            column_count = 0
            tr = TimeRecord(start_time=start_time, end_time=end_time, task_type=task_type, task_name=task_name)
            time_record_list.append(tr)

    time_distribution = dict()
    for item in time_record_list:
        print(item)
        if item.interval_seconds != 0:
            if item.task_type not in time_distribution:
                time_distribution[item.task_type] = item.interval_seconds / 60
            else:
                time_distribution[item.task_type] += item.interval_seconds / 60

    print("--- 时间分布 ---")
    print(time_distribution)
    print("---------------")

    return [time_record_list, time_distribution]


def build_time_hotpot(time_record_list):
    hotpot_list = []
    row_cube = 12
    column_cube = 24
    mins_cube = 5
    one_cube_seconds = mins_cube * 60
    one_row_seconds = column_cube * one_cube_seconds
    # 初始化热点二维数组
    for i in range(row_cube):
        tag_list = []
        for j in range(column_cube):
            tag_list.append('none')
        hotpot_list.append(tag_list)
    base_line = datetime.strptime("00:00", "%H:%M")
    for tr in time_record_list:
        start_timestamp = int(datetime.strptime(tr.start_time, "%H:%M").timestamp()-base_line.timestamp())
        end_timestamp = int(datetime.strptime(tr.end_time, "%H:%M").timestamp()-base_line.timestamp())
        if tr.end_time == "00:00":
            end_timestamp += 3600*24
        # print(start_timestamp)
        # print(end_timestamp)
        start_row = math.floor(start_timestamp/one_row_seconds)
        end_row = math.floor(end_timestamp/one_row_seconds)
        # print(math.floor(start_row))
        # print(math.floor(end_row))
        start_column = int((start_timestamp-(one_row_seconds * start_row))/one_cube_seconds)
        end_column = int((end_timestamp-(one_row_seconds * end_row))/one_cube_seconds)
        # print(start_column)
        # print(end_column)
        if start_row == end_row:
            for i in range(start_column, end_column):
                hotpot_list[start_row][i] = tr.task_type
        else:
            while start_row < end_row:
                for i in range(start_column, column_cube):
                    hotpot_list[start_row][i] = tr.task_type
                start_column = 0
                start_row += 1
            for i in range(0, end_column):
                hotpot_list[start_row][i] = tr.task_type
    return hotpot_list


def insert_daily_time_collect(request_data):
    [time_record_list, time_distribution] = handle_time_distribution(request_data['content'])
    print('[create] time_distribution=', time_distribution)
    time_collect = DailyTimeCollect.objects.filter(status=1, user=request_data['user'], year=request_data['year'],
                                                   month=request_data['month'], day=request_data['day'])

    if '工作' not in time_distribution or time_distribution['工作'] == 0:
        time_distribution['工作'] = 5
    if '学习' not in time_distribution or time_distribution['学习'] == 0:
        time_distribution['学习'] = 5
    if '阅读' not in time_distribution or time_distribution['阅读'] == 0:
        time_distribution['阅读'] = 5
    if '健身' not in time_distribution or time_distribution['健身'] == 0:
        time_distribution['健身'] = 5
    if '规划' not in time_distribution or time_distribution['规划'] == 0:
        time_distribution['规划'] = 5
    total_time = time_distribution['工作'] + time_distribution['学习'] + time_distribution['阅读'] + time_distribution['健身'] + time_distribution['规划']
    average_time = int(total_time/4)
    if not time_collect:
        user = OmpUser.objects.get(id=request_data['user'])
        DailyTimeCollect.objects.create(year=request_data['year'], month=request_data['month'], day=request_data['day'],
                                        user=user, status=1,
                                        total_time_work=time_distribution['工作'],
                                        total_time_study=time_distribution['学习'],
                                        total_time_read=time_distribution['阅读'],
                                        total_time_exercise=time_distribution['健身'],
                                        total_time_plan=time_distribution['规划'],
                                        total_time_all=total_time, average_time_all=average_time)
        print('已创建新数据趋势记录！', time_distribution, ' ', total_time, ' ', average_time)
    else:
        time_collect[0].total_time_work = time_distribution['工作']
        time_collect[0].total_time_study = time_distribution['学习']
        time_collect[0].total_time_read = time_distribution['阅读']
        time_collect[0].total_time_exercise = time_distribution['健身']
        time_collect[0].total_time_plan = time_distribution['规划']
        time_collect[0].total_time_all = total_time
        time_collect[0].average_time_all = average_time
        time_collect[0].save()
        print('已更新数据趋势记录！', time_distribution, ' ', total_time, ' ', average_time)
