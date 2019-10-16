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


def as_num(number, prec=20):
    """
    解决科学计数不现实为直观小数
    :param number:
    :param prec:
    :return:
    """
    import decimal
    import math
    ctx = decimal.Context()
    ctx.prec = prec
    if 'E' in str(number) or 'e' in str(number):  # 判断时候为科学计数
        # n = format(ctx.create_decimal(str(number)), 'f')
        return format(ctx.create_decimal(str(number)), 'f')
    else:
        # print(number, type(number))
        return number


def cnmd(d):
    d2 = {}
    for k, v in d.items():
        d2[v[0]] = v[1]
    print(d2)
    print(sorted(d2.items(), key=lambda x: x[0]))
    print(sorted(d2.items(), key=lambda x: x[0])[-1][1])
    return sorted(d2.items(), key=lambda x: x[0])[-1][1]


def count_list_max_len(list):
    """
    取出list中 出现长度 最多的 任意值

    key:value
    长度:[长度,下标]

    :param list:
    :return:
    """
    d = {}
    for i in list:

        if not d.get(len(str(i))):
            d[len(str(i))] = [1, '{}'.format(i)]
        else:
            n1 = d.get(len(str(i)))[0]
            n2 = i
            # print('n1', n1)
            # print('n2', n2)
            d[len(str(i))] = [n1 + 1, n2]
    print(d)
    return d


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
        """获取交易所所有Symbol -> 储存至Redis"""
        R.flushall()
        print('redis db8 flushall .....')
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

    # @unittest.skip('pass')
    def test_004(self):
        """
        1.从 Redis Symbol List 中提取逐一对比 用于 与 orderbook 精度 对比
            错误 -> 记录Redis
            查看错误
        2.根据需要交易币对准备买入金额
        3.交易
        """

        # list_c = 60
        # sy_ob = 'okex:spot_list_'

        error_num = 0
        for i in range(1, list_c + 1):
            print(i)
            n = "%05d" % i
            print(n, type(n))

            dic_obj = eval('(' + R.get(sy_ob + n) + ')')
            print('-----moneyPrecision-----')
            print(dic_obj, type(dic_obj))
            print(dic_obj['moneyPrecision'])

            print('-----orderbook-----')
            jd_list = get_url_order_book('okex:spot', dic_obj['symbol']).json()['data']
            print('asks list ->>>\n', jd_list['asks'])
            print('bids list ->>>\n', jd_list['bids'])
            new_asks = [as_num(i[0]) for i in jd_list['asks']]
            new_bids = [as_num(i[0]) for i in jd_list['bids']]
            print('asks 价格 list ->>>\n', new_asks)
            print('bids 价格 list ->>>\n', new_bids, type(new_bids))
            asks_and_bids = new_asks + new_bids
            print('合并价格 ->>>\n ', asks_and_bids)

            # 排序反取 与 切出精度
            asks_and_bids_c = str(cnmd(count_list_max_len(asks_and_bids)))
            # asks_and_bids_c = str(count_list_max_len(asks_and_bids)).split('.')[1]

            print('-----精度提取-----')
            moneyPrecision_c = dic_obj['moneyPrecision'].split('.')[1]

            print('moneyPrecision - > {} -> 精度:{}'.format(dic_obj['moneyPrecision'], moneyPrecision_c))
            print('买卖平均精度:{}'.format(asks_and_bids_c))

            if len(moneyPrecision_c) != len(asks_and_bids_c.split('.')[1]):
                d = {
                    '币对:moneyPrecision': str(dic_obj['moneyPrecision']),
                    'OrderBook精度': asks_and_bids_c,
                }
                R.set('error_dic_obj_{}'.format(i), str(d))
                print('======记录错误精度 -> {} ======'.format(n))
                error_num += 1
        # if error_num != 0:
        #     print('发现错误的错误精度,明细查看Redis')
        #     assert error_num == 0
        # else:
        #     print(''.format(error_num))

    @unittest.skip('pass')
    def test_005(self):
        """1"""

    @unittest.skip('pass')
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
