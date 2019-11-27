# -*- coding: utf-8 -*-
# @Time    : 2019-10-23 19:20
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : OrderFunc.py
# @Software: PyCharm

from all_import import *
from config.data.test_data import *


# 下单
def generating_orders(accountId, exchange, exchangeType, postType, price, qty, side, symbol):
    """
    :param accountId:       accountId
    :param exchange:        交易所
    :param exchangeType:    交易类型  币币-> spot, 杠杆-> margin, 交割-> future, 永续-> swap
    :param postType:                 默认-> normal , 吃单-> post_only
    :param side:            交易方向
    :return:

    币币 -> 下单/挂单
    杠杆 -> 下单/挂单
    永续 -> 下单/挂单
    交割 -> 下单/挂单

    """

    # exchange = 'okex'
    # exchangeType = 'spot'
    # postType = 'normal'
    # price = '1'
    # qty = '1'
    # side = 'buy'
    # symbol = 'ltc_okb'

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
        "price": price,
        "qty": qty,
        "side": side,
        "symbol": symbol,
        "type": "limit"
    }
    print('send json -> {} '.format(d))

    if exchangeType == 'spot':
        print('func -> generating_orders data -> spot')
        result = requests.post(placeOrder, json=d, headers=header)
        return result
    if exchangeType == 'margin':
        print('func -> generating_orders data -> margin')
        result = requests.post(placeOrder, json=d, headers=header)
        return result
    if exchangeType == 'future':
        print('func -> generating_orders data -> future')
        result = requests.post(placeOrder, json=d, headers=header)
        return result
    if exchangeType == 'swap':
        print('func -> generating_orders data -> swap')
        return


# 撤单
def cancel_order(accountId, exchange, exchangeType, orderId, symbol):
    co = {
        "accountId": accountId,
        "customId": "",
        "exchange": exchange,
        "exchangeType": exchangeType,
        "orderId": orderId,
        "symbol": symbol
    }
    result = requests.post(cancelOrder, json=co, headers=header)
    print(result.json())
    return result


#  查看订单状态
def check_order(accountId, exchange, exchangeType, orderId, symbol, all_json=False):
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
    if result.json()['code'] == 1000 and not all_json:
        return result.json()['data']['status']
    elif all_json and result.json()['code'] == 1000:
        return result.json()

    else:
        return result.json()


# 查看挂单list
def get_active_orders(accountId, exchange, exchangeType):
    """获取活跃订单列表"""
    ao = {
        "accountId": accountId,
        "exchange": exchange,
        "exchangeType": exchangeType,
        "readFromCache": True,
        "symbol": ""
    }
    result = requests.post(getActiveOrders, json=ao, headers=header)
    # print(result.json())
    return result


# 获取交易所所有币对list
def get_url_symbol_list(exchange, R):
    """

    moneyPrecision -> 下单价格精度
    basePrecision  -> 下单数量精度
    minOrderSize   -> 下单数量
    minOrderValue  -> 下单价值

    :param exchange:  交易所:子市场 -> okex:spot
    :return:
    """
    kv = {
        'exchange': exchange
    }
    result = requests.get(Symbol_url, kv)
    print(type(result.json()['data']))
    v = result.json()['data']
    print(v)
    R.set(exchange, str(v))
    return


# 分开保存每一个币种到Redis
def save_symbol_obj(s, R):
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


# 获取交易所所有买卖档位价格与数量
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
    return result


# 获取ticker币对金额(不精准)
def get_ticker(exchange, symbol, contractType=''):
    """

    :param exchange:        okex:spot
    :param symbol:          trx_okb
    :param contractType:    期货的合约类型，如果是现货或杠杆时填空即可 -> this_week,quarter,swap
    :return:
    """
    da = {
        'contractType': contractType,
        'exchange': exchange,
        'symbol': symbol
    }
    result = requests.get(ticker, da)
    print(result.json())
    return result


