# -*- coding:utf-8 -*-

import datetime
import os
import sys
import types
import HtmlMaker
import MailSender


reload(sys)
sys.setdefaultencoding('utf-8')

log_tag = os.path.basename(os.getcwd())


def save_crawler_log(log_path, log):
    log_file = open(log_path + '/CrawlerLog.txt', 'a')
    if type(log) is types.StringType:
        if "Step" in log:
            log_str = log_tag + " : " + str(datetime.datetime.now()) + "  " + log
        else:
            log_str = log_tag + " : " + str(datetime.datetime.now()) + "       - " + log
    else:
        log_str = log_tag + " : " + str(datetime.datetime.now()) + "       - " + str(log)
    print log_str
    log_file.write(log_str + '\n')
    del log_str, log_path, log
    log_file.close()


def save_crawler_log_both(plan_log_path, device_log_path, log):
    save_crawler_log(plan_log_path, log)
    save_crawler_log(device_log_path, log)


def save_logcat(plan, app, device, finish):
    save_crawler_log(plan.logPath, "Step : save device log : " + device.id)
    if not os.path.exists(os.getcwd()):
        os.makedirs(os.getcwd())
    command = 'adb -s ' + device.id + ' logcat -d >> ' + device.logPath + '/logcat.txt'
    os.system(command)
    if not finish:
        get_log_commend = 'adb -s ' + device.id + ' logcat -d'
        log = os.popen(get_log_commend).readlines()
        for line in log:
            if line.find('System.err') != -1:
                device.update_crawl_statue('HasCrashed')
                device.failedTime += 1
                break
            elif line.find('ANR') != -1:
                device.update_crawl_statue('HasANR')
                device.failedTime += 1
                break
            del line
        HtmlMaker.mack_failed_result_html(plan, app)
        MailSender.send_failed_mail(plan, app, device)
        del get_log_commend, log
    del plan, device, finish, command


def save_crawl_result(plan, app):
    save_crawler_log(plan.logPath, "Step : Save crawl results . ")
    resultHtml = HtmlMaker.mack_crawl_result_html(plan, app)
    result_file = open(plan.logPath + '/Result.html', 'w')
    result_file.write(resultHtml)
    result_file.close()
