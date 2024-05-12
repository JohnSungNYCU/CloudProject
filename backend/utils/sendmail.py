# -*- coding: utf-8 -*-
# author: timor

import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from omsBackend.settings import MAIL_ACOUNT

# 設置服務器名稱、用戶名、密碼以及郵件後綴
mail_host = MAIL_ACOUNT["mail_host"]
mail_user = MAIL_ACOUNT["mail_user"]
mail_pass = MAIL_ACOUNT["mail_pass"]
mail_postfix = MAIL_ACOUNT["mail_postfix"]


# 發送郵件函數
def send_mail(to_list, cc_list, sub, content):
    me = mail_user + "<" + mail_user + "@" + mail_postfix + ">"
    # f = open(context)
    # msg = MIMEText(f.read(),_charset="utf-8")
    # f.close()
    # msg = MIMEText(context)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = to_list
    msg['Cc'] = cc_list
    list = msg['Cc'].split(',')
    list.append(msg['To'])
    context = MIMEText(content, _subtype='html', _charset='utf-8')  # 解決亂碼
    msg.attach(context)
    try:
        send_smtp = smtplib.SMTP()
        send_smtp.connect(mail_host, 587)
        send_smtp.starttls()
        send_smtp.login(mail_user, mail_pass)

        send_smtp.sendmail(me, list, msg.as_string())
        send_smtp.close()
        return {"code": 'success', "msg": "通知郵件發送成功"}
    except Exception as e:
        print(e)
        return {"code": 'error', "msg": "通知郵件發送失敗"}


if __name__ == '__main__':
    to_list = sys.argv[1]  # 收件人列表   '111@126.com'
    cc_list = sys.argv[2]  # 抄送人列表   '111@126.com;222@126.com;'
    sub = sys.argv[3]
    context = sys.argv[4]
    if send_mail(to_list, cc_list, sub, context):
        print({"code": 'success', "msg": "通知郵件發送成功"})
    else:
        print({"code": 'error', "msg": "通知郵件發送失敗"})