# 格式化8位小数
def bl8(n):
    """
    保留8位小数
    :param n:
    :return:
    """
    return round(float(n), 8)


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
        if '.' not in str(number):
            return str(number) + '.0'
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
    if isinstance(s, int):
        s = str(float(s))
    else:
        s = str(as_num(s))

    print('first_add -> 传入金额:', s)

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


def first_add(s, sell=False):
    """

    :param s:      浮点数字符串
    :param sell:   卖加 买减 -> 默认:买减
    :return:
    """
    k = '0.'
    if isinstance(s, int):
        s = str(round(float(s), 1))
    else:
        s = str(as_num(s))

    print('first_add -> 传入金额:', s, type(s))

    s_obj = s.split('.')  # '0' + '0123'
    print('s_obj s_obj s_obj s_obj', s_obj)
    print('s_obj[0]', s_obj[0])
    print('s_obj[1]', s_obj[1])
    print(len(s_obj[1]))
    if int(s_obj[0]) == 0:
        if sell:
            print('sell')
            okc = kexue_add(float(s) + 0.1, len(str(s_obj[1])))
            print('计算结果:', okc, type(okc))
            return okc

        else:
            print('buy')
            s_obj_index = []
            add_list = []
            if len(s_obj[1]) >= 1:
                for index, i in enumerate(s_obj[1]):
                    if int(i) > 0:  # 如果为 0 往后推一为再减少
                        s_obj_index.append(int(index))  # 组装值 >0 索引 list

                print('符合格式的索引列表:{}'.format(s_obj_index))

                for j in s_obj_index:
                    c_num = k + '0' * int(j) + '1'  # 生成计算精度: k + '0' * index + '1'
                    add_list.append(c_num)
                    print(c_num)

                    okc = kexue_add(float(s) - float(c_num), len(str(s_obj[1])))  # 格式化科学计数
                    print(okc)

                    print('{} - {} = {} -> {} -> {}'.format(s, c_num, okc, type(okc), float(okc)))

                    if float(okc) == 0:
                        print('Calculation results is zero ')
                        print(okc + '1', type(okc + '1'))
                        return okc + '1'  # 末尾补 1 -> '0.00000000'+'1'
                    else:
                        print('计算结果:', okc, type(okc))
                        return okc
                print('计算值的列表:{}'.format(add_list))

    else:
        print('整数位 > 0')

        lens = len(str(s_obj[0])) - 1  # 整数位第一位+1
        add_okc = '1{}'.format('0' * lens)
        print('计算的值:{}'.format(add_okc))

        if sell:
            print('sell')
            okc = kexue_add(float(s) + float(add_okc), len(str(s_obj[1])))
            print(okc, type(okc))
            return okc
        else:
            print('buy')
            okc = kexue_add(float(s) - float(add_okc), len(str(s_obj[1])))
            print(okc, type(okc))
            return okc


