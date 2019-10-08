# -*- coding: utf-8 -*-
# @Time    : 2019-10-07 17:39
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_002_Order.py
# @Software: PyCharm

from all_import import *
from data.Order.data import *
from data.Common.data import *


class TestOrder(StartEnd):
    """下单"""
    data = d

    def test_order_000(self):
        """成功下单"""
        header['trade_sToken'] = sToken
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 1000)
        assert_json(result.json(), 'message', '下单成功')
        assert_json(result.json(), 'success', True)

    def test_order_001(self):
        """sToken为空下单"""
        header['trade_sToken'] = ""
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2002)
        assert_json(result.json(), 'success', False)

    def test_order_002(self):
        """错误sToken下单"""
        header['trade_sToken'] = sToken + 'xxx'
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2002)
        assert_json(result.json(), 'success', False)

    def test_order_003(self):
        """错误ID或ID为空下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['accountId'] = '6666'
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2002)
        assert_json(result.json(), 'success', False)

        self.data['accountId'] = ''
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)

    def test_order_004(self):
        """错误交易所或空参数下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['exchange'] = 'test......'
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2100)
        assert_json(result.json(), 'success', False)

        self.data['exchange'] = ''
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)

    def test_order_005(self):
        """错误子市场或空参数下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['exchangeType'] = '111'
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2103)
        assert_json(result.json(), 'message', '系统中没有这个子市场')
        assert_json(result.json(), 'success', False)

        self.data['exchangeType'] = ''
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)

    @unittest.skip('postType 参数没有校验')
    def test_order_006(self):
        """错误的postType下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['postType'] = '99999'
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())

    @unittest.skip('postType 为空默认 normal')
    def test_order_006_01(self):
        """postType为空下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['postType'] = ''
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())

    def test_order_007(self):
        """price为空下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['price'] = ''
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)

    @unittest.skip('price 错误参数没有校验')
    def test_order_008(self):
        """错误的price下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['price'] = 'x'
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())

    def test_order_009(self):
        """大于可买入个数下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['qty'] = '99999'
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2000)
        assert_json(result.json(), 'success', False)

    def test_order_010(self):
        """买入个数为空下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['qty'] = ''
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)

    @unittest.skip('qty 错误参数没有校验')
    def test_order_011(self):
        """错误的买入个数下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['qty'] = 'x'
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())

    def test_order_012(self):
        """错误交易方向下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['side'] = 'test......'
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2104)
        assert_json(result.json(), 'success', False)

    def test_order_013(self):
        """交易方向为空参数下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['side'] = ''
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)

    def test_order_014(self):
        """币对错误下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['symbol'] = 'xxx'
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2000)
        assert_json(result.json(), 'success', False)

    def test_order_015(self):
        """币对错误为空"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['symbol'] = ''
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)

    @unittest.skip('type 为空默认 limit')
    def test_order_016(self):
        """错误的type下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['type'] = 'test......'
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())

    def test_order_017(self):
        """type为空下单"""
        self.data = reset_data(self.data)
        header['trade_sToken'] = sToken

        self.data['type'] = ''
        result = requests.post(placeOrder, json=self.data, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)


if __name__ == '__main__':
    unittest.main()
