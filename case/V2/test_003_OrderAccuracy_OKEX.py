# -*- coding: utf-8 -*-
# @Time    : 2019-10-15 10:39
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_003_OrderAccuracy_OKEX.py
# @Software: PyCharm


import traceback

from all_import import *
from config.data.test_data import *
from common.OrderFunc import *


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
    """
    使用:
        cnmd(count_list_max_len(list))

    :param d:
    :return:
    """
    d2 = {}
    for k, v in d.items():
        d2[v[0]] = v[1]
    print(d2)
    # print(sorted(d2.items(), key=lambda x: x[0]))
    # print(sorted(d2.items(), key=lambda x: x[0])[-1][1])
    return sorted(d2.items(), key=lambda x: x[0])[-1][1]


def ad_price(price_list):
    """
    过滤失去精度的下单价格
    :param price_list:
    :return:
    """
    new_d = list(zip(price_list, list(range(len(price_list)))))
    lens = 0
    new_l = []
    for i in new_d:
        x = list(i)
        x[1] = len(str(x[0]))
        # print(x)
        if int(x[1]) >= lens:
            lens = int(x[1])
            new_l.append(x[0])
        else:
            pass
    print('数据长度-> {}'.format(lens))
    n = 0
    for j in range(len(new_l)):
        if len(str(new_l[n])) < lens:  # 第一个元素长度<目标长度
            new_l.pop(n)  # 删除
        else:
            n += 1  # 索引+1
    print('符合精度的价格list -> ', new_l)
    print('提取价格 -> ', new_l[0])
    return new_l[0]


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


def last_add_2(s, sell=False):
    """

    :param s:      浮点数字符串
    :param sell:   卖加 买减
    :return:
    """
    k = '0.'
    if type(s) == type(int(1)):
        s = str(float(s))
    else:
        s = str(as_num(s))

    print('last_add_2 -> 传入金额:', s)

    """处理只有一位小数 或者 整数 例: 0.1"""
    if len(s.split('.')[1]) < 2:
        if sell:
            r = float(s) + 0.5  # 卖 +0.5 买 -0.5
            print('sell -> ', r)
            return str(r)
        else:
            r = float(s)
            if 0.5 > r > 0.2:
                r = round(r - 0.1, len(s) - 2)
                print('buy -> ', r)
                return str(r)

            else:
                print('buy -> ', r)
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
        print('sell -> ', r)
        return str(r)
    else:
        print('buy')
        if int(s[-2:-1]) == 0:  # 值的倒数第二位为 0 往后 推一位
            print(type(float(s)))
            msg = '{} - {}'.format(float(s), as_num(float(ss) / 10))
            print(msg)
            r = kexue_add((float(s)) - (float(ss) / 10), len(s) - 2)
            print('科学计数计算结果', r)
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


