# -*- coding: utf-8 -*-
# @Time    : 2019-10-07 16:06
# @Author  : ShaHeTop-Almighty-ares
# @Email   : yang6333yyx@126.com
# @File    : PublicFunc.py
# @Software: PyCharm

import os


# 断言json
def assert_json(json_obj, key, v):
    assert json_obj[key] == v


# 返回sk
def return_sk():
    return


# 检查金额
def c_money():
    return


# 查找最新报告
def latest_report(report_dir):
    lists = os.listdir(report_dir)  # 报告列表
    print('报告列表', lists)
    lists.sort(key=lambda fn: os.path.getatime(report_dir + '/' + fn))  # 排序
    file = os.path.join(report_dir, lists[-1])  # 最新生成的报告
    print('最新的报告', file)
    return file


# 邮件
def send_mail(latest_report):
    import os
    import smtplib  # 发送邮件
    from email.header import Header  # 邮件标题
    from email.mime.text import MIMEText  # 邮件内容
    from email.mime.multipart import MIMEMultipart  # 邮件附件

    f = open(latest_report, 'rb')  # 打开最新报告
    print('打开报告', f)
    mail_content = f.read()  # 读取
    f.close()

    smtpserver = 'smtp.qq.com'
    user = '872540033@qq.com'
    password = 'nzxhfssrwgrhbbic'

    # 417993207
    # password = 'raqmcaefhprmcbcd'

    sender = '872540033@qq.com'
    receive = '417993207@qq.com'

    # 邮件标题-内容
    subject = '自动化测试报告'

    # 附件
    # report_img_dir = './test_report/screenshot/sgj.jpg'
    # send_file = open(report_img_dir, 'rb').read()
    # att = MIMEText(send_file, 'base64', 'utf-8')  # 编码
    # att = ['Content-Type'] = 'application/octet-stream'  # 文件类型二进制
    # att = ["Content-Disposition"] = 'attachment;filename="sgj.png"'

    # 邮件正文
    msg = MIMEText(mail_content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = receive

    # SSL协议端口号
    smtp = smtplib.SMTP_SSL(smtpserver, 465)

    # 认证
    smtp.helo(smtpserver)  # 向服务器标识身份
    smtp.ehlo(smtpserver)  # 服务器返回结果确认
    smtp.login(user, password)  # 登录
    print('开始发送邮件')
    smtp.sendmail(sender, receive, msg.as_string())
    smtp.quit()
    print('发送完成')
