# -*- coding: utf-8 -*-
# @Time    : 2019-10-07 15:16
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : run.py
# @Software: PyCharm


import unittest
from common.HTMLTestReportCN import HTMLTestRunner
import time
import sys
from config.config import *

# 终端执行
path = '/Users/yangyuexiong/Desktop/AirCurrency'
sys.path.append(path)

# 报告路径
report_dir = './reports'
# 测试路径
test_dir = './case/V2'
# test_dir = './case/v3.0_'
# 文件前缀
# file_prefix = 'test_*.py'
file_prefix = 'test_003_OrderAccuracy_OKEX.py'

if not C:
    file_prefix = ''

print('报告路径:{}\n测试路径:{}\n文件前缀:{}\n'.format(report_dir, test_dir, file_prefix))

# 测试路径，匹配规则
discover = unittest.defaultTestLoader.discover(test_dir, pattern=file_prefix)

# 时间拼接报告名称
now = time.strftime('%Y-%m-%d %H_%M_%S')
test_rp = '测试报告_{}_.html'.format(now)
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
        print(latest_report)
        print('发送报告到邮箱')
        send_mail(latest_report)

if __name__ == '__main__':
    pass
