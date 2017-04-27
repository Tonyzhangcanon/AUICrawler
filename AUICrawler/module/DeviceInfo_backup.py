# -*- coding:utf-8 -*-

import os
import re
import datetime
from script import Saver
import PageInfo
import matplotlib
matplotlib.use('Agg')
import pylab as pl
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
        return result

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
        self.beginCrawlTime = datetime.datetime.now()

    def draw_screen_shot(self, node, local_png):
        bounds = node.bounds
        image = pl.array(Image.open(local_png))
        fig = pl.figure(0, figsize=(float(self.screenResolution[0]) / 100, float(self.screenResolution[1]) / 100),
                  dpi=100)
        pl.imshow(image)
        x = [bounds[0], bounds[0], bounds[2], bounds[2], bounds[0]]
        y = [bounds[1], bounds[3], bounds[3], bounds[1], bounds[1]]
        pl.axis('off')
        pl.axis('scaled')
        pl.axis([0, int(self.screenResolution[0]), int(self.screenResolution[1]), 0])
        pl.plot(x[:5], y[:5], 'r', linewidth=2)
        pl.savefig(local_png)
        pl.clf()
        pl.cla()
        pl.close(fig)
        im = Image.open(local_png)
        box = (float(self.screenResolution[0]) / 8, float(self.screenResolution[1]) / 9,
               float(self.screenResolution[0]) * 65 / 72, float(self.screenResolution[1]) * 8 / 9)
        region = im.crop(box)
        region.save(local_png)
        del bounds, x[:], y[:], node, local_png, image, im, box, region, fig
        gc.collect()

    def draw_screen(self, image, box, line_width, color_rgb):
        i = Image.open(image)
        for w in range(line_width):
            for x in range(box[0] + w, box[2] - w):
                i.putpixel((x, box[1]+1+w), color_rgb)
                i.putpixel((x, box[3]-1-w), color_rgb)
            for y in range(box[1] + w, box[3] - w):
                i.putpixel((box[0]+1+w, y), color_rgb)
                i.putpixel((box[2]-1-w, y), color_rgb)
        i.save(image)
        del i
        gc.collect()



