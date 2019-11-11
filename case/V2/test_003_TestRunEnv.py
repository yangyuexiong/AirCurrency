# -*- coding: utf-8 -*-
# @Time    : 2019-11-07 10:12
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_003_TestRunEnv.py
# @Software: PyCharm


from all_import import *
from config.data.test_data import *


class TestRunEnv(StartEnd):
    """测试运行环境"""

    def test_001(self):
        """1"""
        print(BaseUrl)


if __name__ == '__main__':
    unittest.main()
