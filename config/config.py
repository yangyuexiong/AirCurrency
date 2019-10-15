# -*- coding: utf-8 -*-
# @Time    : 2019-10-09 13:56
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : config.py
# @Software: PyCharm

import redis

C = True
SEND_MAIL = False

REDIS_PWD = 123456
POOL = redis.ConnectionPool(host='localhost', port=6379, password=REDIS_PWD, decode_responses=True, db=8)
R = redis.Redis(connection_pool=POOL)

if __name__ == '__main__':
    pass

    d = {
        'a': 1,
        'b': 2,
        'c': 3,

    }

    # print(d.get('a'))
    # print(d.get('d'))
    # sy_obj = 'okex:spot_list_00421'
    # print(sy_obj[:-5])

    # l1 = ['1', '2']
    # l2 = ['3', '4']
    # print(list(zip(l1, l2)))
    # print(dict(zip(l1, l2)))
    #
    # for i, j in list(zip(l1, l2)):
    #     print(i, j)

