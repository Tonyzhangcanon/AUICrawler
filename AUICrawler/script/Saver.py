# -*- coding:utf-8 -*-

import datetime
import os
import sys
import types
import HtmlMaker

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
    log_file.close()
    del log_str, log_path, log, log_file


def save_crawler_log_both(plan_log_path, device_log_path, log):
    save_crawler_log(plan_log_path, log)
    save_crawler_log(device_log_path, log)
    del plan_log_path, device_log_path, log


def save_logcat(plan, device):
    save_crawler_log(plan.logPath, "Step : save device log : " + device.id)
    if not os.path.exists(os.getcwd()):
        os.makedirs(os.getcwd())
    command = 'adb -s ' + device.id + ' logcat -d >> ' + device.logPath + '/logcat.txt'
    os.system(command)
    del plan, device, command


def save_error_logcat(plan, device):
    save_crawler_log(plan.logPath, "Step : save device log : " + device.id)
    device.failedTime += 1
    command1 = 'adb -s ' + device.id + ' logcat -d >> ' + device.logPath + '/errorLog' + str(device.failedTime) + '.txt'
    command2 = 'adb -s ' + device.id + ' logcat -d >> ' + device.logPath + '/logcat.txt'
    os.system(command1)
    os.system(command2)
    get_log_command = 'adb -s ' + device.id + ' logcat -d'
    log = os.popen(get_log_command).readlines()
    update_statue_finish = False
    for line in log:
        # if line.find('NullPointerException') != -1:
        #     device.update_crawl_statue('NullPointExc')
        #     update_statue_finish = True
        #     break
        if line.find('shortMsg') != -1:
            device.update_crawl_statue('HasCrashed')
            update_statue_finish = True
            break
        elif line.find('ANR ') != -1:
            device.update_crawl_statue('HasANR')
            update_statue_finish = True
            break
        elif line.find('Fatal') != -1:
            device.update_crawl_status('ForceClosed')
            update_statue_finish = True
            break
        del line
    if not update_statue_finish:
        device.update_crawl_statue('UnknownExc')
    del get_log_command, log, plan, device, command1, command2, update_statue_finish


def save_crawl_result(plan, app):
    save_crawler_log(plan.logPath, "Step : Save crawl results . ")
    resultHtml = HtmlMaker.mack_crawl_result_html(plan, app)
    result_file = open(plan.logPath + '/Result.html', 'w')
    result_file.write(resultHtml)
    result_file.close()
    del plan, app, resultHtml, result_file
