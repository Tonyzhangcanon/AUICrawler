# -*- coding:utf-8 -*-
import os
import time
from AUICrawler.script import Setting
from AUICrawler.module.DeviceInfo import Device
from AUICrawler.script import Saver
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Plan:
    def __init__(self):
        self.product = Setting.AppProduct
        self.coverageLevel = Setting.CoverageLevel
        self.runCaseTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.logPath = self.create_this_time_folder()
        self.deviceList = self.get_device_list()

    # change the node info ,because the same type nodes has difference bounds.
    # the same type nodes need crawl once only

    def create_this_time_folder(self):
        path = os.getcwd() + '/result/' + self.runCaseTime
        print path
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def get_device_list(self):
        device_list = []
        string = '	'
        outLine = os.popen('adb devices').readlines()
        for line in outLine:
            if string in line:
                device_id = line[0:line.index(string)]
                device = Device(self, device_id)
                device_list.append(device)
                index = device_list.index(device)
                device.update_device_account(Setting.AccountList[index])
        Saver.save_crawler_log(self.logPath, device_list)
        return device_list



