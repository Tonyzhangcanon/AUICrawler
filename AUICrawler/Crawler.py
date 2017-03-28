# -*- coding:utf-8 -*-
import threading
from module.CrawledApp import App
from module.PlanInfo import Plan
from runner import runner
from script import Setting
from script import Saver
import getopt, sys
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

plan = Plan()
app = App(plan)

opts, args = getopt.getopt(sys.argv[1:], "auicsjkld:t:r:")
for op, value in opts:
    if op == "-a":
        Setting.CrawlModel = 'Activity'
    elif op == "-u":
        Setting.UnInstallApk = True
        Setting.InstallApk = True
    elif op == "-i":
        Setting.RunInitNodes = True
    elif op == '-c':
        Setting.RunInitCase = True
    elif op == '-s':
        Setting.SaveScreen = True
    elif op == '-j':
        Setting.SaveJumpOutScreen = True
    elif op == '-k':
        Setting.KeepRun = True
    elif op == '-l':
        Setting.Login = True
    elif op == '-d':
        device_list = []
        if ',' in value:
            device_list = value.split(',')
        else:
            device_list.append(value)
        plan.update_device_list(device_list)
    elif op == '-t':
        Setting.TimeModel = 'Limit'
        Setting.LimitTime = int(value)
    elif op == '-r':
        Setting.CoverageLevel = float(value)
        if Setting.CrawlModel == 'Normal':
            Setting.CrawlModel = 'Random'

if len(plan.deviceList) == 0:
    plan.get_device_list()

threads = []

for device in plan.deviceList:
    thread = threading.Thread(target=runner.run_test, args=(plan, app, device))
    threads.append(thread)
for th in threads:
    th.start()
for th in threads:
    th.join()

plan.endTime = datetime.datetime.now()
Saver.save_crawl_result(plan, app)
