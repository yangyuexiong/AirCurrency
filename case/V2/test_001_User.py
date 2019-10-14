# -*- coding: utf-8 -*-
# @Time    : 2019-10-07 15:24
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_001_User.py
# @Software: PyCharm

from all_import import *
from data.User.data import *


@unittest.skip('pass-> TestWebToken')
class TestWebToken(StartEnd):
    """验证web会话"""

    def test_WebToken_001(self):
        """验证成功"""
        result = requests.get(verifyWebToken, headers=header)
        print(result.json())

        assert_json(result.json(), 'code', 1000)
        assert_json(result.json(), 'message', '验证成功')
        assert_json(result.json(), 'success', True)

    def test_WebToken_002(self):
        """验证失败"""
        header['webToken'] = 'xxx'
        result = requests.get(verifyWebToken, headers=header)
        print(result.json())

        assert_json(result.json(), 'code', 2000)
        assert_json(result.json(), 'message', '用户未登录！')
        assert_json(result.json(), 'success', False)

    def test_WebToken_003(self):
        """验证失败"""
        header['webToken'] = ''
        result = requests.get(verifyWebToken, headers=header)
        print(result.json())

        assert_json(result.json(), 'code', 2000)
        assert_json(result.json(), 'message', '参数错误！')
        assert_json(result.json(), 'success', False)


class TestGenToken(StartEnd):
    """生成sToken"""

    def test_sToken_001(self):
        """"""

    def test_sToken_002(self):
        """"""

    def test_sToken_003(self):
        """"""


class TestUserInfo(StartEnd):

    def test_userInfo_001(self):
        """"""


if __name__ == '__main__':
    unittest.main()
