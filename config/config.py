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


    def cnmd(d):
        d2 = {}
        for k, v in d.items():
            d2[v[0]] = v[1]
        print(d2)
        # print(sorted(d2.items(), key=lambda x: x[0]))
        # print(sorted(d2.items(), key=lambda x: x[0])[-1][1])
        return sorted(d2.items(), key=lambda x: x[0])[-1][1]


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
        print(number)
        if 'E' in str(number) or 'e' in str(number):  # 判断时候为科学计数
            n = format(ctx.create_decimal(str(number)), 'f')
            print(n)
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
        if type(s) == type(int(1)):
            s = str(float(s))
        else:
            s = str(as_num(s))

        print('传入金额:', s, type(s), 'len -> {}'.format(len(s)))

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


    def cnmd_02(d):
        d2 = {}
        for k, v in d.items():
            d2[v[0]] = [].append(v[1])
            print(d2)
        print(d2)


    # last_add_2('0.00000100')

    # print(as_num('1.02e-06'))
    # print(as_num('1e-06'))

    p = ['aaa', 'aaaaa', 'aaaa', 'bbbbb', 'ccccc']
    p1 = ['0.00000389', '0.0000039', '0.00000381', '0.00000382', '11', '22', '33', ]


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
            print('x -> ', x)
            x[1] = len(str(x[0]))
            print(x)
            if int(x[1]) >= lens:
                lens = int(x[1])
                new_l.append(x[0])
            else:
                pass
        print('符合精度的价格list -> ', new_l)
        print('提取价格 -> ', new_l[0])
        return new_l[0]


    ad_price(p1)