class TestOrderAccuracyForOKEX(StartEnd, CommonFunc):
    """okex"""

    """
    test_001: 获取交易所所有Symbol -> 储存至Redis
    test_002: 将Symbol list 中每一个币对象分开储存 -> Redis
    test_003: 检查币obj参数
    test_004: 下单前 -> 通过已有orderBook校验 -> moneyPrecision精度
    test_005: spot 通过下单测试 -> moneyPrecision 与 basePrecision + minOrderSize
    test_006: margin 通过下单测试 -> moneyPrecision 与 basePrecision+minOrderSize
    test_007: test_005的调试类->>>【不包含】try-except
    test_008: 复查是否还有未撤的活跃订单->撤单
    test_009: 查看输出错误
    """
    error_num = 0
    logs_path = os.getcwd().split('case')[0] + '/logs'
    f_list = [
        'okex_err_OrderBook.json',
        'okex_err_OrderBook_MoneyPrecision.json',
        'okex_err_Symbol_OrderMoneyPrecision.json',
        'okex_err_Order.json',
        'okex_func_errors.json'
    ]

    def test_001(self):
        """获取交易所所有Symbol(spot,margin) -> 储存至Redis"""

        self.clear_db_08()

        for i in self.f_list:
            with open(self.logs_path + '/{}'.format(i), 'w', encoding='utf-8') as f:
                f.write('')
            print('clear file -> {}'.format(i))

        get_url_symbol_list('okex:spot')
        get_url_symbol_list('okex:margin')

    def test_002(self):
        """将Symbol list 中每一个币对象分开储存 -> Redis"""
        res_spot = save_symbol_obj('okex:spot')
        res_margin = save_symbol_obj('okex:margin')
        print('okex:spot -> {}'.format(res_spot))
        print(res_spot[0])
        print(res_spot[1])

        print('okex:margin -> {}'.format(res_margin))
        print(res_margin[0])
        print(res_margin[1])

        global list_c
        global sy_ob
        list_c = int(res_spot[0])  # spot 总数
        sy_ob = res_spot[1][:-5]  # spot 前缀:okex:spot_list_

        global list_margin_c
        global sy_obj_margin
        list_margin_c = int(res_margin[0])  # margin 总数
        sy_obj_margin = res_margin[1][:-5]

    def test_003(self):
        """检查币obj参数"""
        print(list_c)
        print(sy_ob)
        print(list_margin_c)
        print(sy_obj_margin)
        # list_c = 10
        # sy_ob = 'okex:spot_list_'

        print('========== check spot ==========')
        for i in range(1, list_c + 1):
            print(i)
            n = "%05d" % i
            print(n, type(n))

            dic_obj = eval('(' + R.get(sy_ob + n) + ')')
            print(dic_obj, type(dic_obj))

            self.check_sy_kv(dic_obj)
        print('========== check spot success ==========')

        print('========== check margin ==========')
        for i in range(1, list_margin_c + 1):
            print(i)
            n = "%05d" % i
            print(n, type(n))

            dic_obj = eval('(' + R.get(sy_obj_margin + n) + ')')
            print(dic_obj, type(dic_obj))

            self.check_sy_kv(dic_obj)

        print('========== check margin success ==========')

    def test_004(self):
        """下单前 -> 通过已有orderBook校验 -> moneyPrecision精度"""
        """
        1.从 Redis Symbol List 中提取逐一对比 用于 与 orderbook 精度 对比校验
            错误 -> 记录Redis -> 记录文件
            查看错误
        """

        print(list_c)
        print(sy_ob)
        print(list_margin_c)
        print(sy_obj_margin)
        # list_c = 421  # 调试
        # sy_ob = 'okex:spot_list_'  # 调试

        for i in range(1, list_c + 1):

            try:
                print(i)
                n = "%05d" % i
                print('编号:', n, type(n))

                dic_obj = eval('(' + R.get(sy_ob + n) + ')')
                print('-----moneyPrecision-----')
                print(dic_obj, type(dic_obj))
                print(dic_obj['moneyPrecision'])
                print('\n')

                print('-----orderbook-----')
                jd_list_init = get_url_order_book('okex:spot', dic_obj['symbol']).json()

                if jd_list_init.get('data', None):
                    jd_list = jd_list_init['data']

                    print('<<<- asks list ->>>\n', jd_list['asks'], '\n')
                    print('<<<- bids list ->>>\n', jd_list['bids'], '\n')
                    new_asks = [as_num(i[0]) for i in jd_list['asks']]
                    new_bids = [as_num(i[0]) for i in jd_list['bids']]
                    print('<<<- asks 价格 list ->>>\n', new_asks, type(new_asks), '\n')
                    print('<<<- bids 价格 list ->>>\n', new_bids, type(new_bids), '\n')
                    asks_and_bids = new_asks + new_bids
                    print('<<<- 合并价格 ->>>\n ', asks_and_bids, type(asks_and_bids))
                    print('\n')

                    # 排序反取 与 切出精度
                    asks_and_bids_c = str(cnmd(count_list_max_len(asks_and_bids)))
                    # asks_and_bids_c = str(ad_price(new_asks))  # 卖价
                    # asks_and_bids_c = str(ad_price(new_bids))  # 买价
                    # asks_and_bids_c = str(ad_price(asks_and_bids))  # 合并买卖价
                    print(asks_and_bids_c)

                    print('-----精度提取-----')
                    moneyPrecision_c = dic_obj['moneyPrecision'].split('.')[1]

                    print('moneyPrecision - > {} -> 精度:{}'.format(dic_obj['moneyPrecision'], moneyPrecision_c))
                    print('买卖平均价格 -> {} -> 精度:{}'.format(asks_and_bids_c, asks_and_bids_c.split('.')[1]))

                    if len(moneyPrecision_c) != len(asks_and_bids_c.split('.')[1]):
                        d = {
                            'Redis_symbol_id': n,
                            'symbol_obj': dic_obj,
                            '该用例检验参数:moneyPrecision': str(dic_obj['moneyPrecision']),
                            'OrderBook精度': asks_and_bids_c,
                        }
                        with open(self.logs_path + '/okex_err_OrderBook_MoneyPrecision.json', 'a+') as f:
                            f.write(str(d) + '\n')

                        R.set('error_dic_obj_{}'.format(i), str(d))
                        print('======Redis -> 记录该币错误精度 -> {} ======'.format(n))
                        self.error_num += 1
                else:
                    msg = '未找到该币种 -> {} 请前往 -> {} 交易所复查 -> this func is test_004\n'.format(dic_obj['symbol'], 'okex')
                    with open(self.logs_path + '/okex_err_OrderBook.json', 'a+') as f:
                        f.write(msg)
                        continue
            except BaseException as e:
                msg = 'test_004 -> ID{} 执行异常 -> {}'.format(n, str(e))
                print(msg)
                with open(self.logs_path + '/okex_func_errors.json', 'a+') as f:
                    f.write(msg)
                    traceback.print_exc(file=open(self.logs_path + '/okex_func_errors.json', 'a+'))
                    f.write('\n')
                continue

            # if error_num != 0:
            #     print('发现错误的错误精度,明细查看 -> Redis db8')
            #     assert error_num == 0
            # else:
            #     print('error symbol number:{}'.format(error_num))

    def test_005(self):
        """spot 通过下单测试 -> moneyPrecision 与 basePrecision+minOrderSize"""
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
            
            
        轮询币种list
            |
        取出币种对象——>取出:moneyPrecision,basePrecision,minOrderSize
            |
        取出该币的orderbook——>筛选出符合精度的下单金额——>生成挂单金额
            |
        检验该币 moneyPrecision 与对应 orderbook 筛选出的金额精度
            |
        生成最小下单量——> basePrecision 与 minOrderSize 相加
            |
        下单挂单
            |
        查看订单状态——> 校验订单 price 与  moneyPrecision 精度
                  ——> 校验订单 qty   与  basePrecision 与 minOrderSize 相加的值
            |
        撤单操作
        """
        print(list_c)
        print(sy_ob)
        # list_c = 1  # 调试
        # sy_ob = 'okex:spot_list_'  # 调试
        # test_sy_ob = 'okex:spot_list_{}'.format("%05d" % 1)

        for i in range(1, list_c + 1):

            try:
                n = "%05d" % i
                # d = eval('(' + R.get(test_sy_ob) + ')')   # 调试单条币对
                d = eval('(' + R.get(sy_ob + n) + ')')  # 币种对象
                sy = d['symbol']
                print('====================test -> {} -> {}===================='.format(n, sy))
                sy_l = d['symbol'].split('_')[0]
                sy_r = d['symbol'].split('_')[1]
                print(d, type(d))
                print('symbol -> {}'.format(sy))
                print('买入币种 -> {}'.format(sy_l))
                print('使用币种 -> {}'.format(sy_r))
                print('最少下单量 -> {}'.format(d['minOrderSize']))
                print('\n')

                # 买减->sell 卖加->buy
                # asks:卖盘  bids:买盘
                p = get_url_order_book('okex:spot', sy).json()
                print('orderbook -> {} \n'.format(p))

                if p.get('data', None):

                    asks_one = p['data']['asks'][0][0]
                    bids_one = p['data']['bids'][0][0]
                    print('卖一:{}'.format(asks_one))
                    print('买一:{}'.format(bids_one))

                    buy_list = [p['data']['asks'][0][0], p['data']['asks'][1][0], p['data']['asks'][2][0]]
                    buy_list2 = [as_num(i) for i in buy_list]
                    print('buy_list -> ', buy_list)
                    print('buy_list_to_float -> ', buy_list2)
                    print('\n')

                    p = last_add_2(bids_one)
                    p1 = last_add_2(ad_price(buy_list2))
                    print('\n')
                    print('*下单金额:', p, type(p))
                    print('*防止精度丢失备用下单金额:', p1, type(p1))
                else:
                    msg = '未找到该币种 -> {} 请前往 -> {} 交易所复查 -> this func is test_005\n'.format(sy['symbol'], 'okex')
                    with open(self.logs_path + '/okex_err_OrderBook.json', 'a+') as f:
                        f.write(msg)
                        print('====================end test -> orror {} -> {}====================\n'.format(n, sy))
                        continue

                if len(p) >= len(p1):
                    this_p = p
                    print('===没有丢失精度===\n')
                else:
                    this_p = p1
                    print('===原下单金额丢失精度->使用备用下单金额执行下单操作===\n')

                print('===数量精度提取===')
                basePrecision = d['basePrecision']
                minOrderSize = d['minOrderSize']

                try:
                    l = str(basePrecision).split('.')[1]
                    print('basePrecision:精度 -> {}'.format(len(str(l))))
                    order_q = kexue_add(float(basePrecision) + float(minOrderSize), len(str(l)))
                    print('basePrecision -> {} {} + minOrderSize -> {} {} -> 下单数量 -> {} {} \n'.format(basePrecision,
                                                                                                      type(
                                                                                                          basePrecision),
                                                                                                      minOrderSize,
                                                                                                      type(
                                                                                                          minOrderSize),
                                                                                                      order_q,
                                                                                                      type(order_q)))
                except BaseException as e:
                    l = 0
                    print(
                        '========================================{}========================================'.format(
                            str(e)))
                    print('basePrecision:精度->{}'.format(l))
                    order_q = kexue_add(float(basePrecision) + float(minOrderSize), l)
                    print(
                        'basePrecision -> {} {} + minOrderSize -> {} {} -> 下单数量 -> {} {} ========int======== \n'.format(
                            basePrecision, type(basePrecision), minOrderSize, type(minOrderSize), order_q,
                            type(order_q)))

                print('*下单数量:', order_q, type(order_q))

                # 下单
                r = generating_orders('okex', 'spot', 'normal', this_p, order_q, 'buy', sy)  # buy
                # r = generating_orders('okex', 'spot', 'normal', this_p, order_q, 'sell', sy)  # sell
                res = r.json()
                print(res)
                print('\n')
                c = res.get('code', None)
                m = res.get('message', None)
                s = res.get('success', None)
                sleep(1)
                try:
                    """
                    捕捉: 下单,获取订单,撤单 异常
                    """
                    exchangeType = res['data']['exchangeType']
                    orderId = res['data']['orderId']
                    symbol = res['data']['symbol']

                    # 获取订单
                    order_status = check_order('okex', exchangeType, orderId, symbol, all_json=True)

                    obj_price = d['moneyPrecision']
                    od_price = order_status['data']['price']
                    obj_minsize = d['minOrderSize']
                    od_minsize = order_status['data']['qty']
                    print(obj_price, type(obj_price))
                    print(od_price, type(od_price))
                    print(obj_minsize, type(obj_minsize))
                    print(od_minsize, type(od_minsize))
                    print('=====校验订单精度=====\n')

                    if len(obj_price.split('.')[1]) != len(od_price.split('.')[1]):
                        error_log(self.logs_path, str(d), str(order_status))

                    # 撤单
                    co['exchangeType'] = order_status['data']['exchangeType']
                    co['orderId'] = order_status['data']['orderId']
                    co['symbol'] = order_status['data']['symbol']
                    result = requests.post(cancelOrder, json=co, headers=header)
                    print(result.json())
                    print('====================end test -> {} -> {}====================\n'.format(n, sy))

                except BaseException as e:
                    if not s and m != '下单成功':
                        with open(self.logs_path + '/okex_err_Order.json', 'a+') as f:
                            ff = '币种对象:\n\t{}\n下单金额:\n\t{}\n下单数量:\n\t{}\n返回json:\n\t{}\n\n'.format(
                                str(d), str(this_p), str(order_q), str(res))
                            f.write('下单失败 -> 精度丢失 或者 金额不足 币对ID:{}\n{}'.format(n, str(ff)))
                            traceback.print_exc(file=open(self.logs_path + '/okex_err_Order.json', 'a+'))
                    else:
                        with open(self.logs_path + '/okex_err_Order.json', 'a+') as f:
                            ff = '币种对象:\n\t{}\n下单金额:\n\t{}\n下单数量:\n\t{}\n\n'.format(str(d), str(this_p), str(order_q))
                            f.write('撤单失败 -> 没有找到该挂单 或 订单已经成交: -> 币对ID:{}\n{}\n{}'.format(n, ff, str(e)))
                            traceback.print_exc(file=open(self.logs_path + '/okex_err_Order.json', 'a+'))
                    continue

            except BaseException as e:
                msg = 'test_005 -> ID{} 执行异常 -> {}'.format(n, str(e))
                print(msg)
                with open(self.logs_path + '/okex_func_errors.json', 'a+') as f:
                    f.write(msg)
                    traceback.print_exc(file=open(self.logs_path + '/okex_func_errors.json', 'a+'))
                continue

    def test_006(self):
        """复查是否还有未撤的活跃订单->撤单"""
        r = get_active_orders().json()  # spot订单
        print(r['data'])
        if len(r['data']) == 0:
            print('未发现漏撤订单')
        else:
            print('发现漏撤订单')
            for i in r['data']:
                co['exchangeType'] = i['exchangeType']
                co['orderId'] = i['orderId']
                co['symbol'] = i['symbol']
                result = requests.post(cancelOrder, json=co, headers=header)
                print(result.json())
            print('已经处理漏撤订单')

    def test_007(self):
        """margin 通过下单测试 -> moneyPrecision 与 basePrecision+minOrderSize"""
        print(list_margin_c)
        print(sy_obj_margin)
        # list_margin_c = 10
        # sy_obj_margin = 'okex:margin_list_'

        for i in range(1, list_margin_c + 1):
            try:
                n = "%05d" % i
                d = eval('(' + R.get(sy_obj_margin + n) + ')')

                sy = d['symbol']
                print('====================test -> {} -> {}===================='.format(n, sy))
                sy_l = d['symbol'].split('_')[0]
                sy_r = d['symbol'].split('_')[1]
                print(d, type(d))
                print('symbol -> {}'.format(sy))
                print('买入币种 -> {}'.format(sy_l))
                print('使用币种 -> {}'.format(sy_r))
                print('最少下单量 -> {}'.format(d['minOrderSize']))
                print('\n')

                # 买减->sell 卖加->buy
                # asks:卖盘  bids:买盘
                p = get_url_order_book('okex:spot', sy).json()
                print('orderbook -> {} \n'.format(p))

                if p.get('data', None):

                    asks_one = p['data']['asks'][0][0]
                    bids_one = p['data']['bids'][0][0]
                    print('卖一:{}'.format(asks_one))
                    print('买一:{}'.format(bids_one))

                    buy_list = [p['data']['asks'][0][0], p['data']['asks'][1][0], p['data']['asks'][2][0]]
                    buy_list2 = [as_num(i) for i in buy_list]
                    print('buy_list -> ', buy_list)
                    print('buy_list_to_float -> ', buy_list2)
                    print('\n')

                    p = last_add_2(bids_one)
                    p1 = last_add_2(ad_price(buy_list2))
                    print('\n')
                    print('*下单金额:', p, type(p))
                    print('*防止精度丢失备用下单金额:', p1, type(p1))
                else:
                    msg = '未找到该币种 -> {} 请前往 -> {} 交易所复查 -> this func is test_006\n'.format(sy['symbol'], 'okex')
                    with open(self.logs_path + '/okex_err_OrderBook.json', 'a+') as f:
                        f.write(msg)
                        print('====================end test -> orror {} -> {}====================\n'.format(n, sy))
                        continue

                if len(p) >= len(p1):
                    this_p = p
                    print('===没有丢失精度===\n')
                else:
                    this_p = p1
                    print('===原下单金额丢失精度->使用备用下单金额执行下单操作===\n')

                print('===数量精度提取===')
                basePrecision = d['basePrecision']
                minOrderSize = d['minOrderSize']

                try:
                    l = str(basePrecision).split('.')[1]
                    print('basePrecision:精度 -> {}'.format(len(str(l))))
                    order_q = kexue_add(float(basePrecision) + float(minOrderSize), len(str(l)))
                    print('basePrecision -> {} {} + minOrderSize -> {} {} -> 下单数量 -> {} {} \n'.format(basePrecision,
                                                                                                      type(
                                                                                                          basePrecision),
                                                                                                      minOrderSize,
                                                                                                      type(
                                                                                                          minOrderSize),
                                                                                                      order_q,
                                                                                                      type(order_q)))
                except BaseException as e:
                    l = 0
                    print(
                        '========================================{}========================================'.format(
                            str(e)))
                    print('basePrecision:精度->{}'.format(l))
                    order_q = kexue_add(float(basePrecision) + float(minOrderSize), l)
                    print(
                        'basePrecision -> {} {} + minOrderSize -> {} {} -> 下单数量 -> {} {} ========int======== \n'.format(
                            basePrecision, type(basePrecision), minOrderSize, type(minOrderSize), order_q,
                            type(order_q)))

                print('*下单数量:', order_q, type(order_q))

                try:
                    # 查看余额
                    print('===查看需要划转的资金===')
                    md = self.money_detailed(accountId).json()
                    spot_money = md['data']['position']['spot']
                    margin_money = md['data']['position']['margin']
                    sy_money = [i for i in spot_money if i['symbol'] == sy_r][0]
                    print('币种:{}\n余额:{}'.format(sy_money.get('symbol'), sy_money.get('total')))

                    nb = 0
                    if int(str(sy_money.get('total')).split('.')[0]) < 1:  # 余额小于 1
                        nb = round(float(sy_money.get('total')), 16)  # 保留 6位小数
                        print('划转金额:{}'.format(nb))
                    else:
                        print(sy_money.get('total'), type(sy_money.get('total')))
                        nb = int(float(sy_money.get('total')))  # 取整
                        print('划转金额:{}'.format(nb))

                    # 划转 spot -> margin
                    print('===划转 spot -> margin===')
                    mt = self.money_transfer(accountId, nb, sy_r, 'spot', sy, 'margin').json()
                    print(mt)
                    sleep(1)

                except BaseException as e:
                    msg = 'test_006 -> ID{} 执行异常(查询余额or划转出现异常) -> {}'.format(n, str(e))
                    print(msg)
                    with open(self.logs_path + '/okex_func_errors.json', 'a+') as f:
                        f.write(msg)
                        traceback.print_exc(file=open(self.logs_path + '/okex_func_errors.json', 'a+'))
                    continue

                # 下单
                r = generating_orders('okex', 'margin', 'normal', this_p, order_q, 'buy', sy)  # buy
                res = r.json()
                print(res)
                print('\n')
                c = res.get('code', None)
                m = res.get('message', None)
                s = res.get('success', None)
                sleep(1)

                try:
                    """
                    捕捉: 下单,获取订单,撤单 异常
                    """
                    exchangeType = res['data']['exchangeType']
                    orderId = res['data']['orderId']
                    symbol = res['data']['symbol']

                    # 获取订单
                    order_status = check_order('okex', exchangeType, orderId, symbol, all_json=True)

                    obj_price = d['moneyPrecision']
                    od_price = order_status['data']['price']
                    obj_minsize = d['minOrderSize']
                    od_minsize = order_status['data']['qty']
                    print(obj_price, type(obj_price))
                    print(od_price, type(od_price))
                    print(obj_minsize, type(obj_minsize))
                    print(od_minsize, type(od_minsize))
                    print('=====校验订单精度=====\n')

                    if len(obj_price.split('.')[1]) != len(od_price.split('.')[1]):
                        error_log(self.logs_path, str(d), str(order_status))

                    # 撤单
                    co['exchangeType'] = order_status['data']['exchangeType']
                    co['orderId'] = order_status['data']['orderId']
                    co['symbol'] = order_status['data']['symbol']
                    result = requests.post(cancelOrder, json=co, headers=header)
                    print(result.json())
                    print('====================end test -> {} -> {}====================\n'.format(n, sy))

                    print('=====划转还原 金额  margin -> spot=====')
                    reset_md = self.money_detailed(accountId).json()
                    reset_spot_money = reset_md['data']['position']['spot']
                    reset_margin_money = reset_md['data']['position']['margin']
                    sy_money = [i for i in reset_margin_money if i['symbol'] == sy_r][0]
                    print('币种:{}\n余额:{}'.format(sy_money.get('symbol'), sy_money.get('total')))
                    print(nb)
                    print(sy_r)
                    print(sy)
                    sleep(1)
                    reset_mt = self.money_transfer(accountId, nb, sy_r, 'margin', sy, 'spot').json()
                    print(reset_mt)
                    sleep(1)

                except BaseException as e:
                    if not s and m != '下单成功':
                        with open(self.logs_path + '/okex_err_Order.json', 'a+') as f:
                            ff = '币种对象:\n\t{}\n下单金额:\n\t{}\n下单数量:\n\t{}\n返回json:\n\t{}\n\n'.format(
                                str(d), str(this_p), str(order_q), str(res))
                            f.write('下单失败 -> 精度丢失 或者 金额不足 或 没有币对 币对ID:{}\n{}'.format(n, str(ff)))
                            traceback.print_exc(file=open(self.logs_path + '/okex_err_Order.json', 'a+'))
                            continue
                    else:
                        with open(self.logs_path + '/okex_err_Order.json', 'a+') as f:
                            ff = '币种对象:\n\t{}\n下单金额:\n\t{}\n下单数量:\n\t{}\n\n'.format(str(d), str(this_p), str(order_q))
                            f.write('撤单失败 -> 没有找到该挂单 或 订单已经成交: -> 币对ID:{}\n{}\n{}'.format(n, ff, str(e)))
                            traceback.print_exc(file=open(self.logs_path + '/okex_err_Order.json', 'a+'))
                            continue
            except BaseException as e:
                msg = 'test_006 -> ID{} 执行异常 -> {}'.format(n, str(e))
                print(msg)
                with open(self.logs_path + '/okex_func_errors.json', 'a+') as f:
                    f.write(msg)
                    traceback.print_exc(file=open(self.logs_path + '/okex_func_errors.json', 'a+'))
                    continue
        self.test_010()

    # @unittest.skip('废除 test_005的调试类->>>【不包含】try-except')
    def test_008(self):
        """test_005的调试类->>>【不包含】try-except"""
        self.money_spot_margin()

    def test_009(self):
        """查看错误输出"""

        er = 0
        for i in self.f_list:
            with open(self.logs_path + '/{}'.format(i), 'r', encoding='utf-8') as f:
                fs = f.read()
                if not fs:
                    print('{} -> not error'.format(i))
                else:
                    print('===error->>> {} ==='.format(i))
                    print(fs, '\n')
                    er += 1
        assert er == 0

    # @unittest.skip('调试函数 -> Pass')
    def test_010(self):
        """调试函数"""
        self.money_spot_margin()

    @unittest.skip('调试函数 -> Pass')
    def test_0999(self):
        """调试函数"""
        # {
        #     "accountId": "4993",
        #     "amount": 5,
        #     "coin": "usdt",
        #     "from": "spot",
        #     "symbol": "trx_usdt",
        #     "to": "margin"
        # }
        # r = self.money_transfer(accountId, 5, 'usdt', 'spot', 'trx_usdt', 'margin').json()
        # r = self.money_transfer(accountId, 0.00001704, 'usdt', 'margin', 'eos_usdt', 'spot').json()
        # print(r)

        reset_mt = self.money_transfer(accountId, 6, 'usdt', 'margin', 'neo_usdt', 'spot').json()
        print(reset_mt)
        # self.test_001()
        # self.test_002()
        # self.test_003()
        # self.test_004()
        # self.test_006()


if __name__ == '__main__':
    unittest.main()
