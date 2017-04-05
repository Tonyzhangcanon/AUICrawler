# -*- coding:utf-8 -*-

import os
import re
import datetime
from script import Saver
from config import Setting
import PageInfo
from PIL import Image
import gc


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
        self.beginCrawlTime = datetime.datetime.now()
        self.endCrawlTime = datetime.datetime.now()
        self.unCrawledNodes = []
        self.hasCrawledNodes = []
        self.hasCrawlPage = []
        self.hasCrawledActivities = []
        self.saveScreenNum = 0
        self.jump_out_time = 0
        self.crawlStatue = "Inited"
        self.failedTime = 0
        self.page_now = PageInfo.Page()

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
        x = ''
        y = ''
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
        except Exception, e:
            print (e)
            command = 'adb -s ' + self.id + ' shell cat /system/build.prop | findstr "product" '
            result = os.popen(command).readlines()
            for line in result:
                key = 'ro.product.model='
                if key in line:
                    device_name = line[line.find(key) + len(key):-2]
                    break
            Saver.save_crawler_log(self.logPath, "device name : " + device_name)
        del command, result, key
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
        del command
        return result

    def update_crawl_statue(self, statue):
        Saver.save_crawler_log(self.logPath, "Step : Update crawl statue from " + self.crawlStatue + ' to ' + statue)
        self.crawlStatue = statue
        del statue

    def update_device_account(self, account):
        Saver.save_crawler_log(self.logPath, "Step : Update account : " + str(account))
        self.accountInfo = account
        del account

    def update_crawled_nodes(self, node_info):
        if node_info not in self.hasCrawledNodes:
            self.hasCrawledNodes.append(node_info)
        del node_info

    def update_uncrawled_nodes(self, page):
        if page.clickableNodesNum != 0:
            for node in page.clickableNodes:
                if node.nodeInfo not in self.unCrawledNodes:
                    self.unCrawledNodes.append(node.nodeInfo)
                del node
        if page.longClickableNodesNum != 0:
            for node in page.longClickableNodes:
                if node.nodeInfo not in self.unCrawledNodes:
                    self.unCrawledNodes.append(node.nodeInfo)
                del node
        if page.editTextsNum != 0:
            for node in page.editTexts:
                if node.nodeInfo not in self.unCrawledNodes:
                    self.unCrawledNodes.append(node.nodeInfo)
                del node

    def update_crawled_activity(self, activity):
        if activity not in self.hasCrawledActivities:
            self.hasCrawledActivities.append(activity)
        del activity

    def delete_uncrawled_nodes(self, node_info):
        if node_info in self.unCrawledNodes:
            self.unCrawledNodes.remove(node_info)
        del node_info

    def is_in_uncrawled_nodes(self, node_info):
        if node_info in self.unCrawledNodes:
            del node_info
            return True
        else:
            del node_info
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
        self.beginCrawlTime = datetime.datetime.now()

    def save_screen(self, node, model):
        if Setting.SaveScreen:
            try:
                Saver.save_crawler_log(self.logPath, "Step : save screenshot ")
                get_screenshot_command = 'adb -s ' + self.id + ' shell /system/bin/screencap -p /sdcard/screenshot.png'
                activity = node.currentActivity
                resource_id = node.resource_id
                resource_id = resource_id[resource_id.find('/') + 1:]
                location = node.location
                if model:
                    local_png = self.screenshotPath + '/' + str(self.saveScreenNum) + '-' + str(
                        activity) + '-' + str(
                        resource_id) + '-' + str(location[0]) + '-' + str(location[1]) + '.png'
                else:
                    local_png = self.screenshotPath + '/' + str(self.saveScreenNum) + '-' + 'unCrawl' + '-' + str(
                        activity) + '-' + str(
                        resource_id) + '-' + str(location[0]) + '-' + str(location[1]) + '.png'
                pull_screenshot_command = 'adb -s ' + self.id + ' pull /sdcard/screenshot.png ' + local_png
                os.system(get_screenshot_command)
                os.system(pull_screenshot_command)
                self.saveScreenNum += 1
                i = Image.open(local_png)
                for w in range(3):
                    bounds = node.bounds
                    for x in range(bounds[0] + w, bounds[2] - w):
                        i.putpixel((x, bounds[1] + 1 + w), (255, 0, 0))
                        i.putpixel((x, bounds[3] - 1 - w), (255, 0, 0))
                    for y in range(bounds[1] + w, bounds[3] - w):
                        i.putpixel((bounds[0] + 1 + w, y), (255, 0, 0))
                        i.putpixel((bounds[2] - 1 - w, y), (255, 0, 0))
                i.save(local_png)
                del get_screenshot_command, activity, resource_id, location, pull_screenshot_command, local_png, i
                del node, model, bounds
                gc.collect()
            except Exception, e:
                print (str(e))
                Saver.save_crawler_log(self.logPath, "save screen error")

    def save_screen_jump_out(self, package, activity):
        if Setting.SaveJumpOutScreen:
            try:
                Saver.save_crawler_log(self.logPath, "Step : jump out . save screenshot ")
                get_screenshot_command = 'adb -s ' + self.id + ' shell /system/bin/screencap -p /sdcard/screenshot.png'
                local_png = self.screenshotPath + '/' + str(self.saveScreenNum) + '-' + str(package) + '-' + str(
                    activity) + '-Jump' + str(self.jump_out_time) + '.png'
                pull_screenshot_command = 'adb -s ' + self.id + ' pull /sdcard/screenshot.png ' + local_png
                os.system(get_screenshot_command)
                os.system(pull_screenshot_command)
                self.saveScreenNum += 1
                self.jump_out_time += 1
                del get_screenshot_command, local_png, pull_screenshot_command
                gc.collect()
            except Exception, e:
                print (str(e))
                Saver.save_crawler_log(self, "save screen error")




