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
        return
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


# 订单/精度相关公共类
class CommonFunc:
    """公共类"""

    def clear_db_08(self, R):
        """测试数据init"""
        R.flushdb()
        # R.flushall()
        print('redis db{} flushall .....'.format(R))

    def check_sy_kv(self, sy, R):
        """
        检查symbol参数 最要包括:moneyPrecision,basePrecision,minOrderSize,minOrderValue

        :param sy:
        :param R:
        :return:

        """
        demo = {'exSymbol': 'knc_btc', 'symbol': 'knc_btc', 'exBaseCoin': 'knc', 'exMoneyCoin': 'btc',
                'baseCoin': 'knc',
                'moneyCoin': 'btc', 'basePrecision': '0.001', 'moneyPrecision': '0.0000001', 'minOrderSize': '1',
                'symbolType': 'spot', 'tradeType': 'knc', 'multiplier': '1'}

        if not sy.get('moneyPrecision') or not sy.get('basePrecision'):
            print('moneyPrecision 或 basePrecision 为 None')
            R.set('error->symbol缺少参数->{}'.format(shortuuid.uuid()), str(sy))

        if float(sy.get('moneyPrecision')) <= 0 or float(sy.get('basePrecision')) <= 0:
            print('moneyPrecision 或 basePrecision 值 < 0')
            R.set('error->symbol缺少参数->{}'.format(shortuuid.uuid()), str(sy))

        if not sy.get('minOrderSize') and not sy.get('minOrderValue'):
            print('minOrderSize 与 minOrderValue 为 None')
            R.set('error->symbol缺少参数->{}'.format(shortuuid.uuid()), str(sy))

        if sy.get('minOrderSize'):
            if float(sy.get('minOrderSize')) <= 0:
                print('minOrderSize  <= 0')
                R.set('error->symbol缺少参数->{}'.format(shortuuid.uuid()), str(sy))

        if sy.get('minOrderValue'):
            if float(sy.get('minOrderValue')) <= 0:
                print('minOrderValue  <= 0')
                R.set('error->symbol缺少参数->{}'.format(shortuuid.uuid()), str(sy))

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

    def money_transfer(self, accountId, amount, coin, from_, symbol, to_):
        """
        资金划转
        :param accountId: 帐户id
        :param amount: 划转数量
        :param coin: 币种，如BTC
        :param from_: 转出账户 如 spot
        :param symbol: 币对，如btc_usdt
        :param to_: 转入账户
        :return:

        {
          "accountId": "4993",
          "amount": 5,
          "coin": "usdt",
          "from": "spot",
          "symbol": "trx_usdt",
          "to": "margin"
        }

        """

        mt = {
            "accountId": accountId,
            "amount": amount,
            "coin": coin,
            "from": from_,
            "symbol": symbol,
            "to": to_
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


if __name__ == '__main__':
    pass
