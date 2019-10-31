# -*- coding: utf-8 -*-
# @Time    : 2019-10-10 10:51
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_data.py
# @Software: PyCharm

from all_import import *

# 用户UID的加密签名,hash=sha256((uid+timestamp),sk）
sToken = '9b09f5cd-9832-4bfe-9800-8ed5c38eefc1'

'''

下单参数:

    "accountId": "4993",
    "exchange": "okex",
    "exchangeType": "string",   # spot, margin, future, swap
    "postType": "string",       # 默认 normal，可选post_only
    "price": "string",          # 金额
    "qty": "string",            # 数量
    "side": "string",           # 买卖方向，默认有 buy, sell, open_buy, open_sell, close_buy, cloe_sell
    "symbol": "string",         # 币对如 btc_usdt
    "type": "string"            # 默认 limit，不支持market

取消订单参数:

    "accountId": "4993",
    "customId": "string",
    "exchange": "okex",
    "exchangeType": "string",   # 交易所子市场，共有：spot, margin, future, swap
    "orderId": "string",
    "symbol": "string"          # 币对如 btc_usdt

accountId*	string
账户id

exchange*	string
交易所名字

exchangeType*	string
交易所子市场，共有：spot, margin, future, swap

readFromCache*	boolean
是否从缓存中读取, true，从缓存中读取；false直接访问交易所获取数据

symbol*	string
交易对,下单使用系统映射后的交易对，使用下划线分隔，如btc_usdt；如果该字段为空，无法从交易所中获取数据，只能从缓存中获取。

'''

# okex:4993
# bitfinex:5008
# bitmex:5009
# accountId = '4993'

accountId_to_dict = {
    'okex': '4993',
    'bitfinex': '5008',
    'bitmex': '5009',
}

# 交易类型
exchangeType = {
    '币币': 'spot',
    '杠杆': 'margin',
    '交割': 'future',
    '非交割': 'swap',
}

# 交易方向
side = {
    '买': 'buy',
    '卖': 'sell',
    '开多': 'open_buy',
    '平多': 'close_buy',
    '开空': 'open_sell',
    '平空': 'close_sell',
}

# 撤单
co = {
    "accountId": '',
    "customId": "",
    "exchange": "okex",
    "exchangeType": "",
    "orderId": "",
    "symbol": ""
}


# 重置下单测试数据
def reset_place_order(data):
    init_d = {
        "accountId": "4993",
        "exchange": "okex",
        "exchangeType": "spot",
        "postType": "normal",
        "price": "1",
        "qty": "1",
        "side": "buy",
        "symbol": "ltc_okb",
        "type": "limit"
    }
    if data != init_d:
        print('F:重置参数')
        return init_d
    else:
        print('T:重置参数')
        return data


# 返回对应交易所测试数据
def return_exchange(exch):
    d = {
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
    if exch == exchange['okex']:
        d['exchange'] = exch
        return d
    if exch == exchange['火币']:
        pass
    if exch == exchange['币安']:
        pass


if __name__ == '__main__':
    pass
