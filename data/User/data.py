# -*- coding: utf-8 -*-
# @Time    : 2019-10-07 16:54
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : test_data.py
# @Software: PyCharm


import time
import hashlib
import hmac
import base64

print(time.time())
print(int(time.time() * 1000))

user_id = 'f089334d-b0c9-42b2-aea3-950b2b6ac697'

# user_id + str(int(time.time()*1000)) + sk
