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
        print('======Test start:{}======'.format(self))

    def tearDown(self):
        print('======End of test:{}======'.format(self))
