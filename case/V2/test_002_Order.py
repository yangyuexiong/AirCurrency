# -*- coding: utf-8 -*-
# @Time    : 2019-10-07 17:39
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_002_Order01.py
# @Software: PyCharm

from time import sleep

from all_import import *
from config.data.test_data import *
from common.OrderFunc import *

R = redis_obj(9)


class PublicOrderFunc:
    """公共类"""

    result = ''
    active_list = []

    def clear_db_08(self):
        """测试数据init"""
        # R.flushall()
        R.flushdb()
        print('redis db8 flushall .....')

    def fund_status(self, x, exchangeType, symbol_l, symbol_r):
        """
        当前需要交易的币对或者期货余额

        :param x:               pre->交易前金额  post->交易后金额
        :param exchangeType:    交易类型-> spot, margin, future, swap
        :param symbol_l:        币对L -> eos
        :param symbol_r:        币对R -> okb
        :return:
        """

        j = {
            "accountId": accountId
        }
        total = 0
        free = 0
        result = requests.post(getAsset, json=j, headers=header)
        # print(result.json()['data']['position']['spot'])
        for i in result.json()['data']['position'][exchangeType]:
            if i['symbol'] == symbol_r:
                print(i)
                print('total:', i['total'])
                print('free :', i['free'])
                total = i['total']
                free = i['free']
                # print(total)
                # print(free)
                print(float(total))
                print(float(free))

        if x == 'pre':
            R.set('pre_total', round(float(total), 8))
            R.set('pre_free', round(float(free), 8))
        elif x == 'post':
            R.set('post_total', round(float(total), 8))
            R.set('post_free', round(float(free), 8))

        print('{} -> fund_status end'.format(x))

    def assert_balance(self, order_status, ty='buy'):
        """状态与余额"""
        msg = 'Contrast of transaction amount before and after normal -> {}'.format(order_status)

        print(R.get('pre_free'), type(R.get('pre_free')))
        print(R.get('post_free'), type(R.get('post_free')))
        print(R.get('price'), type(R.get('price')))
        print(bl8(R.get('pre_free')), type(bl8(R.get('pre_free'))))
        if order_status == 'active':
            print('挂单')
            pre_free = bl8(R.get('pre_free'))
            post_free = bl8(R.get('post_free'))
            price = bl8(R.get('price'))
            assert round(pre_free, 8) == round(post_free + price, 8)
            print(msg)
            return 'active'

        elif order_status == 'cancelled':
            print('撤销')
            print(msg)
            return

        elif order_status == 'completed':
            print('下单成功')
            pre_total = bl8(R.get('pre_total'))
            post_total = bl8(R.get('post_total'))
            price = bl8(R.get('price'))
            print('原金额:{}\n使用金额:{}\n下单后金额:{}'.format(pre_total, price, post_total))
            sc = pre_total * 0.001
            if ty == 'buy':
                assert round(pre_total, 8) == round(post_total + price, 8)
            elif ty == 'sell':
                assert round(pre_total, 8) == round(post_total + price, 8)
            print(msg)
            return 'completed'

        else:
            print('测试数据错误-> {}'.format(order_status))
            assert 1 == 1 - 1

    def go_active(self):
        """生成订单 -> 挂单"""
        result = generating_orders(
            exchange='okex',
            exchangeType='spot',
            postType='normal',
            price='1',
            qty='1',
            side='buy',
            symbol='ltc_okb'
        )
        print(result.json())
        assert_json(result.json(), 'code', 1000)
        assert_json(result.json(), 'message', '下单成功')
        assert_json(result.json(), 'success', True)
        print('test place order success')
        self.result = result

    def save_test_data_to_db(self, result):
        """保存测试数据"""
        print(float(result.json()['data']['price']))
        R.set('price', float(result.json()['data']['price']))
        R.set('orderId', result.json()['data']['orderId'])
        R.set('exchangeType', result.json()['data']['exchangeType'])
        R.set('symbol', result.json()['data']['symbol'])
        print('save db success')


