# -*- coding:utf-8 -*-

import os
import time
import types
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

log_tag = os.path.basename(os.getcwd())


def save_crawler_log(log_path, log):
    log_file = open(log_path + '/CrawlerLog.txt', 'a')
    if type(log) is types.StringType:
        if "Step" in log:
            log_str = log_tag + " : " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "  " + log
        else:
            log_str = log_tag + " : " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "       - " + log
    else:
        log_str = log_tag + " : " + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + "       - " + str(log)
    print log_str
    log_file.write(log_str + '\n')
    log_file.close()


def save_crawler_log_both(plan_log_path, device_log_path, log):
    save_crawler_log(plan_log_path, log)
    save_crawler_log(device_log_path, log)
