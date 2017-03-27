# -*- coding:utf-8 -*-

import os
import re
import time
from script import Saver
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Device:
    def __init__(self, plan, device_id):
        Saver.save_crawler_log(plan.logPath, "Step : Init device : " + device_id)
        self.id = device_id
        Saver.save_crawler_log(plan.logPath, "id : " + self.id)
        self.logPath = self.create_device_folder(plan)
        self.name = self.get_device_name()
        self.model = self.get_device_model()
        self.version = self.get_device_sys_version()
        self.accountInfo = []
        self.screenResolution = self.get_screen_resolution()
        self.screenshotPath = self.create_screenshot_folder()
        self.beginCrawlTime = int(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
        self.unCrawledNodes = []
        self.hasCrawledNodes = []
        self.hasCrawlPage = []
        self.hasCrawledActivities = []
        self.crawlStatue = "Inited"

    def create_device_folder(self, plan):
        path = plan.logPath + '/' + self.id
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def get_screen_resolution(self):
        Saver.save_crawler_log(self.logPath, "Step : get screen resolution")
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
        Saver.save_crawler_log(self.logPath, resolution)
        return resolution

    def create_screenshot_folder(self):
        path = self.logPath + '/Screenshot'
        Saver.save_crawler_log(self.logPath, "Step : creat screenshot folder")
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def get_device_name(self):
        # linux:
        # adb shell cat /system/build.prop | grep "product"
        # windows
        # adb -s 84B5T15A10010101 shell cat /system/build.prop | findstr "product"
        device_name = ''
        try:
            command = 'adb -s ' + self.id + ' shell cat /system/build.prop | grep "product" '
            result = os.popen(command).readlines()
            for line in result:
                key = 'ro.product.model='
                if key in line:
                    device_name = line[line.find(key) + len(key):-2]
                    break
            Saver.save_crawler_log(self.logPath, "device name : " + device_name)
        except:
            command = 'adb -s ' + self.id + ' shell cat /system/build.prop | findstr "product" '
            result = os.popen(command).readlines()
            for line in result:
                key = 'ro.product.model='
                if key in line:
                    device_name = line[line.find(key) + len(key):-2]
                    break
            Saver.save_crawler_log(self.logPath, "device name : " + device_name)
        return device_name

    def get_device_model(self):
        command = 'adb -s ' + self.id + ' shell getprop ro.product.model'
        model = os.popen(command).read()
        Saver.save_crawler_log(self.logPath, "device model : " + model)
        return model

    def get_device_sys_version(self):
        command = 'adb -s ' + self.id + ' shell getprop ro.build.version.release'
        result = os.popen(command).read()
        Saver.save_crawler_log(self.logPath, "sys version : " + result)
        version = int(result.replace('.', ''))
        return version

    def update_crawl_statue(self, statue):
        Saver.save_crawler_log(self.logPath, "Step : Update crawl statue from " + self.crawlStatue + ' to ' + statue)
        self.crawlStatue = statue

    def update_device_account(self, account):
        Saver.save_crawler_log(self.logPath, "Step : Update account : " + str(account))
        self.accountInfo = account

    def update_crawled_nodes(self, node_info):
        if node_info not in self.hasCrawledNodes:
            self.hasCrawledNodes.append(node_info)

    def update_uncrawled_nodes(self, node_info):
        if node_info not in self.unCrawledNodes:
            self.unCrawledNodes.append(node_info)

    def update_crawled_activity(self, activity):
        if activity not in self.hasCrawledActivities:
            self.hasCrawledActivities.append(activity)

    def delete_uncrawled_nodes(self, node_info):
        if node_info in self.unCrawledNodes:
            self.unCrawledNodes.remove(node_info)

    def is_in_uncrawled_nodes(self, node_info):
        if node_info in self.unCrawledNodes:
            return True
        else:
            return False

    def is_in_hascrawled_nodes(self, node_info):
        if node_info in self.hasCrawledNodes:
            return True
        else:
            return False

    def update_crawl_page(self, nodes_info_list):
        if nodes_info_list not in self.hasCrawlPage:
            self.hasCrawlPage.append(nodes_info_list)

    def update_begin_crawl_time(self):
        self.beginCrawlTime = int(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
