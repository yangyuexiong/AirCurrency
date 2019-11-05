# -*- coding: utf-8 -*-
# @Time    : 2019-10-30 14:37
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : CarryTask.py
# @Software: PyCharm


import time
import os
from datetime import date, datetime

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=6, minute=1, second=1)
@sched.scheduled_job('cron', hour=15, minute=30, second=1)
def cron_task():
    print('开始时间:{}'.format(datetime.now()))

    path_1 = os.getcwd().split('AirCurrency')[0]  # 系统目录
    path_2 = 'AirCurrency/'  # 项目目录
    command_set = 'python3 run.py'  # 启动文件
    print('*->操作系统目录:{}'.format(path_1))
    print('*->项目目录:{}'.format(path_2))
    c = 'cd ~ ; cd {} ; ls ; {}'.format(path_1 + path_2, command_set)
    os.system(c)

    print('结束时间:{}'.format(datetime.now()))


if __name__ == '__main__':
    print('CarryTask start...')
    sched.start()
