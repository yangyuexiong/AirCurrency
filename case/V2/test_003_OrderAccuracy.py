# -*- coding: utf-8 -*-
# @Time    : 2019-10-15 10:39
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_003_OrderAccuracy.py
# @Software: PyCharm


from all_import import *
import shortuuid


# 获取交易所所有币的list
def get_url_symbol_list(exchange):
    """

    moneyPrecision -> 价格精度
    basePrecision  -> 数量精度
    minOrderSize   -> 落单数量
    minOrderValue  -> 价值

    :param exchange:  交易所:子市场 -> okex:spot
    :return:
    """
    kv = {
        'exchange': exchange
    }
    result = requests.get(Symbol_url, kv)
    # print(result.json()['data'][0])
    # print(result.json()['data'][1])
    print(type(result.json()['data']))

    v = result.json()['data']
    print(v)
    R.set(exchange, str(v))
    return


def get_url_order_book(exchange, symbol):
    """

    :param exchange:  交易所:子市场 -> okex:spot
    :param symbol:    币对: -> 如 btc_usdt
    :return:
    """
    kv = {
        'exchange': exchange,
        'symbol': symbol
    }
    result = requests.get(Orderbook, kv)
    print(result.json(), '\n')
    return result


# 分开保存每一个币种
def save_symbol_obj(s):
    """

    :param s: 交易所:子市场 -> okex:spot
    :return:
    """
    okex_spot_list = eval('(' + R.get(s) + ')')
    # print(okex_spot_list)

    list_obj = ''
    list_count = '{}_list_count'.format(s)
    print(list_count)
    print('obj count ->', len(okex_spot_list))
    new_list = zip(range(1, len(okex_spot_list) + 1), okex_spot_list)
    for k, v in new_list:
        print('key:', "%05d" % k)
        print('vaule:', v)
        R.set('{}_list_{}'.format(s, "%05d" % k), str(v))
    list_obj = '{}_list_{}'.format(s, "%05d" % k)
    R.set(list_count, len(okex_spot_list))
    return R.get(list_count), list_obj


class CommonFunc:
    """公共类"""

    def check_sy_kv(self, sy):
        """
        检查symbol参数

        :param sy:
        :return:

        """
        demo = {'exSymbol': 'knc_btc', 'symbol': 'knc_btc', 'exBaseCoin': 'knc', 'exMoneyCoin': 'btc',
                'baseCoin': 'knc',
                'moneyCoin': 'btc', 'basePrecision': '0.001', 'moneyPrecision': '0.0000001', 'minOrderSize': '1',
                'symbolType': 'spot', 'tradeType': 'knc', 'multiplier': '1'}

        if not sy.get('moneyPrecision') or not sy.get('basePrecision'):
            print('moneyPrecision 或 basePrecision 为 None')
            R.set('error_data_{}'.format(shortuuid.uuid()), str(sy))
            assert 1 == 1 - 1

        if float(sy.get('moneyPrecision')) <= 0 or float(sy.get('basePrecision')) <= 0:
            print('moneyPrecision 或 basePrecision 值 < 0')
            R.set('error_data_{}'.format(shortuuid.uuid()), str(sy))
            assert 1 == 1 - 1

        if not sy.get('minOrderSize') and not sy.get('minOrderValue'):
            print('minOrderSize 与 minOrderValue 为 None')
            R.set('error_data_{}'.format(shortuuid.uuid()), str(sy))
            assert 1 == 1 - 1

        if sy.get('minOrderSize'):
            if float(sy.get('minOrderSize')) <= 0:
                print('minOrderSize  <= 0')
                R.set('error_data_{}'.format(shortuuid.uuid()), str(sy))
                assert 1 == 1 - 1

        if sy.get('minOrderValue'):
            if float(sy.get('minOrderValue')) <= 0:
                print('minOrderValue  <= 0')
                R.set('error_data_{}'.format(shortuuid.uuid()), str(sy))
                assert 1 == 1 - 1


class TestOrderAccuracyForOKEX(StartEnd, CommonFunc):
    """okex"""

    def test_001(self):
        """获取Symbol -> 储存至Redis"""

        get_url_symbol_list('okex:spot')

    def test_002(self):
        """将Symbol list 中每一个币对象分开储存 -> Redis"""
        res = save_symbol_obj('okex:spot')
        print(res)
        print(res[0])
        print(res[1])
        global list_c
        global sy_ob
        list_c = int(res[0])
        sy_ob = res[1][:-5]

    def test_003(self):
        """检查币obj参数"""
        print(list_c)
        print(sy_ob)
        # list_c = 10
        # sy_ob = 'okex:spot_list_'
        for i in range(1, list_c + 1):
            print(i)
            n = "%05d" % i
            print(n, type(n))

            dic_obj = eval('(' + R.get(sy_ob + n) + ')')
            print(dic_obj, type(dic_obj))

            self.check_sy_kv(dic_obj)
        print('check success')

    def test_004(self):
        """
        从 Symbol List 中提取逐一对比 并交易
        根据币对准备买入金额
        """

    def test_005(self):
        """1"""
        print('-' * 100)
        r = get_url_order_book('okex:spot', 'btc_usdt').json()['data']['asks'][0][0]
        print(r)
        print(float(r))

    # @unittest.skip('pass')
    def test_099(self):
        """"""
        R.flushall()
        print('redis db8 flushall .....')

    @unittest.skip('pass')
    def test_0999(self):
        """1"""
        # print(R.get('okex:spot_list_00001'))
        i = 1
        print(eval('(' + R.get('okex:spot_list_' + str(("%05d" % i))) + ')'))


if __name__ == '__main__':
    unittest.main()