@unittest.skip('PASS')
class TestPlaceOrderForwardLogic(StartEnd, PublicOrderFunc):
    """Place Order Forward logic"""

    def test_001_PlaceOrderActive_001(self):
        """测试-币币:偏离交易下单 -> buy【挂单】 测试:前后金额增加/减少"""

        self.clear_db_08()

        """交易前"""
        self.fund_status('pre', 'spot', 'eos', 'okb')

        """生成订单"""
        self.go_active()

        """测试数据存储"""
        result = self.result
        self.save_test_data_to_db(result)

        """查看订单状态"""
        exchangeType = result.json()['data']['exchangeType']
        orderId = result.json()['data']['orderId']
        symbol = result.json()['data']['symbol']
        sleep(1)
        order_status = check_order('okex', exchangeType, orderId, symbol)
        print(order_status)
        print('check order status success')

        x = get_active_orders().json()['data'][0]['orderId']

        """交易后"""
        self.fund_status('post', 'spot', 'eos', 'okb')

        """检查状态金额"""
        self.assert_balance(order_status)

    def test_002_PlaceOrderActive_002(self):
        """测试-币币:交易 -> buy【撤单】前后金额增加/减少"""

        co['orderId'] = R.get('orderId')
        co['exchangeType'] = R.get('exchangeType')
        co['symbol'] = R.get('symbol')

        result = requests.post(cancelOrder, json=co, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 1000)
        assert_json(result.json(), 'message', '撤单成功')
        assert_json(result.json(), 'success', True)
        print('撤单 assert end')

        pre_free = bl8(R.get('pre_free'))
        post_free = bl8(R.get('post_free'))
        price = bl8(R.get('price'))

        assert round(pre_free, 8) == round(post_free + price, 8)
        print('free success')

        pre_total = bl8(R.get('pre_total'))
        post_total = bl8(R.get('post_total'))
        print(pre_total)
        print(post_total)
        assert round(pre_total, 8) == round(post_total, 8)
        print('total success')
        self.clear_db_08()

    def test_003_PlaceOrderActive_003(self):
        """测试-币币:交易 -> buy【成交】前后金额增加/减少"""


