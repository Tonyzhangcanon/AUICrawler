# -*- coding:utf-8 -*-
import os
import time
from AUICrawler.script import Setting
from AUICrawler.module.DeviceInfo import Device
from AUICrawler.script import SaveLog
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Plan:
    def __init__(self):
        self.product = Setting.AppProduct
        self.coverageLevel = Setting.CoverageLevel
        self.runCaseTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.unCrawledNodes = []
        self.hasCrawledNodes = []
        self.hasCrawlPage = []
        self.hasCrawledActivities = []
        self.logPath = self.create_this_time_folder()
        self.deviceList = self.get_device_list()

    # change the node info ,because the same type nodes has difference bounds.
    # the same type nodes need crawl once only
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
                last_string = line[0:line.index(string)]
                device = Device(self, last_string)
                device_list.append(device)
        SaveLog.save_crawler_log(self.logPath, device_list)
        return device_list
