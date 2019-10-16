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

    def rt_max_len(list_obj):

        rt_dict = {

        }
        for i in list_obj:
            rt_dict[len(i)] += 1


    l1 = ['3', 'aa', 'bb', 'ccc', '222', '333', '444', '1', '2']


    # sorted(list, key=lambda x: len(x))[0]

    # print(sorted(l, key=lambda x: len(x))[-1])

    # for k, v in list(zip(range(0, len(l)), l)):
    #     d = {}
    #     print(k, v)
    #     d[k]

    def count_list_max_len(list):
        """
        key:value
        长度:[长度,下标]

        :param list:
        :return:
        """
        d = {}
        d2 = {}
        for i in list:
            if not d.get(len(str(i))):
                d[len(str(i))] = [1, '{}'.format(i)]
            else:
                n1 = d.get(len(str(i)))[0]
                n2 = i
                d[len(str(i))] = [n1 + 1, n2]
        print(d)
        # in_key = sorted(d.items(), key=lambda x: x[0])
        # in_value = sorted(d.items(), key=lambda x: x[1])
        # print(in_key)
        # print(in_value)
        # print(in_key[-1][1][1])
        for k, v in d.items():
            d2[v[0]] = v[1]

        print(sorted(d2.items(), key=lambda x: x[0]))
        return 1


    dd = {4: [51, 0.15], 3: [6, 0.2], 1: [1, '1'], 6: [2, 0.1288]}

    # print(sorted(dd.items(), key=lambda x: x[0]))
    # print(sorted(dd.items(), key=lambda x: x[1]))
    # print(sorted(dd.items(), key=lambda x: x[1])[-1][1][-1])

    # print(count_list_max_len(dd))
    print(sorted(dd.items(), key=lambda x: x[0]))


    def cnmd(d):
        d2 = {}
        for k, v in d.items():
            d2[v[0]] = v[1]
        print(d2)
        print(sorted(d2.items(), key=lambda x: x[0]))
        print(sorted(d2.items(), key=lambda x: x[0])[-1][1])
        return sorted(d2.items(), key=lambda x: x[0])[-1][1]


    cnmd(dd)