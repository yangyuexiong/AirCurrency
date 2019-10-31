# -*- coding: utf-8 -*-
# @Time    : 2019-10-31 10:47
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : func_test.py
# @Software: PyCharm


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


def ad_price(price_list):
    """
    过滤失去精度的下单价格
    :param price_list:
    :return:
    """
    new_d = list(zip(price_list, list(range(len(price_list)))))
    lens = 0
    new_l = []
    print(new_d)
    for i in new_d:
        x = list(i)
        print('x -> ', x)
        x[1] = len(str(x[0]))
        print(x)
        if int(x[1]) >= lens:
            print('lens-', lens)
            lens = int(x[1])
            new_l.append(x[0])
        else:
            pass
    print('数据长度-> {}'.format(lens))
    n = 0
    for j in range(len(new_l)):
        if len(str(new_l[n])) < lens:  # 第一个元素长度<目标长度
            new_l.pop(n)  # 删除
        else:
            n += 1  # 索引+1
    print('符合精度的价格list -> ', new_l, len(new_l))
    print('提取价格 -> ', new_l[0])
    return new_l[0]


test001 = ['0.0000041', '0.0000042', '0.00000421', '0.00000422', '0.00000432', '0.00000433', '0.00000439',
           '0.0000044', '0.00000446', '0.00000449', '0.00000453', '0.0000046', '0.00000464', '0.00000473',
           '0.00000476', '0.00000487', '0.00000497', '0.000005', '0.00000505', '0.00000509', '0.00000512',
           '0.00000515', '0.00000521', '0.00000525', '0.00000536', '0.00000539', '0.00000544', '0.00000576',
           '0.0000084', '0.00000849', '0.00000401', '0.000004', '0.00000399', '0.00000398', '0.00000397',
           '0.00000395', '0.00000392', '0.00000391', '0.0000039', '0.00000389', '0.00000388', '0.00000382',
           '0.00000381', '0.0000038', '0.00000379', '0.00000378', '0.00000377', '0.00000376', '0.00000375',
           '0.00000374', '0.00000373', '0.00000372', '0.00000371', '0.0000037', '0.00000369', '0.00000367',
           '0.00000366', '0.00000365', '0.00000364', '0.00000363']


# ad_price(test001)
# print(cnmd(count_list_max_len(test001)))

def first_add(s, sell=False):
    """

    :param s:      浮点数字符串
    :param sell:   卖加 买减 -> 默认:买减
    :return:
    """
    k = '0.'
    if isinstance(s, int):
        s = str(round(float(s), 1))
    else:
        s = str(as_num(s))

    print('first_add -> 传入金额:', s, type(s))

    s_obj = s.split('.')  # '0' + '0123'
    print(s_obj[0])
    print(s_obj[1])
    print(len(s_obj[1]))
    if int(s_obj[0]) == 0:
        if sell:
            print('sell')
            okc = kexue_add(float(s) + 0.1, len(str(s_obj[1])))
            print(okc, type(okc))
            return okc

        else:
            print('buy')
            s_obj_index = []
            add_list = []
            if len(s_obj[1]) > 1:
                for index, i in enumerate(s_obj[1]):
                    if int(i) > 0:  # 如果为 0 往后推一为再减少
                        s_obj_index.append(int(index))  # 组装值 >0 索引 list

                print('符合格式的索引列表:{}'.format(s_obj_index))

                for j in s_obj_index:
                    c_num = k + '0' * int(j) + '1'  # 生成计算精度: k + '0' * index + '1'
                    add_list.append(c_num)
                    print(c_num)

                    okc = kexue_add(float(s) - float(c_num), len(str(s_obj[1])))  # 格式化科学计数
                    print(okc)

                    print('{} - {} = {} -> {} -> {}'.format(s, c_num, okc, type(okc), float(okc)))

                    if float(okc) == 0:
                        print('Calculation results is zero ')
                        print(okc + '1', type(okc + '1'))
                        return okc + '1'  # 末尾补 1 -> '0.00000000'+'1'
                    else:
                        print(okc, type(okc))
                        return okc
                print('计算值的列表:{}'.format(add_list))

    else:
        print('整数位 > 0')

        lens = len(str(s_obj[0])) - 1  # 整数位第一位+1
        add_okc = '1{}'.format('0' * lens)
        print('计算的值:{}'.format(add_okc))

        if sell:
            print('sell')
            okc = kexue_add(float(s) + float(add_okc), len(str(s_obj[1])))
            print(okc, type(okc))
            return okc
        else:
            print('buy')
            okc = kexue_add(float(s) - float(add_okc), len(str(s_obj[1])))
            print(okc, type(okc))
            return okc

# first_add('0.00000364', sell=True)
# first_add('57.88', sell=True)
# first_add('0.00000001', sell=True)

# first_add('0.00000364')
# first_add('57.88')
# first_add('0.00000001')

first_add('58.0')