@unittest.skip('PASS')
class TestPlaceOrderReverseLogic(StartEnd, PublicOrderFunc):
    """Place Order Reverse logic"""

    """
    test_000 ~ test_005: -> 查询参数异常逻辑
    test_006 ~ test_026: -> 下单参数异常逻辑
    test_027 ~ test_037: -> 撤单参数异常逻辑
    test_038 ~ test_049: -> 状态参数异常逻辑
    test_050 ~ test_060: -> 挂单列表异常逻辑
    
    """
    j = {
        "accountId": accountId
    }

    # 币币下单
    bb = {
        "accountId": accountId,
        "exchange": "okex",
        "exchangeType": "spot",
        "postType": "normal",
        "price": "1",
        "qty": "1",
        "side": "buy",
        "symbol": "ltc_okb",
        "type": "limit"
    }

    # 撤单
    class_co = {
        "accountId": accountId,
        "customId": "",
        "exchange": "okex",
        "exchangeType": "",
        "orderId": "",
        "symbol": ""

    }

    def test_000(self):
        """还原测试参数"""
        j = {
            "accountId": accountId
        }
        self.j = j
        header['trade_sToken'] = sToken

    def test_001(self):
        """错误accountId查询资产"""
        self.j['accountId'] = 999999
        result = requests.post(getAsset, json=self.j, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2002)
        assert_json(result.json(), 'message', '系统中不存在这个账户或这个账户的key不可用')
        assert_json(result.json(), 'success', False)
        print('test error accountId end')

    def test_002(self):
        """accountId为空"""
        self.j['accountId'] = ''
        result = requests.post(getAsset, json=self.j, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)
        print('test none accountId end')

    def test_003(self):
        """错误的key查询资产"""
        j = {
            "accountIdxxxx": accountId
        }
        result = requests.post(getAsset, json=j, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)
        print('test none key end')

    def test_004(self):
        """错误的sToken查询资产"""
        self.test_000()
        header['trade_sToken'] = 'test ......'
        result = requests.post(getAsset, json=self.j, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2002)
        assert_json(result.json(), 'success', False)
        print('test error sToken end')

    def test_005(self):
        """sToken为空查询资产"""
        self.test_000()
        header['trade_sToken'] = ''
        result = requests.post(getAsset, json=self.j, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2002)
        assert_json(result.json(), 'message', 'header没有传入sToken或sToken为空')
        assert_json(result.json(), 'success', False)
        print('test none sToken end')

    """----------分割线----------"""

    def test_006(self):
        """sToken为空下单"""
        header['trade_sToken'] = ""
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2002)
        assert_json(result.json(), 'success', False)
        print('test none sToken place order end')

    def test_007(self):
        """错误sToken下单"""
        header['trade_sToken'] = sToken + 'xxx'
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2002)
        assert_json(result.json(), 'success', False)
        print('test error sToken place order end')

    def test_008(self):
        """错误accountId下单"""

        self.bb['accountId'] = 'okccccc'
        header['trade_sToken'] = sToken
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2002)
        assert_json(result.json(), 'success', False)
        self.bb['accountId'] = accountId
        print('test error accountId place order end')

    def test_009(self):
        """accountId 为空下单"""
        self.bb['accountId'] = ''
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)
        self.bb['accountId'] = accountId
        print('test none accountId place order end')

    def test_010(self):
        """错误交易所下单"""
        header['trade_sToken'] = sToken
        self.bb['exchange'] = 'test......'
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2100)
        assert_json(result.json(), 'message', '系统中没有该交易所')
        assert_json(result.json(), 'success', False)
        print('test error exchange place order end')

    def test_011(self):
        """交易所参数为空下单"""
        header['trade_sToken'] = sToken
        self.bb['exchange'] = ''
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)
        self.bb['exchange'] = 'okex'
        print('test none exchange place order end')

    def test_012(self):
        """错误子市场下单"""
        header['trade_sToken'] = sToken
        self.bb['exchangeType'] = '111'
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2103)
        assert_json(result.json(), 'message', '系统中没有这个子市场')
        assert_json(result.json(), 'success', False)
        print('test error exchangeType place order end')

    def test_013(self):
        """子市场空参数下单"""
        header['trade_sToken'] = sToken
        self.bb['exchangeType'] = ''
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)
        self.bb['exchangeType'] = 'spot'
        print('test none exchangeType place order end')

    @unittest.skip('postType 参数没有校验')
    def test_014(self):
        """错误的postType下单"""
        header['trade_sToken'] = sToken
        self.bb['postType'] = '99999'
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())

    @unittest.skip('postType 为空默认 normal')
    def test_015(self):
        """postType为空下单"""
        header['trade_sToken'] = sToken
        self.bb['postType'] = ''
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())

    def test_016(self):
        """price 为空下单"""
        header['trade_sToken'] = sToken
        self.bb['price'] = ''
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)
        self.bb['price'] = '1'
        print('test none price place order end')

    @unittest.skip('price 错误参数没有校验')
    def test_017(self):
        """错误的price下单"""
        header['trade_sToken'] = sToken
        self.bb['price'] = 'x'
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())

    def test_018(self):
        """大于可买入个数下单"""
        header['trade_sToken'] = sToken
        self.bb['qty'] = '99999'
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2000)
        assert_json(result.json(), 'success', False)
        print('test >qty place order end')

    def test_019(self):
        """买入个数为空下单"""
        header['trade_sToken'] = sToken
        self.bb['qty'] = ''
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)
        self.bb['qty'] = '1'
        print('test none qty place order end')

    @unittest.skip('qty 错误参数没有校验')
    def test_020(self):
        """错误的买入个数下单"""
        header['trade_sToken'] = sToken
        self.bb['qty'] = 'x'
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())

    def test_021(self):
        """错误交易方向下单"""
        header['trade_sToken'] = sToken
        self.bb['side'] = 'test......'
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2104)
        assert_json(result.json(), 'success', False)
        print('test error side  place order end')

    def test_022(self):
        """交易方向为空参数下单"""
        header['trade_sToken'] = sToken
        self.bb['side'] = ''
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)
        self.bb['side'] = 'buy'
        print('test none side  place order end')

    def test_023(self):
        """币对错误下单"""
        header['trade_sToken'] = sToken
        self.bb['symbol'] = 'xxx'
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2000)
        assert_json(result.json(), 'success', False)
        print('test error symbol place order end')

    def test_024(self):
        """币对错误为空"""
        header['trade_sToken'] = sToken
        self.bb['symbol'] = ''
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)
        self.bb['symbol'] = 'ltc_okb'
        print('test none symbol place order end')

    @unittest.skip('type 为空默认 limit')
    def test_025(self):
        """错误的type下单"""
        header['trade_sToken'] = sToken
        self.bb['type'] = 'test......'
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())

    def test_026(self):
        """type为空下单"""
        header['trade_sToken'] = sToken
        self.bb['type'] = ''
        result = requests.post(placeOrder, json=self.bb, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)
        self.bb['type'] = 'limit'
        print('test none type place order end')

    def test_027(self):
        """生成挂单用于测单测试"""
        print('调用:TestPlaceOrderForwardLogic -> test_001_PlaceOrderActive_001 生成挂单')
        TestPlaceOrderForwardLogic().test_001_PlaceOrderActive_001()

    def test_028(self):
        """错误 accountId 撤单"""
        co['accountId'] = '999999'
        co['orderId'] = R.get('orderId')
        co['exchangeType'] = R.get('exchangeType')
        co['symbol'] = R.get('symbol')
        result = requests.post(cancelOrder, json=co, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2002)
        assert_json(result.json(), 'success', False)
        co['accountId'] = accountId
        print('test error accountId cancel order end')

    def test_029(self):
        """accountId 为空 撤单"""
        co['accountId'] = ''
        co['orderId'] = R.get('orderId')
        co['exchangeType'] = R.get('exchangeType')
        co['symbol'] = R.get('symbol')
        result = requests.post(cancelOrder, json=co, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)
        co['accountId'] = accountId
        print('test none accountId cancel order end')

    def test_030(self):
        """错误 orderId 撤单"""
        co['orderId'] = '12312412421412412412'
        co['exchangeType'] = R.get('exchangeType')
        co['symbol'] = R.get('symbol')
        result = requests.post(cancelOrder, json=co, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2000)
        assert_json(result.json(), 'success', False)
        print('test error orderId cancel order end')

    def test_031(self):
        """orderId 为空 撤单"""
        co['orderId'] = ''
        co['exchangeType'] = R.get('exchangeType')
        co['symbol'] = R.get('symbol')
        result = requests.post(cancelOrder, json=co, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'message', '订单号与自定义订单号不能同时为空')
        assert_json(result.json(), 'success', False)
        print('test none orderId cancel order end')

    def test_032(self):
        """错误 exchangeType 撤单"""
        co['orderId'] = R.get('orderId')
        co['exchangeType'] = 'test....'
        co['symbol'] = R.get('symbol')
        result = requests.post(cancelOrder, json=co, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2103)
        assert_json(result.json(), 'message', '系统中没有这个子市场')
        assert_json(result.json(), 'success', False)
        print('test error exchangeType cancel order end')

    def test_033(self):
        """exchangeType 为空 撤单"""
        co['orderId'] = R.get('orderId')
        co['exchangeType'] = ''
        co['symbol'] = R.get('symbol')
        result = requests.post(cancelOrder, json=co, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)
        print('test none exchangeType cancel order end')

    def test_034(self):
        """错误 symbol 撤单"""
        co['orderId'] = R.get('orderId')
        co['exchangeType'] = R.get('exchangeType')
        co['symbol'] = 'test_test'
        result = requests.post(cancelOrder, json=co, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2000)
        assert_json(result.json(), 'message',
                    '没有该币对:{}:{}:{}.'.format(co['exchange'], co['exchangeType'], co['symbol']))
        assert_json(result.json(), 'success', False)
        print('test error symbol cancel order end')

    def test_035(self):
        """symbol 为空 撤单"""
        co['orderId'] = R.get('orderId')
        co['exchangeType'] = R.get('exchangeType')
        co['symbol'] = ''
        result = requests.post(cancelOrder, json=co, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'message', '参数错误。参数名：symbol， 值：， 提示：交易对不能为空; ')
        assert_json(result.json(), 'success', False)
        print('test none symbol cancel order end')

    def test_036(self):
        """所有参数 为空 撤单"""
        co['orderId'] = ''
        co['exchangeType'] = ''
        co['symbol'] = ''
        result = requests.post(cancelOrder, json=co, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)
        print('test none params cancel order end')

    def test_037(self):
        """撤销订单还原测试数据"""
        header['trade_sToken'] = sToken
        co['orderId'] = R.get('orderId')
        co['exchangeType'] = R.get('exchangeType')
        co['symbol'] = R.get('symbol')
        result = requests.post(cancelOrder, json=co, headers=header)
        print(result.json())
        print('done')

    def test_038(self):
        """生成挂单测试数据用于查询订单"""
        self.go_active()  # 生成订单
        result = self.result
        self.save_test_data_to_db(result)  # 保存订单测试数据
        print('c test data order')

    def test_039(self):
        """错误 accountId 查询订单"""
        exchangeType = R.get('exchangeType')
        orderId = R.get('orderId')
        symbol = R.get('symbol')
        result = check_order('okex', exchangeType, orderId, symbol, a_id='999999')
        assert_json(result, 'code', 2002)
        assert_json(result, 'message', '系统中不存在这个账户或这个账户的key不可用')
        assert_json(result, 'success', False)
        print('test error accountId check order end')

    def test_040(self):
        """accountId 为空 查询订单"""
        exchangeType = R.get('exchangeType')
        orderId = R.get('orderId')
        symbol = R.get('symbol')
        result = check_order('okex', exchangeType, orderId, symbol, a_id='')
        assert_json(result, 'code', 2001)
        assert_json(result, 'success', False)
        print('test none accountId check order end')

    def test_041(self):
        """错误 交易所 查询订单"""
        exchangeType = R.get('exchangeType')
        orderId = R.get('orderId')
        symbol = R.get('symbol')
        result = check_order('test...', exchangeType, orderId, symbol)
        assert_json(result, 'code', 2100)
        assert_json(result, 'message', '系统中没有该交易所')
        assert_json(result, 'success', False)
        print('test error exchange check order end')

    def test_042(self):
        """交易所 为空 查询订单"""
        exchangeType = R.get('exchangeType')
        orderId = R.get('orderId')
        symbol = R.get('symbol')
        result = check_order('', exchangeType, orderId, symbol)
        assert_json(result, 'code', 2001)
        assert_json(result, 'success', False)
        print('test none exchange check order end')

    def test_043(self):
        """错误 exchangeType 查询订单"""
        exchangeType = 'test......'
        orderId = R.get('orderId')
        symbol = R.get('symbol')
        result = check_order('okex', exchangeType, orderId, symbol)
        assert_json(result, 'code', 2103)
        assert_json(result, 'message', '系统中没有这个子市场')
        assert_json(result, 'success', False)
        print('test error exchangeType check order end')

    def test_044(self):
        """exchangeType 为空 查询订单"""
        exchangeType = ''
        orderId = R.get('orderId')
        symbol = R.get('symbol')
        result = check_order('okex', exchangeType, orderId, symbol)
        assert_json(result, 'code', 2001)
        assert_json(result, 'success', False)
        print('test error exchangeType check order end')

    def test_045(self):
        """错误 orderId 查询订单"""
        exchangeType = R.get('exchangeType')
        orderId = '999999999'
        symbol = R.get('symbol')
        result = check_order('okex', exchangeType, orderId, symbol)
        assert_json(result, 'code', 2000)
        assert_json(result, 'message', '没有该订单【{}】的存在'.format(orderId))
        assert_json(result, 'success', False)
        print('test error orderId check order end')

    def test_046(self):
        """orderId 为空 查询订单"""
        exchangeType = R.get('exchangeType')
        orderId = ''
        symbol = R.get('symbol')
        result = check_order('okex', exchangeType, orderId, symbol)
        assert_json(result, 'code', 2001)
        assert_json(result, 'success', False)
        print('test none orderId check order end')

    def test_047(self):
        """错误 symbol 查询订单"""
        exchangeType = R.get('exchangeType')
        orderId = R.get('orderId')
        symbol = 'test......'
        result = check_order('okex', exchangeType, orderId, symbol)
        assert_json(result, 'code', 2000)
        assert_json(result, 'success', False)
        print('test error symbol check order end')

    def test_048(self):
        """ symbol 为空 查询订单"""
        exchangeType = R.get('exchangeType')
        orderId = R.get('orderId')
        symbol = ''
        result = check_order('okex', exchangeType, orderId, symbol)
        assert_json(result, 'code', 2001)
        assert_json(result, 'success', False)
        print('test none symbol check order end')

    def test_049(self):
        """调用 TestPlaceOrderReverseLogic().test_037()"""
        TestPlaceOrderReverseLogic().test_037()

    def test_050(self):
        """1"""
        self.go_active()
        self.go_active()
        self.go_active()
        sleep(1)

    def test_051(self):
        """错误 accountId 查询活跃订单"""
        ao['accountId'] = '999999'
        result = requests.post(getActiveOrders, json=ao, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2002)
        assert_json(result.json(), 'message', "系统中不存在这个账户或这个账户的key不可用")
        assert_json(result.json(), 'success', False)
        print('test error accountId get active orders end')

    def test_052(self):
        """ accountId 为空 查询活跃订单"""
        ao['accountId'] = ''
        result = requests.post(getActiveOrders, json=ao, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'success', False)
        print('test none accountId get active orders end')
        ao['accountId'] = accountId

    def test_053(self):
        """错误 exchange 查询活跃订单"""
        print(ao)
        ao['exchange'] = 'test.....'
        result = requests.post(getActiveOrders, json=ao, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2100)
        assert_json(result.json(), 'message', '系统中没有该交易所')
        assert_json(result.json(), 'success', False)
        print('test error exchange get active orders end')

    def test_054(self):
        """ exchange 为空 查询活跃订单"""
        ao['exchange'] = ''
        result = requests.post(getActiveOrders, json=ao, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'message', '参数错误。参数名：exchange， 值：， 提示：交易所不能为空; ')
        assert_json(result.json(), 'success', False)
        print('test none exchange get active orders end')
        ao['exchange'] = 'okex'

    def test_055(self):
        """错误 exchangeType 查询活跃订单"""
        ao['exchangeType'] = 'test.....'
        result = requests.post(getActiveOrders, json=ao, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2103)
        assert_json(result.json(), 'message', '系统中没有这个子市场')
        assert_json(result.json(), 'success', False)
        print('test error exchangeType get active orders end')

    def test_057(self):
        """ exchangeType 为空 查询活跃订单"""
        ao['exchangeType'] = ''
        result = requests.post(getActiveOrders, json=ao, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'message', '参数错误。参数名：exchangeType， 值：， 提示：交易所子市场不能为空; ')
        assert_json(result.json(), 'success', False)
        print('test none exchangeType get active orders end')
        ao['exchangeType'] = 'spot'

    def test_058(self):
        """错误 readFromCache 查询活跃订单"""
        ao['readFromCache'] = 'test.....'
        result = requests.post(getActiveOrders, json=ao, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'message', '参数json格式错误，请检查后重试。')
        assert_json(result.json(), 'success', False)
        print('test error readFromCache get active orders end')

    def test_059(self):
        """readFromCache 为空 查询活跃订单"""
        ao['readFromCache'] = ''
        result = requests.post(getActiveOrders, json=ao, headers=header)
        print(result.json())
        assert_json(result.json(), 'code', 2001)
        assert_json(result.json(), 'message', '参数错误。参数名：readFromCache， 值：null， 提示：是否从缓存中读取不能为空; ')
        assert_json(result.json(), 'success', False)
        print('test none readFromCache get active orders end')
        ao['readFromCache'] = True

    def test_060(self):
        """撤销所有活跃订单"""
        ac_list = get_active_orders().json()['data']
        for i in ac_list:
            print(i)
            co['exchangeType'] = i['exchangeType']
            co['orderId'] = i['orderId']
            co['symbol'] = i['symbol']
            result = requests.post(cancelOrder, json=co, headers=header)
            print(result.json(), '')

    def test_999(self):
        """clear_db_08()"""
        self.clear_db_08()


