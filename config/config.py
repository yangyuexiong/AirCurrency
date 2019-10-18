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
            n = format(ctx.create_decimal(str(number)), 'f')
            # '{:.10f}'.format(self)
            return round(ctx.create_decimal(float(number)), len(n.split('.')[1]))
            # return ctx.create_decimal(str(number))
        else:
            # print(number, type(number))
            return number


    def last_add_2(s, sell=False):
        """

        :param s:      浮点数字符串
        :param sell:   卖加 买减
        :return:
        """
        k = '0.'
        s = as_num(s)
        print(s)

        """处理只有一位小数 或者 整数 例: 0.1"""
        if len(s.split('.')[1]) < 2:
            if sell:
                r = float(s) + 0.5  # 卖 +0.5 买 -0.5
                print(r)
                return str(r)
            else:
                r = float(s)
                if 0.5 > r > 0.2:
                    r = round(r - 0.1, len(s) - 2)
                    print(r)
                    return str(r)

                else:
                    print(r)
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
            print(r)
            return str(r)
        else:
            if int(s[-2:-1]) == 0:  # 值的倒数第二位为 0 往后 推一位
                print(type(float(s)))
                msg = '{} - {}'.format(float(s), as_num(float(ss) / 10))
                print(msg)
                r = kexue_add((float(s)) - (float(ss) / 10), len(s) - 2)
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


    # last_add_2('0.012')
    last_add_2('0.0000103')
    # last_add_2('0.6')

    print(float(1))
    print(str(float(1)))
