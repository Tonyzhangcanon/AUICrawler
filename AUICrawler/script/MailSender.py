# -*- coding: utf-8 -*-

from __future__ import print_function

import mimetypes
import smtplib
from email.mime.text import MIMEText
from email import MIMEMultipart
from email import MIMEBase
from email import Encoders
from email import Utils
from config import Setting
import os.path


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


def send_failed_mail(plan, app, device):
    file_name = device.logPath + '/' + 'logcat.txt'
    me = "AUICrawler" + "<" + Setting.Mail_User + ">"
    main_msg = MIMEMultipart.MIMEMultipart()
    text = "Has " + device.crawlStatue + " in " + str(device.id) + ' when crawl ' + str(app.appName) + ', please check the logcat file in attachment . \n\n'
    msg = MIMEText(text + plan.resultHtml, _subtype='html', _charset='utf=8')
    main_msg.attach(msg)

    data = open(file_name, 'rb')
    ctype, encoding = mimetypes.guess_type(file_name)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    file_msg = MIMEBase.MIMEBase(maintype, subtype)
    file_msg.set_payload(data.read())
    data.close()
    Encoders.encode_base64(file_msg)  # 把附件编码

    basename = os.path.basename("logcat.txt")
    file_msg.add_header('Content-Disposition', 'attachment', filename=basename)  # 修改邮件头
    main_msg.attach(file_msg)

    # 设置根容器属性
    main_msg['From'] = me
    main_msg['To'] = ";".join(Setting.Mail_To_List)
    main_msg['Subject'] = "自动遍历测试发现异常啦！！！快看我！！！"
    main_msg['Date'] = Utils.formatdate()

    try:
        s = smtplib.SMTP()
        s.connect(Setting.SMTP_HOST)
        s.login(Setting.Mail_User, Setting.Mail_Pass)
        s.sendmail(me, Setting.Mail_To_List, main_msg.as_string())
        s.close()
        return True
    except Exception, e:
        print(str(e))
        return False
