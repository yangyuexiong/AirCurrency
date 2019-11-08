# -*- coding: utf-8 -*-
# @Time    : 2019-10-09 13:56
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : config.py
# @Software: PyCharm

import redis

SEND_MAIL = True

REDIS_PWD = 123456
POOL = redis.ConnectionPool(host='localhost', port=6379, password=REDIS_PWD, decode_responses=True, db=8)
R = redis.Redis(connection_pool=POOL)

"""
db0:记录测试环境异常
db1:记录生产环境异常

db3:运行环境

db5:okex测试
db6:okex生产

db7:bitfimex测试
db8:bitfimex生产

db9:
db10:

"""


def redis_obj(db_num):
    REDIS_PWD = 123456
    POOL = redis.ConnectionPool(host='localhost', port=6379, password=REDIS_PWD, decode_responses=True,
                                db=int(db_num))
    R = redis.Redis(connection_pool=POOL)
    return R


if __name__ == '__main__':
    pass
