# -*- coding: utf-8 -*-
# @Time    : 2019-10-07 17:39
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_002_Order01.py
# @Software: PyCharm

from all_import import *
from config.data.test_data import *
from config.config import R

"""

币币 -> 下单/挂单
杠杆 -> 下单/挂单
永续 -> 下单/挂单
交割 -> 下单/挂单

generating_orders -> 生产需要测试的订单类型
"""


def generating_orders(exchange=None, exchangeType=None, postType=None, side=None):
    """
    :param exchange:        交易所
    :param exchangeType:    交易类型  币币-> spot, 杠杆-> margin, 交割-> future, 永续-> swap
    :param postType:                 默认-> normal , 吃单-> post_only
    :param side:            交易方向
    :return:
    """

    exchange = 'okex'
    exchangeType = 'spot'
    postType = 'normal'
    side = 'buy'

    """
    永续/交割:
        "qty": "1" 整数张
        "symbol":"trx_usd_this_week",当周
        "symbol":"trx_usd_next_week",次周
        "symbol":"trx_usd_quarter",季度
    """

    d = {
        "accountId": accountId,
        "exchange": exchange,
        "exchangeType": exchangeType,
        "postType": postType,
        "price": "1",
        "qty": "1",
        "side": side,
        "symbol": "ltc_okb",
        "type": "limit"
    }

    if exchangeType == 'spot':
        print('func -> generating_orders data -> spot')
        result = requests.post(placeOrder, json=d, headers=header)
    if exchangeType == 'margin':
        print('func -> generating_orders data -> margin')
    if exchangeType == 'future':
        print('func -> generating_orders data -> future')
    if exchangeType == 'swap':
        print('func -> generating_orders data -> swap')

    return result


# 查询需要交易币对资产
def assets_contrast(exchangeType, symbol_l, symbol_r):
    """
    okb -> eos

    :param exchangeType:    交易类型
    :param symbol_1:        币对L -> eos
    :param symbol_2:        币对R -> okb
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

    return {
        'total': float(total),
        'free': float(free),
    }


#  查看订单状态
def check_order(exchange, exchangeType, orderId, symbol):
    j = {
        "accountId": accountId,
        "customId": "",
        "exchange": exchange,
        "exchangeType": exchangeType,
        "orderId": orderId,
        "readFromCache": 'true',
        "symbol": symbol
    }

    result = requests.post(getOrderById, json=j, headers=header)
    print(result.json())
    return result.json()['data']['status']


# 数据处理
def bl8(n):
    """
    保留8位小数
    :param n:
    :return:
    """
    return round(float(n), 8)


class TestPlaceOrderReverseLogic(StartEnd):
    """Place Order Reverse logic"""

    """
    test_000 ~ test_005: -> 查询参数异常逻辑
    test_006 ~ test_026: -> 下单参数异常逻辑
    test_027 ~ test_037: -> 撤单参数异常逻辑
    
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
        print('调用:TestPlaceOrderForwardLogic -> test_004_PlaceOrderActive_000 生成挂单')
        TestPlaceOrderForwardLogic().test_004_PlaceOrderActive_000()

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


class TestPlaceOrderForwardLogic(StartEnd):
    """Place Order Forward logic"""

    def test_001_clear_db_08(self):
        """测试数据init"""
        R.flushall()
        print('flushall.....')

    def test_002_PlaceOrder_data_001(self):
        """币币:交易前金额"""
        pre_transaction = assets_contrast('spot', 'eos', 'okb')
        R.set('pre_total', round(float(pre_transaction['total']), 8))
        R.set('pre_free', round(float(pre_transaction['free']), 8))

    def test_003_PlaceOrder_data_002(self):
        """币币:交易后金额"""
        post_transaction = assets_contrast('spot', 'eos', 'okb')
        R.set('post_total', round(post_transaction['total'], 8))
        R.set('post_free', round(post_transaction['free'], 8))

    def test_004_PlaceOrderActive_000(self):
        """测试-币币:偏离交易下单 -> buy【挂单】 测试:前后金额增加/减少"""

        """交易前"""
        self.test_002_PlaceOrder_data_001()

        """生成订单"""
        result = generating_orders()
        print(result.json())
        assert_json(result.json(), 'code', 1000)
        assert_json(result.json(), 'message', '下单成功')
        assert_json(result.json(), 'success', True)
        print('test place order success')

        """测试数据存储"""
        print(float(result.json()['data']['price']))
        R.set('price', float(result.json()['data']['price']))
        R.set('orderId', result.json()['data']['orderId'])
        R.set('exchangeType', result.json()['data']['exchangeType'])
        R.set('symbol', result.json()['data']['symbol'])
        print('save db success')

        """查看订单状态"""
        exchangeType = result.json()['data']['exchangeType']
        orderId = result.json()['data']['orderId']
        symbol = result.json()['data']['symbol']
        from time import sleep
        sleep(1)
        order_status = check_order('okex', exchangeType, orderId, symbol)
        print(order_status)
        print('check order status success')

        """交易后"""
        self.test_003_PlaceOrder_data_002()

        """检查金额"""
        if order_status == 'active':
            print('挂单')
            print(R.get('pre_free'), type(R.get('pre_free')))
            print(R.get('post_free'), type(R.get('post_free')))
            print(R.get('price'), type(R.get('price')))
            print(bl8(R.get('pre_free')), type(bl8(R.get('pre_free'))))

            pre_free = bl8(R.get('pre_free'))
            post_free = bl8(R.get('post_free'))
            price = bl8(R.get('price'))
            assert round(pre_free, 8) == round(post_free + price, 8)
            print('断言结束')
            print('Contrast of transaction amount before and after normal')

        # if order_status == '':
        #     print('撤销')
        # if order_status == '':
        #     print('下单成功')
        # else:
        #     print('测试数据错误')
        # self.test_PlaceOrder_001()

    def test_005_PlaceOrderActive_001(self):
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


if __name__ == '__main__':
    unittest.main()
