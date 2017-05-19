# -*- coding: utf-8 -*-

from __future__ import print_function

import mimetypes
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import MIMEMultipart
from email import MIMEBase
from email import Encoders
from email import Utils
from config import Setting
import os.path


def send_mail(plan):
    me = "AUICrawler" + "<" + Setting.Mail_User + ">"
    msg = MIMEText(plan.resultHtml, _subtype='html', _charset='utf-8')
    msg['Subject'] = u"自动遍历测试报告 - " + str(plan.runCaseTime)
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


def send_failed_mail_first(plan, app, device):
    file_name = device.logPath + '/' + 'errorLog' + str(device.failedTime) +'.txt'
    me = "AUICrawler" + "<" + Setting.Mail_User + ">"
    main_msg = MIMEMultipart.MIMEMultipart()
    text = device.crawlStatue + " in " + str(device.id) + ' when crawl ' + str(
        app.appName) + ' , please check the logcat file in attachment . \n' + \
        ' I will reCrawl this node again for check is necessary ' + device.crawlStatue + ' or not . \n\n'
    msg = MIMEText(text + plan.resultHtml, _subtype='html', _charset='utf-8')
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

    basename = os.path.basename("log.txt")
    file_msg.add_header('Content-Disposition', 'attachment', filename=basename)  # 修改邮件头
    main_msg.attach(file_msg)

    # 设置根容器属性
    main_msg['From'] = me
    main_msg['To'] = ";".join(Setting.Mail_To_List)
    main_msg['Subject'] = u"自动遍历测试发现异常啦！！！快看我！！！"
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


def send_failed_mail_necessary(plan, app, device, node):
    file_name = device.logPath + '/' + 'errorLog' + str(device.failedTime) + '.txt'
    me = "AUICrawler" + "<" + Setting.Mail_User + ">"
    main_msg = MIMEMultipart.MIMEMultipart()
    text = device.crawlStatue + " again in " + str(device.id) + ' when crawl ' + str(
        app.appName) + ' , please check the screenshot and the logcat file in attachment . \n' + \
        ' Crawl this node is necessary to make app ' + device.crawlStatue + '. \n\n'
    msg = MIMEText(text + plan.resultHtml, _subtype='html', _charset='utf-8')
    main_msg.attach(msg)
    resource_id = node.resource_id
    resource_id = resource_id[resource_id.find('/') + 1:]
    screen = device.screenshotPath + '/' + str(device.saveScreenNum-1) + '-' + str(
                    node.currentActivity) + '-' + str(
                    resource_id) + '-' + str(node.location[0]) + '-' + str(node.location[1]) + '.png'
    if os.path.exists(screen):
        fp = open(screen, 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-Disposition', 'attachment', filename=os.path.basename("screenShot"))
        main_msg.attach(msgImage)
    data = open(file_name, 'rb')
    ctype, encoding = mimetypes.guess_type(file_name)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    file_msg = MIMEBase.MIMEBase(maintype, subtype)
    file_msg.set_payload(data.read())
    data.close()
    Encoders.encode_base64(file_msg)  # 把附件编码
    file_msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename("log.txt"))  # 修改邮件头
    main_msg.attach(file_msg)

    # 设置根容器属性
    main_msg['From'] = me
    main_msg['To'] = ";".join(Setting.Mail_To_List)
    main_msg['Subject'] = u"自动遍历测试 - 复现异常啦，此处应该有掌声！！！！"
    main_msg['Date'] = Utils.formatdate()


def send_failed_mail_un_necessary(plan, app, device):
    me = "AUICrawler" + "<" + Setting.Mail_User + ">"
    main_msg = MIMEMultipart.MIMEMultipart()
    text = "App don't " + device.crawlStatue + " after reCrawl on " + str(device.id) + ' when crawl ' + str(
        app.appName) + ' , check the log file in last mail , please .\n\n'
    msg = MIMEText(text + plan.resultHtml, _subtype='html', _charset='utf=8')
    main_msg.attach(msg)

    # 设置根容器属性
    main_msg['From'] = me
    main_msg['To'] = ";".join(Setting.Mail_To_List)
    main_msg['Subject'] = u"自动遍历测试 - 异常未复现"
    main_msg['Date'] = Utils.formatdate()