@unittest.skip('pass-> 单元调试类')
class TestDevTest(StartEnd, PublicOrderFunc):
    """调试类"""

    # @unittest.skip('pass')
    def test_tx_001(self):
        """test_tx_001"""

        """
        1.获取交易前金额 -> 保存到reids
        2.获取当前价格
        3.买卖->储存订单信息
        4.判断订单状态
            (1)挂单->检查金额->撤单->查看该订单状态
            (2)成功->检查金额->卖出->查看该订单状态
        
        """
        self.fund_status('pre', 'spot', 'trx', 'okb')

        # 获取价格
        timely_buy = get_ticker('okex:spot', 'trx_okb').json()['data']['sell']
        result = generating_orders(
            exchange='okex',
            exchangeType='spot',
            postType='normal',
            price=timely_buy,
            qty='1',
            side='buy',
            symbol='trx_okb'
        )

        print(result.json())
        self.save_test_data_to_db(result)

        exchangeType = result.json()['data']['exchangeType']
        orderId = result.json()['data']['orderId']
        symbol = result.json()['data']['symbol']
        sleep(1)
        order_status = check_order('okex', exchangeType, orderId, symbol)
        print(order_status)

        self.fund_status('post', 'spot', 'trx', 'okb')

        r = self.assert_balance(order_status)
        if r == 'active':
            pass
        elif r == 'completed':
            pass
        elif r == 'cancelled':
            pass

    def test_tx_002(self):
        """test_tx_002"""

    def test_tx_003(self):
        """test_tx_003"""

    def test_tx_004(self):
        """test_tx_004"""

    def test_tx_005(self):
        """test_tx_005"""


if __name__ == '__main__':
    unittest.main()
