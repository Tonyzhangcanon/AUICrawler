# -*- coding:utf-8 -*-
import threading
from AUICrawler.module.CrawledApp import App
from AUICrawler.module.PlanInfo import Plan
from AUICrawler.runner import easyrunner
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

plan = Plan()
app = App(plan)
threads = []

for device in plan.deviceList:
    thread = threading.Thread(target=easyrunner.run_test, args=(plan, app, device))
    threads.append(thread)
for th in threads:
    th.start()
for th in threads:
    th.join()
