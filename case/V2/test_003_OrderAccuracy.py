# -*- coding: utf-8 -*-
# @Time    : 2019-10-15 10:39
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_003_OrderAccuracy.py
# @Software: PyCharm

import shortuuid

from all_import import *
from config.data.test_data import *
from case.V2.test_002_Order import generating_orders, get_ticker, check_order


# 获取交易所所有币的list
def get_url_symbol_list(exchange):
    """

    moneyPrecision -> 价格精度
    basePrecision  -> 数量精度
    minOrderSize   -> 下单数量
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


def kexue_add(number, ll):
    # print('{:.{}f}'.format(number, ll))
    # print(type('{:.{}f}'.format(number, ll)))
    return '{:.{}f}'.format(number, ll)


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
    # print(sorted(d2.items(), key=lambda x: x[0]))
    # print(sorted(d2.items(), key=lambda x: x[0])[-1][1])
    return sorted(d2.items(), key=lambda x: x[0])[-1][1]


def last_add_2(s, sell=False):
    """

    :param s:      浮点数字符串
    :param sell:   卖加 买减
    :return:
    """
    k = '0.'
    s = as_num(s)
    print(s)

    """处理只有一位小数 或者 整数 例: 0.1"""
    if len(s.split('.')[1]) < 2:
        if sell:
            r = float(s) + 0.5  # 卖 +0.5 买 -0.5
            print(r)
            return str(r)
        else:
            r = float(s)
            if 0.5 > r > 0.2:
                r = round(r - 0.1, len(s) - 2)
                print(r)
                return str(r)

            else:
                print(r)
                return str(r)

    """处理一位小数以上 例: 0.01"""
    for i in s[2:]:
        k = k + '0'
    print(k)

    k1 = k[:-2]
    print('加减精度:', k1)

    k2 = k[len(k) - 2:-1]
    print('倒数第二位:', k2)

    k2_1 = int(k2) + 1
    print('倒数第二位 +1:', k2_1)

    k3 = k[len(s) - 1:]
    print('最后一位 默认 ->:', k3)

    ss = k1 + str(k2_1) + k3  # 例: "0.0" + "1" + "0"
    print('生成需要计数精度:', ss)

    if sell:
        r = kexue_add(float(s) + float(ss), len(s) - 2)  # 卖+1 买-1
        r = as_num(r)
        print(r)
        return str(r)
    else:
        if int(s[-2:-1]) == 0:  # 值的倒数第二位为 0 往后 推一位
            print(type(float(s)))
            msg = '{} - {}'.format(float(s), as_num(float(ss) / 10))
            print(msg)
            r = kexue_add((float(s)) - (float(ss) / 10), len(s) - 2)
            if r == 0:  # 计算结果为:0
                print('==0 ->', r, '返回 -> 0')
                return 0
            r = as_num(r)
            print('倒数第二位 == 0 且最后一位减法后结果 >0 :', r)
            return str(r)
        else:
            r = round(float(s) - float(ss), len(s) - 2)
            r = as_num(r)
            print('倒数第二位不为 0 减法:', r)
            print(r)
            return str(r)


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


# 获取余额
def get_user_asset():
    """获取余额"""
    j = {
        "accountId": accountId
    }
    result = requests.post(getAsset, json=j, headers=header)
    return result


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

    """
    test_004: 通过已有orderBook校验 -> moneyPrecision精度
    
    test_005: 通过下单测试 -> moneyPrecision
    """

    def test_001(self):
        """获取交易所所有Symbol -> 储存至Redis"""
        R.flushall()
        print('redis db8 flushall .....')

        with open(os.getcwd() + '/err_symbol_to_orderbook.json', 'w', encoding='utf-8') as f:
            f.write('')
        print('clear file -> err_symbol_to_orderbook.json')

        with open(os.getcwd() + '/err_symbol_to_order.json', 'w', encoding='utf-8') as f:
            f.write('')
        print('clear file -> err_symbol_to_order.json')

        get_url_symbol_list('okex:spot')

    def test_002(self):
        """将Symbol list 中每一个币对象分开储存 -> Redis"""
        res = save_symbol_obj('okex:spot')
        print(res)
        print(res[0])
        print(res[1])
        global list_c
        global sy_ob
        list_c = int(res[0])  # 总数
        sy_ob = res[1][:-5]  # 前缀

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
        """通过已有orderBook校验 -> moneyPrecision精度"""
        """
        1.从 Redis Symbol List 中提取逐一对比 用于 与 orderbook 精度 对比校验
            错误 -> 记录Redis -> 记录文件
            查看错误
        """

        # list_c = 1
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

            print('-----精度提取-----')
            moneyPrecision_c = dic_obj['moneyPrecision'].split('.')[1]

            print('moneyPrecision - > {} -> 精度:{}'.format(dic_obj['moneyPrecision'], moneyPrecision_c))
            print('买卖平均价格 -> {} -> 精度:{}'.format(asks_and_bids_c, asks_and_bids_c.split('.')[1]))

            if len(moneyPrecision_c) != len(asks_and_bids_c.split('.')[1]):
                d = {
                    'symbol_obj': dic_obj,
                    '该用例检验参数:moneyPrecision': str(dic_obj['moneyPrecision']),
                    'OrderBook精度': asks_and_bids_c,
                }
                with open(os.getcwd() + '/err_symbol_to_orderbook.json', 'a+') as f:
                    f.write(str(d) + '\n')

                R.set('error_dic_obj_{}'.format(i), str(d))
                print('======记录错误精度 -> {} ======'.format(n))
                error_num += 1

        with open(os.getcwd() + '/err_symbol_to_orderbook.json', 'r', encoding='utf-8') as f:
            fs = f.read()
            if not fs:
                print('not error symbol')
            else:
                print('error symbol ->>>\n')
                print(fs)
                assert not fs

        if error_num != 0:
            print('发现错误的错误精度,明细查看 -> Redis db8')
            assert error_num == 0
        else:
            print('error symbol number:{}'.format(error_num))

    def test_005(self):
        """通过下单测试 -> moneyPrecision"""
        """
        从Redis逐一取出币对进行下单
        1.获取币对obj
        2.根据需要交易币对准备买入金额
            查询余额 
                不足 -> 划转 
                足够 -> 下挂单
        3.下单 -> 挂单
            提取最少下单量 -> minOrderSize
            
        4.查看订单状态
        5.检验 moneyPrecision
        6.撤单
            (1)成功撤单
            (2)撤单失败 -> 订单成交 -> 记录日志
        """
        list_c = 421  # 调试
        sy_ob = 'okex:spot_list_'  # 调试
        # test_sy_ob = 'okex:spot_list_{}'.format("%05d" % 1)

        for i in range(1, list_c + 1):
            n = "%05d" % i
            pass
            # d = eval('(' + R.get(test_sy_ob) + ')')   # 调试单条币对
            d = eval('(' + R.get(sy_ob + n) + ')')
            sy = d['symbol']
            sy_l = d['symbol'].split('_')[0]
            sy_r = d['symbol'].split('_')[1]
            print(d, type(d))
            print('symbol -> {}'.format(sy))
            print('买入币种 -> {}'.format(sy_l))
            print('使用币种 -> {}'.format(sy_r))
            print('最少下单量 -> {}'.format(d['minOrderSize']))

            # r = get_user_asset().json()['data']['position']  # 余额情况
            # print(r['spot'])
            # print(r['margin'])
            # for i in r['spot']:
            #     print(i)

            # 买减->sell 卖加->buy
            p = get_ticker('okex:spot', sy).json()['data']['sell']
            print(p, type(p))
            p = last_add_2(p)
            print('下单金额:', p)

            r = generating_orders('okex', 'spot', 'normal', p, d['minOrderSize'], 'buy', sy)
            print(r.json())

            exchangeType = r.json()['data']['exchangeType']
            orderId = r.json()['data']['orderId']
            symbol = r.json()['data']['symbol']
            sleep(1)
            order_status = check_order('okex', exchangeType, orderId, symbol, all_json=True)

            obj_price = d['moneyPrecision']
            od_price = order_status['data']['price']
            print(obj_price, type(obj_price))
            print(od_price, type(od_price))
            print('=====校验订单精度=====')
            if len(obj_price.split('.')[1]) != len(od_price.split('.')[1]):
                with open(os.getcwd() + '/err_symbol_to_order.json', 'a+') as f:
                    f.write(str(d) + '\n' + str(order_status) + '\n')
            else:
                try:
                    print('=====订单精度校验通过=====')
                    print('=====撤销该挂单=====')
                    co['exchangeType'] = order_status['data']['exchangeType']
                    co['orderId'] = order_status['data']['orderId']
                    co['symbol'] = order_status['data']['symbol']
                    result = requests.post(cancelOrder, json=co, headers=header)
                    print(result.json())
                except BaseException as e:
                    with open(os.getcwd() + '/err_symbol_to_order.json', 'a+') as f:
                        msg = 'File "/test_003_OrderAccuracy.py", line 444'
                        f.write('form Exception {}\n'.format(msg) + str(d) + '\n' + str(order_status) + '\n')
                    print('没有找到该挂单 或 已经成交: -> {}'.format(str(e)))

        # with open(os.getcwd() + '/err_symbol_to_order.json', 'r', encoding='utf-8') as f:
        #     fs = f.read()
        #     if not fs:
        #         print('not error symbol ')
        #     else:
        #         print('error symbol ->>>\n')
        #         print(fs)
        #         assert not fs

    @unittest.skip('pass')
    def test_099(self):
        """调试函数"""
        R.flushall()
        print('redis db8 flushall .....')

    @unittest.skip('pass')
    def test_0999(self):
        """调试函数"""


if __name__ == '__main__':
    unittest.main()
