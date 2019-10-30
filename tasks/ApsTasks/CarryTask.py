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


@sched.scheduled_job('cron', hour=18, minute=8, second=59)
def cron_task():
    print(datetime.now())

    path_1 = os.getcwd().split('AirCurrency')[0]
    path_2 = 'AirCurrency/'
    command_set = 'python3 run.py'
    print('*->操作系统目录:{}'.format(path_1))
    print('*->项目目录:{}'.format(path_2))
    c = 'cd ~ ; cd {} ; ls ; {}'.format(path_1 + path_2, command_set)
    os.system(c)

    print(datetime.now())


if __name__ == '__main__':
    sched.start()
