# -*- coding: utf-8 -*-
# @Time    : 2019-10-30 14:37
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : CarryTask.py
# @Software: PyCharm

import os

import time

from datetime import date, datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from config.config import redis_obj

sched = BlockingScheduler()

path_1 = os.getcwd().split('AirCurrency')[0]  # 系统目录
path_2 = 'AirCurrency/'  # 项目目录

print(path_1)

R = redis_obj(3)
if not R.get('RUN_ENV'):
    R.set('RUN_ENV', 'dev')


def start_task():
    """
    执行unittest
    :return:
    """
    print('当前运行环境:{}'.format(R.get('RUN_ENV')))
    command_set = 'python3 run.py'  # 启动文件
    print('*->操作系统目录:{}'.format(path_1))
    print('*->项目目录:{}'.format(path_2))
    c = 'cd ~ ; cd {} ; ls ; {}'.format(path_1 + path_2, command_set)
    os.system(c)


@sched.scheduled_job('cron', hour=6, minute=1, second=1)
@sched.scheduled_job('cron', hour=18, minute=16, second=59)
def cron_task_dev():
    print('开始时间:{}'.format(datetime.now()))

    print('环境变量{}'.format(R.get('RUN_ENV')))
    start_task()  # 执行 dev

    # print('=' * 99)
    # R.set('RUN_ENV', 'pro')
    # print('环境变量{}'.format(R.get('RUN_ENV')))
    #
    # start_task()  # 执行 pro
    # R.set('RUN_ENV', 'dev')
    # print('环境变量{}'.format(R.get('RUN_ENV')))

    print('结束时间:{}'.format(datetime.now()))

    print('cp reports to web ')
    p = path_1 + path_2
    c = 'cp -r {}reports/. {}/app/static/'.format(p, path_1 + 'AirCurrencyWeb')
    os.system(c)
    print('done')


if __name__ == '__main__':
    print('CarryTask start...')
    sched.start()
