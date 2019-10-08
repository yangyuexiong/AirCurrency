# -*- coding: utf-8 -*-
# @Time    : 2019-10-07 15:19
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : BaseUnit.py
# @Software: PyCharm

import unittest
import urllib3


class StartEnd(unittest.TestCase):

    def setUp(self):
        # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        print('======测试开始======')

    def tearDown(self):
        print('======测试结束======')
