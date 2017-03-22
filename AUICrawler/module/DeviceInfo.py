# -*- coding:utf-8 -*-

import os
import re
from AUICrawler.script import SaveLog
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Device:
    def __init__(self, plan, device_id):
        SaveLog.save_crawler_log(plan.logPath, "Step : Init device : " + device_id)
        self.id = device_id
        self.logPath = self.create_device_folder(plan)
        self.name = self.get_device_name()
        self.model = self.get_device_model()
        self.version = self.get_device_sys_version()
        self.accountInfo = []
        self.screenResolution = self.get_screen_resolution()
        self.screenshotPath = self.create_screenshot_folder()
        self.crawlStatue = "Inited"

    def create_device_folder(self, plan):
        path = plan.logPath + '/' + self.id
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def get_screen_resolution(self):
        SaveLog.save_crawler_log(self.logPath, "Step : get screen resolution")
        command = 'adb -s ' + self.id + ' shell wm size'
        resolution = []
        result = os.popen(command).readlines()
        for line in result:
            if 'Physical size: ' in line:
                r = re.findall(r'\d+', line)
                x = r[0]
                y = r[1]
        resolution.append(x)
        resolution.append(y)
        SaveLog.save_crawler_log(self.logPath, resolution)
        return resolution

    def create_screenshot_folder(self):
        path = self.logPath + '/Screenshot'
        SaveLog.save_crawler_log(self.logPath, "Step : creat screenshot folder")
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def get_device_name(self):
        # linux:
        # adb shell cat /system/build.prop | grep "product"
        # windows
        # adb -s 84B5T15A10010101 shell cat /system/build.prop | findstr "product"
        command = 'adb -s ' + self.id + ' shell cat /system/build.prop | grep "product" '
        result = os.popen(command).readlines()
        for line in result:
            key = 'ro.product.model='
            if key in line:
                device_name = line[line.find(key) + len(key):-2]
                break
        SaveLog.save_crawler_log(self.logPath, device_name)
        return device_name

    def get_device_model(self):
        command = 'adb -s ' + self.id + ' shell getprop ro.product.model'
        model = os.popen(command).read()
        SaveLog.save_crawler_log(self.logPath, model)
        return model

    def get_device_sys_version(self):
        command = 'adb -s ' + self.id + ' shell getprop ro.build.version.release'
        result = os.popen(command).read()
        SaveLog.save_crawler_log(self.logPath, result)
        version = int(result.replace('.', ''))
        return version

    def update_crawl_statue(self, statue):
        SaveLog.save_crawler_log(self.logPath, "Step : Update crawl statue from " + self.crawlStatue + ' to ' + statue)
        self.crawlStatue = statue

    def update_device_account(self, account):
        SaveLog.save_crawler_log(self.logPath, "Step : Update account : " + str(account))
        self.accountInfo = account
