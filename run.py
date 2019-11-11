# -*- coding: utf-8 -*-
# @Time    : 2019-10-07 15:16
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : run.py
# @Software: PyCharm

import os
import sys

# 终端执行
path_1 = os.getcwd().split('AirCurrency')[0]
path_2 = 'AirCurrency/'
path = path_1 + path_2
sys.path.append(path)
print(path)


def ter_start():
    # 终端命令穿参
    ter_param = sys.argv[1:]
    if len(ter_param) != 0:
        print(ter_param)
        p = ter_param[0]
        print(p, type(p))

        if p == 'all':
            "执行所有用例"
            print('all -> 执行所有用例')
            file_prefix = 'test_*.py'
            return file_prefix

        if p == 'okex':
            """执行okex"""
            print('okex case')
            file_prefix = 'test_003_OrderAccuracy_001_OKEX.py'
            return file_prefix

        if p == 'bitfinex':
            """执行bitfinex"""
            print('bitfinex case')
            file_prefix = 'test_003_OrderAccuracy_002_BitFinex.py'
            return file_prefix

        if p == 'bitmex':
            """执行bitmex"""
            print('bitmex case')
            file_prefix = 'test_003_OrderAccuracy_003_BitMex.py'
            return file_prefix

        else:
            print('参数错误...')
            exit()
    else:
        print('else -> all test case')
        # file_prefix = 'test_003_OrderAccuracy_001_OKEX.py'
        # file_prefix = 'test_003_OrderAccuracy_002_BitFinex.py'
        # file_prefix = 'test_003_OrderAccuracy_*.py'
        file_prefix = 'test_999_TestRunEnv.py'
        # return 'test_*.py'
        return file_prefix


report_dir = './reports'  # 报告路径
test_dir = './case/V2'  # 测试路径
file_prefix = ''  # 文件前缀

file_prefix = ter_start()

import time

import unittest

from common.HTMLTestReportCN import HTMLTestRunner
from config.config import *

R = redis_obj(3)
if not R.get('RUN_ENV'):
    R.set('RUN_ENV', 'dev')

print('报告路径:{}\n测试路径:{}\n文件前缀:{}\n'.format(report_dir, test_dir, file_prefix))

# 测试路径，匹配规则
discover = unittest.defaultTestLoader.discover(test_dir, pattern=file_prefix)

# 时间拼接报告名称
if R.get('RUN_ENV') == 'pro':
    ll = 'pro'
else:
    ll = 'dev'
now = time.strftime('%Y-%m-%d %H:%M:%S')
test_rp = '测试报告_{} {}_.html'.format(ll, now)
report_name = report_dir + '/' + test_rp

# 打开-生成测试报告
with open(report_name, 'wb') as f:
    print('f:', f)
    runner = HTMLTestRunner(stream=f, title='自动化测试报告', description='回归测试')
    runner.run(discover)
    f.close()

    if SEND_MAIL:
        from common.PublicFunc import latest_report, send_mail

        print('查找最新报告')
        latest_report = latest_report(report_dir)
        # print(latest_report)
        print('发送报告到邮箱')
        send_mail(latest_report)

if __name__ == '__main__':
    pass