# 订单/精度相关公共类
class CommonFunc:
    """公共类"""

    def clear_db_08(self, R):
        """测试数据init"""
        R.flushdb()
        # R.flushall()
        print('redis db{} flushall .....'.format(R))

    def check_sy_kv(self, redis_id, sy, R):
        """
        检查symbol参数 最要包括:moneyPrecision,basePrecision,minOrderSize,minOrderValue

        :param redis_id:
        :param sy:
        :param R:
        :return:


        精度规则：
            1. moneyPrecision、basePrecision ->必须不为空
            2. minOrderSize，minOrderValue   ->不能同时为空
            3. 上述四个字段非空时，必须大于0

        """
        demo = {'exSymbol': 'knc_btc', 'symbol': 'knc_btc', 'exBaseCoin': 'knc', 'exMoneyCoin': 'btc',
                'baseCoin': 'knc',
                'moneyCoin': 'btc', 'basePrecision': '0.001', 'moneyPrecision': '0.0000001', 'minOrderSize': '1',
                'symbolType': 'spot', 'tradeType': 'knc', 'multiplier': '1'}

        new_obj = {
            'redis_id': redis_id,
            'redis_err': '',
            'result': str(sy)
        }

        # print(sy)
        # print(sy.get('moneyPrecision'), type(sy.get('moneyPrecision')))
        # print(float(sy.get('moneyPrecision')), type(float(sy.get('moneyPrecision'))))
        # print(round(float(sy.get('moneyPrecision')), len(sy.get('moneyPrecision').split('.')[1])))

        try:
            if not sy.get('moneyPrecision') or not sy.get('basePrecision'):
                print('moneyPrecision 或 basePrecision 为 None')
                new_obj['redis_err'] = 'moneyPrecision 或 basePrecision 为 None'
                sy.update(new_obj)
                R.set('test_003->币对参数有误->ID:{}'.format(redis_id), str(sy))

            if float(sy.get('moneyPrecision')) <= 0 or float(sy.get('basePrecision')) <= 0:
                print('moneyPrecision 或 basePrecision 值 < 0')
                new_obj['redis_err'] = 'moneyPrecision 或 basePrecision 值 < 0'
                sy.update(new_obj)
                R.set('test_003->币对参数有误->ID:{}'.format(redis_id), str(sy))

            if not sy.get('minOrderSize') and not sy.get('minOrderValue'):
                print('minOrderSize 与 minOrderValue 都为空')
                new_obj['redis_err'] = 'minOrderSize 与 minOrderValue 都为空'
                sy.update(new_obj)
                R.set('test_003->币对参数有误->ID:{}'.format(redis_id), str(sy))

            if sy.get('minOrderSize'):
                if float(sy.get('minOrderSize')) <= 0:
                    print('minOrderSize  <= 0')
                    new_obj['redis_err'] = 'minOrderSize  <= 0'
                    sy.update(new_obj)
                    R.set('test_003->币对参数有误->ID:{}'.format(redis_id), str(sy))

            if sy.get('minOrderValue'):
                if float(sy.get('minOrderValue')) <= 0:
                    print('minOrderValue  <= 0')
                    new_obj['redis_err'] = 'minOrderValue  <= 0'
                    sy.update(new_obj)
                    R.set('test_003->币对参数有误->ID:{}'.format(redis_id), str(sy))
        except BaseException as e:
            new_obj['redis_err'] = str(e)
            sy.update(new_obj)
            R.set('next_test_003->忽略check_sy_kv的try->ID:{}'.format(redis_id), str(sy))

    def check_odb(self, list_count, sy_first_key, ex_and_ext, R, redis_first_key):
        """

        :param list_count:      交易所币对总数
        :param sy_first_key:    币对前缀: 如 huobi:margin_list_
        :param ex_and_ext:      交易所与交易类型: 如 'huobi:spot'
        :param R:               redis实例
        :param redis_first_key: 用例标示
        :return:
        """
        for i in range(1, list_count + 1):

            try:
                print(i)
                n = "%05d" % i
                print('编号:', n, type(n))

                dic_obj = eval('(' + R.get(sy_first_key + n) + ')')
                print('-----moneyPrecision-----')
                print(dic_obj, type(dic_obj))
                print('moneyPrecision -> {}'.format(dic_obj['moneyPrecision']))
                print('\n')

                print('-----orderbook-----')
                jd_list_init = get_url_order_book(ex_and_ext, dic_obj['symbol']).json()

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
                        new_obj = {
                            'redis_id': n,
                            'redis_err': '该用例检验参数:moneyPrecision:{}与OrderBook精度:{}不一致'.format(
                                str(dic_obj['moneyPrecision']), asks_and_bids_c),
                            'result': ''
                        }
                        dic_obj.update(new_obj)
                        R.set('{}->币种精度与OrderBook不相符->{}'.format(redis_first_key, n), str(dic_obj))
                else:
                    new_obj = {
                        'redis_id': n,
                        'redis_err': 'OrderBook未找到该币对',
                        'result': jd_list_init
                    }
                    dic_obj.update(new_obj)
                    R.set('{}->OrderBook未找到该币种->ID{}'.format(redis_first_key, n), str(dic_obj))
                    continue
            except BaseException as e:
                new_obj = {
                    'redis_id': n,
                    'redis_err': '{}->外层func执行异常:{}'.format(redis_first_key, str(e)),
                    'result': '忽略'
                }
                dic_obj.update(new_obj)
                R.set('{}->外层func执行异常->ID{}'.format(redis_first_key, n), str(dic_obj))
                continue

    def money_detailed(self, accountId):
        """
        资金明细
        :param accountId: 帐户id
        :return:
        """
        j = {
            "accountId": accountId
        }
        result = requests.post(getAsset, json=j, headers=header)
        return result

    def money_transfer(self, accountId, amount, coin, from_, fromSymbol, to_, toSymbol, update=False):
        """
        资金划转
        :param accountId: 帐户id
        :param amount: 划转数量
        :param coin: 币种，如BTC
        :param from_: 转出账户 如 spot
        :param fromSymbol: 转出币对 如btc_usdt
        :param symbol: 币对，如btc_usdt
        :param to_: 转入账户
        :param toSymbol: 转入币对 如btc_usdt
        :param update: 默认为false
        :return:


        {
          "accountId": "5016",
          "amount": 0.00072815,
          "coin": "btc",
          "from": "spot",
          "fromSymbol": "btt_btc",
          "to": "margin",
          "toSymbol": "btt_btc",
          "update": true
        }
        demo:
            mt = self.money_transfer(a_id, '0.00072815', 'btc', 'spot', 'btt_btc', 'margin', 'btt_btc', update=True).json()
            print(mt)

        """

        mt = {
            "accountId": accountId,
            "amount": amount,
            "coin": coin,
            "from": from_,
            "fromSymbol": fromSymbol,
            "to": to_,
            "toSymbol": toSymbol,
            "update": update,
        }
        result = requests.post(transfer, json=mt, headers=header)
        return result

    def money_spot_margin(self, accountId):
        r = self.money_detailed(accountId).json()
        spot_money = r['data']['position']['spot']
        margin_money = r['data']['position']['margin']

        print('<---------- spot ---------->')
        for i in spot_money:
            if i['symbol'] in ['btc', 'usdt', 'usdk', 'eth']:
                print(i)

        print('<---------- all spot ---------->')
        for i in spot_money:
            print(i)

        print('<---------- margin ---------->')
        for j in margin_money:
            print(j)

    def format_output_log(self, exchange, R, R2, file_path):
        """
        整合并格式化输出日志
        :param exchange:    交易所名称
        :param R:           错误日志 redis db
        :param R2:          整合后存放的 redis db
        :param file_path:   生成日志文件的路径
        :return:
        """

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
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(tb))
            # print(tb)

        else:
            tb.add_row(['null', 'null', 'null'])
            print('===未发现错误===')
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('')
            # print(tb)

    def see_err_output(self, file_path, file_name):
        """
        查看错误输出
        :param file_path: 文件路径
        :param file_name: 文件名称
        :return:
        """

        er = 0

        with open(file_path, 'r', encoding='utf-8') as f:
            fs = f.read()
            if not fs:
                print('not error')
            else:
                # print(fs)
                print('错误日志记录')
                print('AirCurrency/logs/{}'.format(file_name))
                er += 1
        assert er == 0


if __name__ == '__main__':
    pass
    print(get_active_orders('5016', 'huobi', 'spot').json())
    print(get_active_orders('5016', 'huobi', 'spot').json()['data'][0]['orderId'])
    print(get_active_orders('5016', 'huobi', 'spot').json()['data'][0]['status'])

    # x = '56997877086'
    # res = check_order('5016', 'huobi', 'spot', x, 'trx_usdt')
    # print('\n')
    # print(res)
