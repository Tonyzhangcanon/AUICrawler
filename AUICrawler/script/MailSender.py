# -*- coding: utf-8 -*-

from __future__ import print_function
import smtplib
from email.mime.text import MIMEText
from config import Setting


def send_mail(plan):
    me = "AUICrawler" + "<" + Setting.Mail_User + ">"
    msg = MIMEText(plan.resultHtml, _subtype='html', _charset='gb2312')
    msg['Subject'] = "自动遍历测试报告 - " + str(plan.runCaseTime)
    msg['From'] = me
    msg['To'] = ";".join(Setting.Mail_To_List)
    try:
        s = smtplib.SMTP()
        s.connect(Setting.SMTP_HOST)
        s.login(Setting.Mail_User, Setting.Mail_Pass)
        s.sendmail(me, Setting.Mail_To_List, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print(str(e))
        return False

