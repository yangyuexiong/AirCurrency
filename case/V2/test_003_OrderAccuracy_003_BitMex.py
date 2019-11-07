# -*- coding: utf-8 -*-
# @Time    : 2019-10-30 17:54
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_003_OrderAccuracy_003_BitMex.py
# @Software: PyCharm

from all_import import *
from config.data.test_data import *
from common.OrderFunc import *
from case.V2.test_003_OrderAccuracy_001_OKEX import as_num, cnmd, count_list_max_len, first_add, kexue_add, ad_price

a_id = accountId_to_dict.get('bitmex')
ob_ex_exType = 'bitmex:future'
exchange = 'bitmex'
R = redis_obj(13)


@unittest.skip('VPN -> Pass')
class TestOrderAccuracyForBITFINEX(StartEnd, CommonFunc):
    """BitMex"""

    # btc_usd_xbtz19    12季度合约
    # btc_usd_xbtu19    9季度合约
    # btc_usd_xbtusd    永续合约

    error_num = 0
    logs_path = os.getcwd().split('case')[0] + '/logs'
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    f_name = '/BitMex_log_{}.txt'.format(now)
    format_logs = {
        'msg': '',
        'send': ''
    }

    def test_001(self):
        """获取交易所所有Symbol(future) -> 储存至Redis"""
        self.clear_db_08(R)
        get_url_symbol_list('bitmex:future', R)

    def test_002(self):
        """将Symbol list 中每一个币对象分开储存 -> Redis"""
        res_future = save_symbol_obj('bitmex:future', R)

        print('bitfinex:future -> {}'.format(res_future))
        print(res_future[0])
        print(res_future[1])

        global list_future_c
        global sy_obj_future
        list_future_c = int(res_future[0])  # future 总数
        sy_obj_future = res_future[1][:-5]

    def test_003(self):
        """检查币对参数"""
        print(list_future_c)
        print(sy_obj_future)

        print('========== check future ==========')
        for i in range(1, list_future_c + 1):
            print(i)
            n = "%05d" % i
            print(n, type(n))

            dic_obj = eval('(' + R.get(sy_obj_future + n) + ')')
            print(dic_obj, type(dic_obj))

            self.check_sy_kv(dic_obj, R)

        print('========== check future success ==========')

    def test_007(self):
        """future 通过下单测试 -> moneyPrecision """
        # print(list_future_c)
        # print(sy_obj_future)

        list_future_c = 1  # 调试
        sy_obj_future = 'bitmex:future_list_'  # 调试

        for i in range(1, list_future_c + 1):
            n = "%05d" % i
            d = eval('(' + R.get(sy_obj_future + n) + ')')

            sy = d['symbol']
            print('====================test -> {} -> {}===================='.format(n, sy))
            sy_l = d['symbol'].split('_')[0]
            sy_r = d['symbol'].split('_')[1]
            print(d, type(d))
            print('symbol -> {}'.format(sy))
            print('买入币种 -> {}'.format(sy_l))
            print('使用币种 -> {}'.format(sy_r))
            print('最少下单量 -> {}'.format(d['minOrderSize']))
            print('\n')

            # 买减->sell 卖加->buy
            # asks:卖盘  bids:买盘
            p = get_url_order_book('bitmex:future', sy).json()
            print('orderbook -> {} \n'.format(p))

            if p.get('data', None):

                asks_one = p['data']['asks'][0][0]
                bids_one = p['data']['bids'][0][0]
                print('卖一:{}'.format(asks_one))
                print('买一:{}'.format(bids_one))

                buy_list = [p['data']['asks'][0][0], p['data']['asks'][1][0], p['data']['asks'][2][0]]
                buy_list2 = [as_num(i) for i in buy_list]
                print('buy_list -> ', buy_list)
                print('buy_list_to_float -> ', buy_list2)
                print('\n')

                p = first_add(bids_one)
                p1 = first_add(ad_price(buy_list2))
                print('\n')
                print('*下单金额:', p, type(p))
                print('*防止精度丢失备用下单金额:', p1, type(p1))
            else:
                sss = '{} -> 交易所或OrderBook未找到该币种'.format(sy)
                self.format_logs['msg'] = str(d)
                self.format_logs['send'] = sss
                R.set('test_007->交易所或OrderBook未找到该币种->{}'.format(i), str(self.format_logs))
                print('====================end test -> orror {} -> {}====================\n'.format(n, sy))
                continue

            if len(p) >= len(p1):
                this_p = p
                print('===没有丢失精度===\n')
            else:
                this_p = p1
                print('===原下单金额丢失精度->使用备用下单金额执行下单操作===\n')

            print('===数量精度提取===')
            minOrderSize = d['minOrderSize']
            print(minOrderSize)

            r = generating_orders(a_id, exchange, 'future', 'normal', this_p, minOrderSize, 'open_buy', sy)
            print(r.json())


if __name__ == '__main__':
    unittest.main()
