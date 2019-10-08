# -*- coding: utf-8 -*-
# @Time    : 2019-10-07 15:33
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : Urls.py
# @Software: PyCharm

"""
登录平台获取token ->
验证 -> verifyWebToken
生成SToken -> genSToken

"""
BaseUrl = 'https://test.bithelp.top/private-api'

Token = 'ADD44DB572D23684C3C047E9087588A67aeee0a758bc49e98626503da22dcfe7'

header = {
    'webToken': Token
}

cookie = {
    "cookie": "trade_token=FF7D6C7E6280B9E67523947DF90577A946778b750a2e4ba1b0c959aa3aff8266"
}

# user
verifyWebToken = BaseUrl + '/auth/verifyWebToken'  # 验证web会话

genSToken = BaseUrl + '/auth/genSToken'  # 生成sToken

removeST = BaseUrl + '/auth/remove'  # 销毁sToken

user_info = BaseUrl + '/user/info'  # 用户信息

# order
placeOrder = BaseUrl + '/order/placeOrder'  # 下单
