# -*- coding:utf-8 -*-
import datetime
import getopt
import sys
import threading

from config import Setting
from module.CrawledApp import App
from module.PlanInfo import Plan
from runner import runner
from script import Saver
from script import MailSender

plan = Plan()

opts, args = getopt.getopt(sys.argv[1:], "aicsjklud:t:r:p:")
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
    elif op == '-p':
        if ',' in value:
            apk_list = []
            apk_list = value.split(',')
            Setting.ApkPath = apk_list[0]
            Setting.TestApkPath = apk_list[1]
        else:
            Setting.ApkPath = value

app = App(plan)

if len(plan.deviceList) == 0:
    plan.get_device_list(app)
elif Setting.Login:
    device_list = plan.deviceList
    for device in device_list:
        index = device_list.index(device)
        accountList = Setting.AccountList[app.packageName]
        device.update_device_account(accountList[index])
        del device, index, accountList

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
MailSender.send_mail(plan)

