# -*- coding:utf-8 -*-
import os
import datetime
from config import Setting
from DeviceInfo import Device
from script import Saver
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Plan:
    def __init__(self):
        self.coverageLevel = Setting.CoverageLevel
        self.runCaseTime = datetime.datetime.now()
        self.logPath = self.create_this_time_folder()
        self.deviceList = []
        self.deviceNum = str(len(self.deviceList))
        self.passedDevice = 0
        self.failedDevice = 0
        self.endTime = None
        self.resultHtml = '<a>测试结果</a>'

    # change the node info ,because the same type nodes has difference bounds.
    # the same type nodes need crawl once only

    def create_this_time_folder(self):
        path = os.getcwd() + '/result/' + self.runCaseTime.strftime('%Y%m%d%H%M%S')
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
                if Setting.Login:
                    index = device_list.index(device)
                    device.update_device_account(Setting.AccountList[index])
                del device_id, device
            del line
        Saver.save_crawler_log(self.logPath, device_list)
        self.deviceList = device_list
        self.deviceNum = str(len(device_list))
        del device_list, string, outLine

    def update_device_list(self, id_list):
        device_list = []
        for device_id in id_list:
            device = Device(self, device_id)
            device_list.append(device)
            index = device_list.index(device)
            device.update_device_account(Setting.AccountList[index])
            del device_id, device, index
        self.deviceList = device_list
        self.deviceNum = str(len(device_list))
        del device_list



