# -*- coding: utf-8 -*-
# @Time    : 2019-10-15 10:39
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_003_OrderAccuracy_001_OKEX.py
# @Software: PyCharm


import traceback

from all_import import *
from config.data.test_data import *
from common.OrderFunc import *

if R.get('RUN_ENV') == 'pro':
    run_env = 'pro'
    a_id = accountId_to_dict.get('pro')['okex']
    R = redis_obj(5)
    R2 = redis_obj(1)
else:
    run_env = 'dev'
    a_id = accountId_to_dict.get('dev')['okex']
    R = redis_obj(6)
    R2 = redis_obj(0)

ob_ex_exType = 'okex:spot'
exchange = 'okex'


class TestOrderAccuracyForOKEX(StartEnd, CommonFunc):
    """okex"""

    """
    test_001: 获取交易所所有Symbol -> 储存至Redis
    test_002: 将Symbol list 中每一个币对象分开储存 -> Redis
    test_003: 检查币obj参数
    test_004: 下单前 -> 通过已有orderBook校验 spot-> moneyPrecision精度
    test_005: 下单前 -> 通过已有orderBook校验 margin-> moneyPrecision精度
    test_006: spot 通过下单测试 -> moneyPrecision 与 basePrecision + minOrderSize
    test_007: 复查是否还有未撤的活跃订单->撤单
    test_008: margin 通过下单测试 -> moneyPrecision 与 basePrecision+minOrderSize
    test_009: 查看 spot 与 margin 资金
    test_010: 整合并格式化输出日志 
    test_011: 查看输出错误
    test_012: 调试test_006，test_007
    
    """
    error_num = 0
    logs_path = os.getcwd().split('case')[0] + '/logs'
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    f_name = '/okex_log_{}_{}.txt'.format(run_env, now)

    print(run_env)

    def test_001(self):
        """获取交易所所有Symbol(spot,margin) -> 储存至Redis"""

        self.clear_db_08(R)
        get_url_symbol_list('{}:spot'.format(exchange), R)
        get_url_symbol_list('{}:margin'.format(exchange), R)

    def test_002(self):
        """将Symbol list 中每一个币对象分开储存 -> Redis"""

        res_spot = save_symbol_obj('{}:spot'.format(exchange), R)
        res_margin = save_symbol_obj('{}:margin'.format(exchange), R)

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
        """检查币对参数"""
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

            self.check_sy_kv(n, dic_obj, R)
        print('========== check spot success ==========')

        print('========== check margin ==========')
        for i in range(1, list_margin_c + 1):
            print(i)
            n = "%05d" % i
            print(n, type(n))

            dic_obj = eval('(' + R.get(sy_obj_margin + n) + ')')
            print(dic_obj, type(dic_obj))

            self.check_sy_kv(n, dic_obj, R)

        print('========== check margin success ==========')

    def test_004(self):
        """下单前 -> 通过已有orderBook校验 spot-> moneyPrecision精度"""
        """
        1.从 Redis Symbol List 中提取逐一对比 用于 与 orderbook 精度 对比校验
            错误 -> 记录Redis -> 记录文件
            查看错误
        """

        print(list_c)
        print(sy_ob)
        # list_c = 421  # 调试
        # sy_ob = 'okex:spot_list_'  # 调试
        self.check_odb(list_c, sy_ob, 'okex:spot', R, 'test_004')

    def test_005(self):
        """下单前 -> 通过已有orderBook校验 margin-> moneyPrecision精度"""
        print(list_margin_c)
        print(sy_obj_margin)
        # list_margin_c = 24  # 调试
        # sy_obj_margin = 'okex:margin_list_'  # 调试
        self.check_odb(list_margin_c, sy_obj_margin, 'okex:margin', R, 'test_005')

    def test_006(self):
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
        r_first_key = 'test_006'
        print(list_c)
        print(sy_ob)
        # list_c = 10  # 调试
        # sy_ob = 'okex:spot_list_'  # 调试
        # test_sy_ob = 'okex:spot_list_{}'.format("%05d" % 171)

        for i in range(1, list_c + 1):

            try:
                n = "%05d" % i
                # d = eval('(' + R.get(test_sy_ob) + ')')  # 调试单条币对
                d = eval('(' + R.get(sy_ob + n) + ')')  # 币种对象
                sy = d['symbol']
                print('====================test -> {} -> {}===================='.format(n, sy))
                sy_l = d['symbol'].split('_')[0]
                sy_r = d['symbol'].split('_')[1]
                print(d, type(d))
                print('symbol -> {}'.format(sy), type(sy))
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

                    p = first_add(bids_one)
                    p1 = first_add(ad_price(buy_list2))
                    print('\n')
                    print('*下单金额:', p, type(p))
                    print('*防止精度丢失备用下单金额:', p1, type(p1))
                else:
                    new_obj = {
                        'redis_id': n,
                        'redis_err': 'OrderBook未找到该币对:{}'.format(sy),
                        'result': p
                    }
                    d.update(new_obj)
                    R.set('{}->OrderBook未找到该币种->ID:{}'.format(r_first_key, n), str(d))
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
                    # 下单
                    r = generating_orders(a_id, exchange, 'spot', 'normal', this_p, order_q, 'buy', sy)  # buy
                    # r = generating_orders(a_id, exchange, 'spot', 'normal', this_p, order_q, 'sell', sy)  # sell
                    res = r.json()
                    print(res)
                    sleep(1)

                    res_code = res.get('code', None)
                    res_message = res.get('message', None)

                    if res_code == 2000 and '响应失败,交易所返回信息' in res_message and 'Order total cannot be lower than' in res_message:
                        x = eval('(' + res.get('rawStr', None).replace('null', "''") + ')')
                        xx = (x['err-msg'].split('than:')[1][2:-1])
                        new_obj = {
                            'redis_id': n,
                            'redis_err': '数量精度误差:币对数量精度:{},交易所精度:{}'.format(order_q, xx),
                            'result': res
                        }

                        d.update(new_obj)
                        R.set('{}->下单失败->ID:{}'.format(r_first_key, n), str(d))
                        print('下单失败->{}'.format(n))
                        continue

                    exchangeType = res['data'].get('exchangeType', None)
                    orderId = res['data'].get('orderId', None)
                    symbol = res['data'].get('symbol', None)

                    if res_code != 1000 and res_message != '下单成功' and not orderId:
                        print(res)

                        new_obj = {
                            'redis_id': n,
                            'redis_err': '下单失败:价格{},数量{}'.format(this_p, order_q),
                            'result': res
                        }
                        d.update(new_obj)
                        R.set('{}->下单失败->ID:{}'.format(r_first_key, n), str(d))
                        print('下单失败->{}'.format(n))
                        continue

                    # 获取订单
                    order_status = check_order(a_id, exchange, exchangeType, orderId, symbol, all_json=True)
                    if order_status.get('message', None) != '获取订单成功：':
                        print(order_status)

                        new_obj = {
                            'redis_id': n,
                            'redis_err': '获取订单失败:状态 {},单号 {}'.format(order_status['data'].get('status', None),
                                                                     order_status['data'].get('orderId', None)),
                            'result': order_status
                        }
                        d.update(new_obj)
                        R.set('{}->获取订单失败->ID:{}'.format(r_first_key, n), str(d))
                        print('获取订单失败->{}'.format(n))
                        continue

                    # 订单状态
                    od_status = order_status['data'].get('status', None)
                    obj_price = d['moneyPrecision']
                    od_price = order_status['data']['price']
                    obj_minsize = d['minOrderSize']
                    od_minsize = order_status['data']['qty']
                    print(obj_price, type(obj_price))
                    print(od_price, type(od_price))
                    print(obj_minsize, type(obj_minsize))
                    print(od_minsize, type(od_minsize))
                    print('=====校验订单精度=====\n')

                    if len(obj_price.split('.')[1]) != len(as_num(od_price).split('.')[1]):
                        new_obj = {
                            'redis_id': n,
                            'redis_err': '下单后币种精度与OrderBook不相符,价格精度{},数量精度{}'.format(od_price, od_minsize, ),
                            'result': order_status
                        }
                        d.update(new_obj)
                        R.set('{}->下单后币种精度与OrderBook不相符->ID{}'.format(r_first_key, n), str(d))

                    print('od_status ->', od_status)

                    # 撤单
                    if od_status != 'active':
                        print('订单状态:{}'.format(od_status))
                        print('撤单失败->{}'.format(n))

                        new_obj = {
                            'redis_id': n,
                            'redis_err': '撤单失败,状态{},单号{}'.format(od_status, order_status['data'].get('orderId', None)),
                            'result': order_status
                        }
                        d.update(new_obj)
                        R.set('{}->撤单失败->{}'.format(r_first_key, n), str(d))
                        continue
                    else:
                        exchangeType = order_status['data'].get('exchangeType')
                        orderId = order_status['data'].get('orderId')
                        symbol = order_status['data'].get('symbol')
                        cancel_order(a_id, exchange, exchangeType, orderId, symbol)
                        print('====================end test -> {} -> {}====================\n'.format(n, sy))

                except BaseException as e:
                    new_obj = {
                        'redis_id': n,
                        'redis_err': '内层func执行异常:{}'.format(str(e)),
                        'result': '忽略'
                    }
                    d.update(new_obj)
                    R.set('{}->内层func执行异常->ID{}'.format(r_first_key, n), str(d))
                    continue

            except BaseException as e:
                new_obj = {
                    'redis_id': n,
                    'redis_err': '外层func执行异常:{}'.format(str(e)),
                    'result': '忽略'
                }
                d.update(new_obj)
                R.set('{}->外层func执行异常->ID{}'.format(r_first_key, n), str(d))
                continue

    def test_007(self):
        """复查是否还有未撤的活跃订单->撤单"""
        r = get_active_orders(a_id, exchange, 'spot').json()  # spot订单
        print(r['data'])
        if len(r['data']) == 0:
            print('未发现漏撤订单')
        else:
            print('发现漏撤订单')
            for i in r['data']:
                cancel_order(a_id, exchange, i['exchangeType'], i['orderId'], i['symbol'])
            print('已经处理漏撤订单')

    @unittest.skip('margin需要调试/划转接口修改未更新到生产环境/划转接口请求限制')
    def test_008(self):
        """margin 通过下单测试 -> moneyPrecision 与 basePrecision+minOrderSize"""
        r_first_key = 'test_008'
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
                p = get_url_order_book('okex:margin', sy).json()
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

                    p = first_add(bids_one)
                    p1 = first_add(ad_price(buy_list2))
                    print('\n')
                    print('*下单金额:', p, type(p))
                    print('*防止精度丢失备用下单金额:', p1, type(p1))
                else:
                    new_obj = {
                        'redis_id': n,
                        'redis_err': '交易所或OrderBook未找到该币种',
                        'result': p
                    }
                    d.update(new_obj)
                    R.set('{}->交易所或OrderBook未找到该币种->{}'.format(r_first_key, n), str(d))
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

                # 划转-下单-反划转
                print('=' * 66 + '划转 -> 下单 -> 撤单 -> 反划转' + '=' * 66)
                # 查看余额
                print('===查看需要划转的资金===')
                md = self.money_detailed(a_id).json()
                # print('md', md)

                if md.get('code', None) == 1000 and md.get('message', None) == '获取成功':
                    spot_money = md['data']['position']['spot']
                    margin_money = md['data']['position']['margin']
                    sy_money = [i for i in spot_money if i['symbol'] == sy_r][0]
                    print('币种:{}\n余额:{}'.format(sy_money.get('symbol'), sy_money.get('total')))

                else:
                    new_obj = {
                        'redis_id': n,
                        'redis_err': '获取资金明细失败',
                        'result': md
                    }
                    d.update(new_obj)
                    R.set('{}->获取资金明细失败->ID{}'.format(r_first_key, n), str(d))
                    continue

                # 小数大于8位取8位
                # 小数小于8位直接取
                # 整数直接取
                if '.' in sy_money.get('total'):
                    if len(sy_money.get('total').split('.')[1]) >= 8:
                        print(sy_money.get('total').split('.')[1][:8])
                        nb = sy_money.get('total').split('.')[0] + '.' + sy_money.get('total').split('.')[1][:8]
                        print(nb)
                    else:
                        nb = sy_money.get('total')
                else:
                    nb = sy_money.get('total')

                print('{}划转金额:{}'.format(n, nb))

                # 划转 spot -> margin
                print('===划转 spot -> margin===')

                mt = self.money_transfer(a_id, nb, sy_r, 'spot', sy, 'margin', sy, update=True).json()
                print(mt)

                if mt.get('code', None) == 1000 and mt.get('message', None) == '操作成功' and mt.get('success', None):
                    print(mt)
                    sleep(1)
                else:
                    new_obj = {
                        'redis_id': n,
                        'redis_err': '划转失败',
                        'result': mt
                    }
                    d.update(new_obj)
                    R.set('{}->划转失败->ID{}'.format(r_first_key, n), str(d))
                    sleep(1)
                    continue

                try:

                    # 下单
                    r = generating_orders(a_id, exchange, 'margin', 'normal', this_p, order_q, 'buy', sy)  # buy
                    res = r.json()
                    print(res)
                    sleep(1)

                    res_code = res.get('code', None)
                    res_message = res.get('message', None)

                    # 下单失败
                    if res_code != 1000 and res_message != '下单成功':
                        print(res)

                        new_obj = {
                            'redis_id': n,
                            'redis_err': '下单失败',
                            'result': res
                        }
                        d.update(new_obj)
                        R.set('{}->下单失败->ID{}'.format(r_first_key, n), str(d))
                        print('下单失败->{}'.format(n))

                        # 下单失败反划转
                        print('=====下单失败 -> 划转还原 金额  margin -> spot=====')
                        reset_md = self.money_detailed(a_id).json()
                        reset_spot_money = reset_md['data']['position']['spot']
                        reset_margin_money = reset_md['data']['position']['margin']
                        print(reset_margin_money)
                        sy_money = [i for i in reset_margin_money if i['symbol'] == sy_r][0]
                        print('币种:{}\n余额:{}'.format(sy_money.get('symbol'), sy_money.get('total')))
                        print(nb)
                        print(sy_r)
                        print(sy)
                        sleep(1)

                        reset_mt = self.money_transfer(a_id, nb, sy_r, 'margin', sy, 'spot', sy, update=True).json()
                        print(reset_mt)

                        # 反划转失败
                        if reset_mt.get('message', None) != '操作成功' and reset_mt.get('code', None) != 1000:
                            new_obj = {
                                'redis_id': n,
                                'redis_err': '下单失败_反划转失败',
                                'result': reset_mt
                            }
                            d.update(new_obj)
                            R.set('{}->下单失败_反划转失败->ID{}'.format(r_first_key, n), str(d))
                            continue
                        else:
                            new_obj = {
                                'redis_id': n,
                                'redis_err': '下单失败_反划转成功',
                                'result': reset_mt
                            }
                            d.update(new_obj)
                            R.set('{}->下单失败_反划转成功->ID{}'.format(r_first_key, n), str(d))
                            continue

                    exchangeType = res['data'].get('exchangeType', None)
                    orderId = res['data'].get('orderId', None)
                    symbol = res['data'].get('symbol', None)

                    # 获取订单
                    order_status = check_order(a_id, exchange, exchangeType, orderId, symbol, all_json=True)
                    if order_status.get('message', None) != '获取订单成功：':
                        print(order_status)
                        new_obj = {
                            'redis_id': n,
                            'redis_err': '获取订单失败',
                            'result': order_status
                        }
                        d.update(new_obj)
                        R.set('{}->获取订单失败->ID{}'.format(r_first_key, n), str(d))
                        print('获取订单失败->{}'.format(n))
                        continue

                    # 订单状态
                    od_status = order_status['data'].get('status', None)

                    obj_price = d['moneyPrecision']
                    od_price = order_status['data']['price']
                    obj_minsize = d['minOrderSize']
                    od_minsize = order_status['data']['qty']
                    print(obj_price, type(obj_price))
                    print(od_price, type(od_price))
                    print(obj_minsize, type(obj_minsize))
                    print(od_minsize, type(od_minsize))
                    print('=====校验订单精度=====\n')

                    if len(obj_price.split('.')[1]) != len(as_num(od_price).split('.')[1]):
                        new_obj = {
                            'redis_id': n,
                            'redis_err': '下单后币种精度与OrderBook不相符,币对【价格精度:{}与数量精度:{}】订单【价格精度:{}与数量精度:{}】'.format(obj_price,
                                                                                                              obj_minsize,
                                                                                                              od_price,
                                                                                                              od_minsize),
                            'result': order_status
                        }
                        d.update(new_obj)
                        R.set('{}->下单后币种精度与OrderBook不相符->ID{}'.format(r_first_key, n), str(d))

                    # 撤单
                    if od_status != 'active':
                        print('订单状态:{}'.format(od_status))
                        print('撤单失败->{}'.format(n))
                        new_obj = {
                            'redis_id': n,
                            'redis_err': '撤单失败,状态{},单号{}'.format(od_status, order_status['data'].get('orderId', None)),
                            'result': order_status
                        }
                        d.update(new_obj)
                        R.set('{}->撤单失败->ID{}'.format(r_first_key, n), str(d))
                        continue
                    else:
                        exchangeType = order_status['data'].get('exchangeType')
                        orderId = order_status['data'].get('orderId')
                        symbol = order_status['data'].get('symbol')
                        cancel_order(a_id, exchange, exchangeType, orderId, symbol)
                        print('====================end test -> {} -> {}====================\n'.format(n, sy))

                    # 反划转
                    print('=====划转还原 金额  margin -> spot=====')
                    reset_md = self.money_detailed(a_id).json()
                    reset_spot_money = reset_md['data']['position']['spot']
                    reset_margin_money = reset_md['data']['position']['margin']
                    sy_money = [i for i in reset_margin_money if i['symbol'] == sy_r][0]
                    print('币种:{}\n余额:{}'.format(sy_money.get('symbol'), sy_money.get('total')))
                    print(nb)
                    print(sy_r)
                    print(sy)
                    sleep(1)

                    reset_mt = self.money_transfer(a_id, nb, sy_r, 'margin', sy, 'spot', sy, update=True).json()
                    print(reset_mt)

                    if reset_mt.get('message', None) != '操作成功' and reset_mt.get('code', None) != 1000:
                        new_obj = {
                            'redis_id': n,
                            'redis_err': '反划转失败',
                            'result': reset_mt
                        }
                        d.update(new_obj)
                        R.set('{}->反划转失败->ID{}'.format(r_first_key, n), str(d))
                        continue
                    else:
                        sleep(1)
                except BaseException as e:
                    new_obj = {
                        'redis_id': n,
                        'redis_err': '内func执行异常:{}'.format(str(e)),
                        'result': '{}'.format(str(traceback.print_exc()))
                    }
                    d.update(new_obj)
                    R.set('{}->内func执行异常->ID{}'.format(r_first_key, n), str(d))
                    continue

            except BaseException as e:
                new_obj = {
                    'redis_id': n,
                    'redis_err': '外func执行异常:{}'.format(str(e)),
                    'result': '{}'.format(str(traceback.print_exc()))
                }
                d.update(new_obj)
                R.set('{}->外func执行异常->ID{}'.format(r_first_key, n), str(d))
                continue

    def test_009(self):
        """查看 spot 与 margin 资金"""
        self.money_spot_margin(a_id)

    def test_010(self):
        """整合并格式化输出日志"""
        '''
        exchange_key = 'exchange:%s' % exchange
        if R.keys(pattern='test_*'):
            for i in R.keys(pattern='test_*'):
                logs_obj = eval('(' + R.get(i) + ')')
                print(logs_obj)
                l = logs_obj['send'].split('->')[0]
                r = logs_obj['send'].split('->')[1]
                R2.hmset(exchange_key, {l: r})

            # print(R2.hgetall(exchange_key))
            # print(type(R2.hgetall(exchange_key)))

            tb.field_names = ['Symbol', 'error']
            for k, v in R2.hgetall(exchange_key).items():
                print(k, '->', v)
                tb.add_row([k, v])
            with open(self.logs_path + self.f_name, 'w', encoding='utf-8') as f:
                f.write(str(tb))
            print(tb)
        else:
            tb.add_row(['null', 'null'])
            print('===未发现错误===')
            with open(self.logs_path + self.f_name, 'w', encoding='utf-8') as f:
                f.write('')
            print(tb)
        '''
        exchange_key = 'exchange:%s' % exchange
        tb.field_names = ['Symbol', 'error', 'result']
        num = 1
        if R.keys(pattern='test_*'):
            for i in R.keys(pattern='test_*'):
                logs_obj = eval('(' + R.get(i) + ')')
                R2.hmset(exchange_key, {num: R.get(i)})
                num += 1
                # print(logs_obj.get('symbol'))
                # print(logs_obj.get('redis_err'))
                # print(logs_obj.get('result'))
                tb.add_row([logs_obj.get('symbol'), logs_obj.get('redis_err'), str(logs_obj.get('result'))])
            with open(self.logs_path + self.f_name, 'w', encoding='utf-8') as f:
                f.write(str(tb))
            print(tb)

        else:
            tb.add_row(['null', 'null', 'null'])
            print('===未发现错误===')
            with open(self.logs_path + self.f_name, 'w', encoding='utf-8') as f:
                f.write('')
            print(tb)

    def test_011(self):
        """ okex -> 查看错误输出"""

        er = 0

        with open(self.logs_path + self.f_name, 'r', encoding='utf-8') as f:
            fs = f.read()
            if not fs:
                print('not error')
            else:
                # print(fs)
                print('错误日志记录')
                print('AirCurrency/logs/{}'.format(self.f_name))
                er += 1
        assert er == 0

    @unittest.skip('调试test_005 -> Pass')
    def test_012(self):
        """调试test_005"""

        list_c = 1  # 调试
        # sy_ob = 'okex:spot_list_'  # 调试
        test_sy_ob = 'okex:spot_list_{}'.format("%05d" % 364)

        for i in range(1, list_c + 1):

            n = "%05d" % i
            d = eval('(' + R.get(test_sy_ob) + ')')  # 调试单条币对
            # d = eval('(' + R.get(sy_ob + n) + ')')  # 币种对象
            sy = d['symbol']
            print('====================test -> {} -> {}===================='.format(n, sy))
            sy_l = d['symbol'].split('_')[0]
            sy_r = d['symbol'].split('_')[1]
            print(d, type(d))
            print('symbol -> {}'.format(sy), type(sy))
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

                p = first_add(bids_one)
                p1 = first_add(ad_price(buy_list2))
                print('\n')
                print('*下单金额:', p, type(p))
                print('*防止精度丢失备用下单金额:', p1, type(p1))
            else:
                sss = '{} -> 交易所或OrderBook未找到该币对'.format(sy)
                self.format_logs['msg'] = str(d)
                self.format_logs['send'] = sss
                R.set('test_005->交易所或OrderBook未找到该币种->ID:{}'.format(i), str(self.format_logs))
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

            # try:

            error_obj = {
                '币对测试ID': str(n),
                '币种对象': str(d),
                '下单金额': str(this_p),
                '下单数量': str(order_q),
                'json_res': ''
            }

            # 下单
            r = generating_orders(a_id, exchange, 'spot', 'normal', this_p, order_q, 'buy', sy)  # buy
            # r = generating_orders(a_id, exchange, 'spot', 'normal', this_p, order_q, 'sell', sy)  # sell
            res = r.json()
            print(res)
            sleep(1)

            res_code = res.get('code', None)
            res_message = res.get('message', None)
            exchangeType = res['data'].get('exchangeType', None)
            orderId = res['data'].get('orderId', None)
            symbol = res['data'].get('symbol', None)

            if res_code != 1000 and res_message != '下单成功' and not orderId:
                print(res)
                error_obj['json_res'] = str(res)
                sss = '{} -> 下单失败:价格{},数量{}'.format(sy, this_p, order_q)
                self.format_logs['msg'] = error_obj
                self.format_logs['send'] = sss
                R.set('test_005->下单失败->ID:{}'.format(n), str(self.format_logs))
                print('下单失败->{}'.format(n))
                continue

            # 获取订单
            order_status = check_order(a_id, exchange, exchangeType, orderId, symbol, all_json=True)
            if order_status.get('message', None) != '获取订单成功：':
                print(order_status)
                error_obj['json_res'] = str(order_status)
                sss = '{} -> 获取订单失败:状态 {},单号 {}'.format(sy, order_status['data'].get('status', None),
                                                        order_status['data'].get('orderId', None))
                self.format_logs['msg'] = error_obj
                self.format_logs['send'] = sss
                R.set('test_005->获取订单失败->ID:{}'.format(n), str(self.format_logs))
                print('获取订单失败->{}'.format(n))
                continue

            # 订单状态
            od_status = order_status['data'].get('status', None)

            obj_price = d['moneyPrecision']
            od_price = order_status['data']['price']
            obj_minsize = d['minOrderSize']
            od_minsize = order_status['data']['qty']
            print(obj_price, type(obj_price))
            print(od_price, type(od_price))
            print(obj_minsize, type(obj_minsize))
            print(od_minsize, type(od_minsize))
            print('=====校验订单精度=====\n')
            print(obj_price.split('.')[1])
            print(od_price)

            if len(obj_price.split('.')[1]) != len(as_num(od_price).split('.')[1]):
                ff = '币种对象:\n{}\n\n订单对象:\n{}'.format(str(d), str(order_status))
                sss = '{} -> 下单后币种精度与OrderBook不相符,价格精度{},数量精度{}'.format(sy, od_price, od_minsize)
                self.format_logs['msg'] = ff
                self.format_logs['send'] = sss
                R.set('test_005->下单后币种精度与OrderBook不相符->ID{}'.format(n), str(self.format_logs))

            print('od_status', od_status)

            # 撤单
            if od_status != 'active':
                print('订单状态:{}'.format(od_status))
                print('撤单失败->{}'.format(n))
                error_obj['json_res'] = str({'订单状态': '{}'.format(od_status)})
                error_obj['订单明细'] = str(order_status)
                sss = '{} -> 撤单失败,状态{},单号{}'.format(sy, od_status, order_status['data'].get('orderId', None))
                self.format_logs['msg'] = error_obj
                self.format_logs['send'] = sss
                R.set('test_005->撤单失败->{}'.format(n), str(self.format_logs))
                continue
            else:
                exchangeType = order_status['data'].get('exchangeType')
                orderId = order_status['data'].get('orderId')
                symbol = order_status['data'].get('symbol')
                cancel_order(a_id, exchange, exchangeType, orderId, symbol)
                print('====================end test -> {} -> {}====================\n'.format(n, sy))

    @unittest.skip('调试函数 -> Pass')
    def test_099(self):
        """调试函数"""
        self.money_spot_margin(a_id)

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
        r = self.money_transfer(a_id, 0.1, 'usdt', 'spot', 'trx_usdt', 'margin').json()
        # r = self.money_transfer(a_id, 0.00001704, 'usdt', 'margin', 'eos_usdt', 'spot').json()
        print(r)

        # reset_mt = self.money_transfer(a_id, 6, 'usdt', 'margin', 'neo_usdt', 'spot').json()
        # print(reset_mt)

    @unittest.skip('分组调试 -> Pass')
    def test_09999(self):
        self.test_001()
        self.test_002()
        # self.test_003()
        # self.test_004()
        # self.test_005()
        # self.test_006()
        # self.test_007()
        self.test_008()
        # self.test_009()
        # self.test_010()

    @unittest.skip('分组调试 -> Pass')
    def test_099999(self):
        """分组调试"""


if __name__ == '__main__':
    unittest.main()
