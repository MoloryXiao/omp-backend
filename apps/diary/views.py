from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from bs4 import BeautifulSoup
from datetime import datetime

from utils.BaseResponse import response_ok, response_error


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
        print(diary_year)
        print(diary_month)
        print(diary_day)

        soup = BeautifulSoup(html_code, 'html.parser', from_encoding='utf-8')
        diary_table = soup.find_all("div")

        column_count = 0
        start_time = ''
        end_time = ''
        task_type = ''
        time_record_list = []
        time_distribution = {
            "无": 0,
            "工作": 0,
            "学习": 0,
            "阅读": 0,
            "规划": 0,
            "健身": 0,
            "未知分类": 0
        }

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
                    return Response(data=response_error(msg="时间样式异常", data=str(time_str_list)), status=status.HTTP_400_BAD_REQUEST)
            elif column_count == 2:
                task_type = item.string
            else:
                task_name = item.string
                column_count = 0
                tr = TimeRecord(start_time=start_time, end_time=end_time, task_type=task_type, task_name=task_name)
                time_record_list.append(tr)

        # 分类时间汇总
        for item in time_record_list:
            print(item)
            if item.interval_seconds != 0:
                if item.task_type in time_distribution:
                    time_distribution[item.task_type] += item.interval_seconds/60
                else:
                    print("未知分类："+item.task_type)
                    time_distribution["未知分类"] += item.interval_seconds/60

        print("--- 时间分布 ---")
        print(time_distribution)

        return Response(data=response_ok(data=time_distribution), status=status.HTTP_200_OK)