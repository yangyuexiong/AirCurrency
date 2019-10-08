# -*- coding: utf-8 -*-
# @Time    : 2019-10-08 11:20
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : data.py
# @Software: PyCharm


'''
    "accountId": "4993",
    "exchange": "okex",
    "exchangeType": "string",   # spot, margin, future, swap
    "postType": "string",       # 默认 normal，可选post_only
    "price": "string",          # 金额
    "qty": "string",            # 数量
    "side": "string",           # 买卖方向，默认有 buy, sell, open_buy, open_sell, close_buy, cloe_sell
    "symbol": "string",         # 币对如btc_usdt
    "type": "string"            # 默认 limit，不支持market
'''

d = {
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


def init_data():
    d = {
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
    return d


def reset_data(data):
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


if __name__ == '__main__':
    pass
    x = {
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
    r = reset_data(x)
    print(r)
