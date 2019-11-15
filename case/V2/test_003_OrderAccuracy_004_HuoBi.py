# -*- coding: utf-8 -*-
# @Time    : 2019-11-15 16:57
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_003_OrderAccuracy_004_HuoBi.py
# @Software: PyCharm


from all_import import *
from config.data.test_data import *
from common.OrderFunc import *
from case.V2.test_003_OrderAccuracy_001_OKEX import as_num, cnmd, count_list_max_len, first_add, kexue_add, ad_price

if R.get('RUN_ENV') == 'pro':
    run_env = 'pro'
    a_id = accountId_to_dict.get('pro')['huobi']
    R = redis_obj(9)
    R2 = redis_obj(1)
else:
    run_env = 'dev'
    a_id = accountId_to_dict.get('dev')['huobi']
    R = redis_obj(10)
    R2 = redis_obj(0)

ob_ex_exType = 'huobi:spot'
exchange = 'huobi'


class TestOrderAccuracyForHuoBi(StartEnd, CommonFunc):
    """HuoBi"""

    error_num = 0
    logs_path = os.getcwd().split('case')[0] + '/logs'
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    f_name = '/HuoBi_log_{}_{}.txt'.format(run_env, now)

    print(run_env)

    def test_001(self):
        """获取交易所所有Symbol(spot,future) -> 储存至Redis"""
        self.clear_db_08(R)
        get_url_symbol_list('{}:spot'.format(exchange), R)
        get_url_symbol_list('{}:margin'.format(exchange), R)

    def test_002(self):
        """将Symbol list 中每一个币对象分开储存 -> Redis"""
        res_spot = save_symbol_obj('{}:spot'.format(exchange), R)
        res_margin = save_symbol_obj('{}:margin'.format(exchange), R)

        print('huobi:spot -> {}'.format(res_spot))
        print(res_spot[0])
        print(res_spot[1])

        print('huobi:margin -> {}'.format(res_margin))
        print(res_margin[0])
        print(res_margin[1])

        global list_c
        global sy_ob
        list_c = int(res_spot[0])  # spot 总数
        sy_ob = res_spot[1][:-5]  # spot 前缀:bitfinex:future_list_

        global list_margin_c
        global sy_obj_margin
        list_margin_c = int(res_margin[0])  # future 总数
        sy_obj_margin = res_margin[1][:-5]

    def test_003(self):
        """检查币对参数"""
        print(list_c)
        print(sy_ob)
        print(list_margin_c)
        print(sy_obj_margin)

        print('========== check spot ==========')
        for i in range(1, list_c + 1):
            print(i)
            n = "%05d" % i
            print(n, type(n))

            dic_obj = eval('(' + R.get(sy_ob + n) + ')')
            print(dic_obj, type(dic_obj))

            self.check_sy_kv(n, dic_obj, R)
        print('========== check spot success ==========')

        print('========== check future ==========')
        for i in range(1, list_margin_c + 1):
            print(i)
            n = "%05d" % i
            print(n, type(n))

            dic_obj = eval('(' + R.get(sy_obj_margin + n) + ')')
            print(dic_obj, type(dic_obj))

            self.check_sy_kv(n, dic_obj, R)

        print('========== check future success ==========')


if __name__ == '__main__':
    unittest.main()
