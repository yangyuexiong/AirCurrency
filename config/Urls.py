# -*- coding: utf-8 -*-
# @Time    : 2019-10-07 15:33
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : Urls.py
# @Software: PyCharm

import os

from config.data.test_data import sToken
from config.config import redis_obj

"""
登录平台获取token ->
验证 -> verifyWebToken
生成SToken -> genSToken

"""
R = redis_obj(3)
if not R.get('RUN_ENV'):
    R.set('RUN_ENV', 'dev')
elif R.get('RUN_ENV') == 'pro':
    BaseUrl = 'https://www.coinfat.com'
else:
    BaseUrl = 'https://test.bithelp.top/private-api'

Token = 'ADD44DB572D23684C3C047E9087588A67aeee0a758bc49e98626503da22dcfe7'

header = {
    'trade_sToken': sToken,
    # 'webToken': Token
}

cookie = {
    "cookie": "trade_token=FF7D6C7E6280B9E67523947DF90577A946778b750a2e4ba1b0c959aa3aff8266"
}

"""--------------------private-api--------------------"""
# User
verifyWebToken = BaseUrl + '/auth/verifyWebToken'  # 验证web会话
genSToken = BaseUrl + '/auth/genSToken'  # 生成sToken
removeST = BaseUrl + '/auth/remove'  # 销毁sToken
user_info = BaseUrl + '/user/info'  # 用户信息

# Order
placeOrder = BaseUrl + '/order/placeOrder'  # 下单
cancelOrder = BaseUrl + '/order/cancelOrder'  # 撤销订单
getOrderById = BaseUrl + '/order/getOrderById'  # 订单查询
getActiveOrders = BaseUrl + '/order/getActiveOrders'  # 活跃订单(挂单)

# Asset
getAsset = BaseUrl + '/assets/getAsset'  # 获取资产
getLeverage = BaseUrl + '/assets/getLeverage'  # 获取杠杆倍数
transfer = BaseUrl + '/assets/transfer'  # 资金划转

"""--------------------public-api--------------------"""
BaseUrl2 = 'https://test.bithelp.top/public-api'
ticker = BaseUrl2 + '/api/public/ticker'  # 获取Ticker
Symbol_url = BaseUrl2 + '/api/public/symbols'  # 获取Symbol
Orderbook = BaseUrl2 + '/api/public/orderbook'  # 获取Orderbook
