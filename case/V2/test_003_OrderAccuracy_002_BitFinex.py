# -*- coding: utf-8 -*-
# @Time    : 2019-10-30 17:55
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_003_OrderAccuracy_002_BitFinex.py
# @Software: PyCharm


from all_import import *
from config.data.test_data import *
from common.OrderFunc import *
from case.V2.test_003_OrderAccuracy_001_OKEX import as_num, cnmd, count_list_max_len, first_add, kexue_add, ad_price

a_id = accountId_to_dict.get('bitfinex')
ob_ex_exType = 'bitfinex:spot'
exchange = 'bitfinex'

if R.get('RUN_ENV') == 'pro':
    R = redis_obj(7)
    R2 = redis_obj(1)
else:
    R = redis_obj(8)
    R2 = redis_obj(0)


class TestOrderAccuracyForBITFINEX(StartEnd, CommonFunc):
    """BitFinex"""

    error_num = 0
    logs_path = os.getcwd().split('case')[0] + '/logs'
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    f_name = '/BitFinex_log_{}.txt'.format(now)
    format_logs = {
        'msg': '',
        'send': ''
    }

    def test_001(self):
        """获取交易所所有Symbol(spot,future) -> 储存至Redis"""
        self.clear_db_08(R)
        get_url_symbol_list('bitfinex:spot', R)
        get_url_symbol_list('bitfinex:future', R)

    def test_002(self):
        """将Symbol list 中每一个币对象分开储存 -> Redis"""
        res_spot = save_symbol_obj('bitfinex:spot', R)
        res_future = save_symbol_obj('bitfinex:future', R)

        print('bitfinex:spot -> {}'.format(res_spot))
        print(res_spot[0])
        print(res_spot[1])

        print('bitfinex:future -> {}'.format(res_future))
        print(res_future[0])
        print(res_future[1])

        global list_c
        global sy_ob
        list_c = int(res_spot[0])  # spot 总数
        sy_ob = res_spot[1][:-5]  # spot 前缀:bitfinex:future_list_

        global list_future_c
        global sy_obj_future
        list_future_c = int(res_future[0])  # future 总数
        sy_obj_future = res_future[1][:-5]

    def test_003(self):
        """检查币对参数"""
        print(list_c)
        print(sy_ob)
        print(list_future_c)
        print(sy_obj_future)

        print('========== check spot ==========')
        for i in range(1, list_c + 1):
            print(i)
            n = "%05d" % i
            print(n, type(n))

            dic_obj = eval('(' + R.get(sy_ob + n) + ')')
            print(dic_obj, type(dic_obj))

            self.check_sy_kv(dic_obj, R)
        print('========== check spot success ==========')

        print('========== check future ==========')
        for i in range(1, list_future_c + 1):
            print(i)
            n = "%05d" % i
            print(n, type(n))

            dic_obj = eval('(' + R.get(sy_obj_future + n) + ')')
            print(dic_obj, type(dic_obj))

            self.check_sy_kv(dic_obj, R)

        print('========== check future success ==========')

    def test_004(self):
        """下单前 -> 通过已有orderBook校验 -> moneyPrecision精度"""

        print(list_c)
        print(sy_ob)
        print(list_future_c)
        print(sy_obj_future)

        # list_c = 416  # 调试
        # sy_ob = 'bitfinex:spot_list_'  # 调试

        for i in range(1, list_c + 1):

            try:
                print(i)
                n = "%05d" % i
                print('编号:', n, type(n))

                dic_obj = eval('(' + R.get(sy_ob + n) + ')')
                print('-----moneyPrecision-----')
                print(dic_obj, type(dic_obj))
                print('moneyPrecision -> {}'.format(dic_obj['moneyPrecision']))
                print('\n')

                print('-----orderbook-----')
                jd_list_init = get_url_order_book('bitfinex:spot', dic_obj['symbol']).json()

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

                        sss = '{} -> 该用例检验参数:moneyPrecision:{}与OrderBook精度:{}不一致'.format(dic_obj['symbol'],
                                                                                         str(dic_obj['moneyPrecision']),
                                                                                         asks_and_bids_c)
                        self.format_logs['msg'] = str(d)
                        self.format_logs['send'] = sss
                        R.set('test_004->币种精度与OrderBook不相符->{}'.format(n), str(self.format_logs))
                else:
                    sss = '{} -> OrderBook未找到该币对'.format(dic_obj['symbol'])
                    self.format_logs['msg'] = ''
                    self.format_logs['send'] = sss
                    R.set('test_004->OrderBook未找到该币种->ID{}'.format(n), str(self.format_logs))
                    continue
            except BaseException as e:
                sss = 'test_004->外层func执行异常:{}'.format(str(e))
                self.format_logs['msg'] = str(dic_obj)
                self.format_logs['send'] = sss
                R.set('test_004->外层func执行异常->ID{}'.format(n), str(self.format_logs))
                continue

    @unittest.skip('请求被限制 -> test_005 Pass')
    def test_005(self):
        """spot 通过下单测试 -> moneyPrecision 与 basePrecision+minOrderSize"""
        print(list_c)
        print(sy_ob)
        # list_c = 3  # 调试
        # sy_ob = 'bitfinex:spot_list_'  # 调试
        # test_sy_ob = 'bitfinex:spot_list_{}'.format("%05d" % 171)

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
                p = get_url_order_book('bitfinex:spot', sy).json()
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
                    sss = '{} -> OrderBook未找到该币对'.format(sy)
                    self.format_logs['msg'] = str(d)
                    self.format_logs['send'] = sss
                    R.set('test_005->OrderBook未找到该币种->ID:{}'.format(n), str(self.format_logs))
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

                    error_obj = {
                        '币对测试ID': str(n),
                        '币种对象': str(d),
                        '下单金额': str(this_p),
                        '下单数量': str(order_q),
                        'json_res': ''
                    }

                    # 下单
                    r = generating_orders(a_id, exchange, 'spot', 'normal', this_p, order_q, 'buy', sy)  # buy
                    # r = generating_orders(a_id, exchange', 'spot', 'normal', this_p, order_q, 'sell', sy)  # sell
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

                except BaseException as e:
                    error_obj = {
                        '币对测试ID': str(n),
                        '币种对象': str(d),
                        '下单金额': str(this_p),
                        '下单数量': str(order_q),
                        '异常': str(e)
                    }
                    sss = '{} -> 内层func执行异常'.format(sy)
                    self.format_logs['msg'] = error_obj
                    self.format_logs['send'] = sss
                    R.set('test_005->内层func执行异常->ID{}'.format(n), str(self.format_logs))
                    continue

            except BaseException as e:
                error_obj = {
                    '币对测试ID': str(n),
                    '币种对象': str(d),
                    '下单金额': str(this_p),
                    '下单数量': str(order_q),
                    '异常': str(e)
                }
                sss = '{} -> 外层func执行异常'.format(sy)
                self.format_logs['msg'] = error_obj
                self.format_logs['send'] = sss
                R.set('test_005->外层func执行异常->ID{}'.format(n), str(self.format_logs))
                continue

    @unittest.skip('请求被限制 -> test_006 Pass')
    def test_006(self):
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

    @unittest.skip('请求被限制 -> test_007 Pass')
    def test_007(self):
        """future 通过下单测试 -> moneyPrecision 与 basePrecision+minOrderSize"""
        print(list_future_c)
        print(sy_obj_future)

    def test_008(self):
        """查看 spot 与 future 资金"""
        j = {
            "accountId": a_id
        }
        result = requests.post(getAsset, json=j, headers=header)
        print('<---------- spot ---------->')
        for i in result.json()['data']['position']['spot']:
            print(i)

        print('<---------- future ---------->')
        for i in result.json()['data']['position']['future']:
            print(i)
        return result

    def test_009(self):
        """整合并格式化输出日志"""

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

    def test_010(self):
        """ BitFinex -> 查看错误输出"""

        er = 0

        with open(self.logs_path + self.f_name, 'r', encoding='utf-8') as f:
            fs = f.read()
            if not fs:
                print('not error')
            else:
                print(fs)
                er += 1
        assert er == 0

    @unittest.skip('分组调试 -> Pass')
    def test_09999(self):
        self.test_001()
        self.test_002()
        self.test_003()
        self.test_004()

        # self.test_099999()
        # self.test_005()
        # self.test_006()

        # self.test_009()
        # self.test_010()

        # r = generating_orders(a_id, exchange, 'spot', 'normal', '0.00043351', '0.6001', 'buy', 'etc_btc')
        # print(r.json())
        # while True:
        #     if r.json()['code'] == 2000 and '响应失败' in r.json()['message']:
        #         r = generating_orders(a_id, exchange, 'spot', 'normal', '0.00043351', '0.6001', 'buy', 'etc_btc')
        #     else:
        #         print('请求成功')
        #         break

    @unittest.skip('分组调试 -> Pass')
    def test_099999(self):
        """1"""
        list_c = 30  # 调试
        sy_ob = 'bitfinex:spot_list_'  # 调试
        # test_sy_ob = 'bitfinex:spot_list_{}'.format("%05d" % 171)

        for i in range(1, list_c + 1):

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
            p = get_url_order_book(ob_ex_exType, sy).json()
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
                sss = '{} -> OrderBook未找到该币对'.format(sy)
                self.format_logs['msg'] = str(d)
                self.format_logs['send'] = sss
                R.set('test_005->OrderBook未找到该币种->ID:{}'.format(n), str(self.format_logs))
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

            error_obj = {
                '币对测试ID': str(n),
                '币种对象': str(d),
                '下单金额': str(this_p),
                '下单数量': str(order_q),
                'json_res': ''
            }

            # 下单
            sleep(30)
            r = generating_orders(a_id, exchange, 'spot', 'normal', this_p, order_q, 'buy', sy)  # buy
            # r = generating_orders(a_id, exchange', 'spot', 'normal', this_p, order_q, 'sell', sy)  # sell
            print(r.json())
            while True:
                if r.json()['code'] == 2000 and '响应失败' in r.json()['message']:
                    r = generating_orders(a_id, exchange, 'spot', 'normal', this_p, order_q, 'buy', sy)
                else:
                    if r.json()['code'] == 2000 and '请求超过频率限制' in r.json()['message']:
                        self.format_logs['send'] = ''
                        self.format_logs['msg'] = str(r.json())
                        R.set('test_005->请求被限制->ID{}'.format(n), str(self.format_logs))
                        sleep(30)
                        break
                    else:
                        print('下单api->请求成功')
                        break

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
            while True:
                if order_status['code'] == 2000 and '响应失败' in order_status['message']:
                    order_status = check_order(a_id, exchange, exchangeType, orderId, symbol, all_json=True)
                else:
                    print('获取订单api->请求成功')
                    break

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
                r = cancel_order(a_id, exchange, exchangeType, orderId, symbol)
                while True:
                    if r.json()['code'] == 2000 and '响应失败' in r.json()['message']:
                        r = cancel_order(a_id, exchange, exchangeType, orderId, symbol)
                    else:
                        print('撤单api->请求成功')
                        break

                print('====================end test -> {} -> {}====================\n'.format(n, sy))


if __name__ == '__main__':
    unittest.main()
