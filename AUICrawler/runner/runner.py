# -*- coding:utf-8 -*-
import os
import datetime
import time
import sys
from script import Saver
from module import PageInfo
from config import Setting
from controller import appController
from controller import pageController
from controller import nodeController

reload(sys)
sys.setdefaultencoding('utf-8')

curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)


def crawl_clickable_nodes(plan, app, device, page_before_run, page_now, init):
    for node in nodeController.get_random_nodes(page_before_run.clickableNodes):
        # if crash and not keep run , break from deep run .page_need_crawled will be None
        if page_now is None:
            Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
            del plan, app, device, page_before_run, init
            break
        # sometimes the need tap node is not shown after one deep run
        if not nodeController.recover_node_shown(plan, app, device, page_now, page_before_run, node):
            del node
            continue
        device.save_screen(node, True)
        appController.tap_node(device, node)
        device.update_crawled_activity(node.currentActivity)
        device.update_crawled_nodes(node.nodeInfo)
        device.delete_uncrawled_nodes(node.nodeInfo)
        # if jump out the test app, try to go back & return the final page
        page_after_operation = pageController.check_page_after_operation(plan, app, device, page_before_run, node)
        if page_after_operation is None:
            Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
            page_now = page_after_operation
            break
        # compare two pages before & after click .
        # update the after page . leave the new clickable/scrollable/longclickable/edittext nodes only.
        page_now = pageController.get_need_crawl_page(plan, app, device, page_before_run, page_after_operation)
        if pageController.page_is_crawlable(app, device, page_now):
            page_now.add_last_page(page_before_run)
            page_now.add_entry(node)
            # deep run
            if init:
                page_now = crawl_init_nodes(plan, app, device, page_now)
            else:
                page_now = crawl_main_nodes(plan, app, device, page_now)
        else:
            page_now = page_after_operation
        # if page no crawlable nodes , back to last Page, until has crawlable nodes, if back time >3, break
        page_now = pageController.recover_page_to_crawlable(plan, app, device, page_now)
        del node
    return page_now


def crawl_longclickable_nodes(plan, app, device, page_before_run, page_now, init):
    for node in nodeController.get_random_nodes(page_before_run.longClickableNodes):
        # if crash and not keep run , break from deep run .page_need_crawled will be None
        if page_now is None:
            Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
            break
        # sometimes the need tap node is not shown after one deep run
        if not nodeController.recover_node_shown(plan, app, device, page_now, page_before_run, node):
            continue
        device.save_screen(node, True)
        appController.long_click_node(device, node)
        device.update_crawled_activity(node.currentActivity)
        device.update_crawled_nodes(node.nodeInfo)
        device.delete_uncrawled_nodes(node.nodeInfo)
        # if jump out the test app, try to go back & return the final page
        page_after_operation = pageController.check_page_after_operation(plan, app, device, page_before_run, node)
        if page_after_operation is None:
            Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
            page_now = page_after_operation
            break
        # compare two pages before & after click .
        # update the after page . leave the new clickable/scrollable/longclickable/edittext nodes only.
        page_now = pageController.get_need_crawl_page(plan, app, device, page_before_run, page_after_operation)
        if pageController.page_is_crawlable(app, device, page_now):
            page_now.add_last_page(page_before_run)
            page_now.add_entry(node)
            # deep run
            if init:
                page_now = crawl_init_nodes(plan, app, device, page_now)
            else:
                page_now = crawl_main_nodes(plan, app, device, page_now)
        else:
            page_now = page_after_operation
        # if page no crawlable nodes , back to last Page, until has crawlable nodes, if back time >3, break
        page_now = pageController.recover_page_to_crawlable(plan, app, device, page_now)
        del node
    del plan, app, device, page_before_run, init
    return page_now


def crawl_edittext(plan, app, device, page_before_run, page_now, init):
    for node in nodeController.get_random_nodes(page_before_run.editTexts):
        # if crash and not keep run , break from deep run .page_need_crawled will be None
        if page_now is None:
            Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
            break
        # sometimes the need tap node is not shown after one deep run
        if not nodeController.recover_node_shown(plan, app, device, page_now, page_before_run, node):
            continue
        device.save_screen(node, True)
        text = appController.get_random_text(8)
        appController.type_text(device, node, text)
        device.update_crawled_activity(node.currentActivity)
        device.update_crawled_nodes(node.nodeInfo)
        device.delete_uncrawled_nodes(node.nodeInfo)
        # if jump out the test app, try to go back & return the final page
        page_after_operation = pageController.check_page_after_operation(plan, app, device, page_before_run, node)
        if page_after_operation is None:
            Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
            page_now = page_after_operation
            break
        # compare two pages before & after click .
        # update the after page . leave the new clickable/scrollable/longclickable/edittext nodes only.
        page_now = pageController.get_need_crawl_page(plan, app, device, page_before_run, page_after_operation)
        if pageController.page_is_crawlable(app, device, page_now):
            page_now.add_last_page(page_before_run)
            page_now.add_entry(node)
            # deep run
            if init:
                page_now = crawl_init_nodes(plan, app, device, page_now)
            else:
                page_now = crawl_main_nodes(plan, app, device, page_now)
        else:
            page_now = page_after_operation
        # if page no crawlable nodes , back to last Page, until has crawlable nodes, if back time >3, break
        page_now = pageController.recover_page_to_crawlable(plan, app, device, page_now)
        del node
    del plan, app, device, page_before_run, init
    return page_now


def crawl_activities(plan, app, device):
    if Setting.CrawlModel == 'Activity':
        for activity in app.activities:
            appController.start_activity(device, app.packageName, app.mainActivity)
            time.sleep(3)
            appController.start_activity(device, app.packageName, activity)
            time.sleep(2)
            info = pageController.get_top_activity_info(device)
            if info['activity'] == activity:
                page = pageController.get_page_info(plan, app, device)
                crawl_nodes_in_an_activity(plan, app, device, activity, page, page)
                appController.kill_app(app)
                del page
            del activity, info
    del plan, app, device


def crawl_nodes_in_an_activity(plan, app, device, activity, page_need_crawl, page_now):
    if page_need_crawl.clickableNodesNum > 0:
        for node in nodeController.get_random_nodes(page_need_crawl.clickableNodes):
            # if crash and not keep run , break from deep run .page_need_crawled will be None
            if page_now is None:
                Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
                del node
                break
            # sometimes the need tap node is not shown after one deep run
            if not nodeController.recover_node_shown(plan, app, device, page_now, page_need_crawl, node):
                del node
                continue
            device.save_screen(node, True)
            appController.tap_node(device, node)
            device.update_crawled_activity(node.currentActivity)
            device.update_crawled_nodes(node.nodeInfo)
            device.delete_uncrawled_nodes(node.nodeInfo)
            # if jump out the test app, try to go back & return the final page
            page_after_operation = pageController.check_activity_after_operation(plan, app, device, activity, page_need_crawl, node)
            if page_after_operation is None:
                Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
                page_now = page_after_operation
                del page_after_operation, node
                break
            # compare two pages before & after click .
            # update the after page . leave the new clickable/scrollable/longclickable/edittext nodes only.
            page_now = pageController.get_need_crawl_page(plan, app, device, page_need_crawl, page_after_operation)
            if pageController.page_is_crawlable(app, device, page_now):
                page_now.add_last_page(page_need_crawl)
                page_now.add_entry(node)
                # deep run
                page_now = crawl_nodes_in_an_activity(plan, app, device, activity, page_now, page_now)
            else:
                page_now = page_after_operation
            # if page no crawlable nodes , back to last Page, until has crawlable nodes, if back time >3, break
            page_now = pageController.recover_page_to_crawlable(plan, app, device, page_now)
    if page_need_crawl.longClickableNodesNum > 0:
        for node in nodeController.get_random_nodes(page_need_crawl.longClickableNodes):
            # if crash and not keep run , break from deep run .page_need_crawled will be None
            if page_now is None:
                Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
                del node
                break
            # sometimes the need tap node is not shown after one deep run
            if not nodeController.recover_node_shown(plan, app, device, page_now, page_need_crawl, node):
                del node
                continue
            device.save_screen(node, True)
            appController.long_click_node(device, node)
            device.update_crawled_activity(node.currentActivity)
            device.update_crawled_nodes(node.nodeInfo)
            device.delete_uncrawled_nodes(node.nodeInfo)
            # if jump out the test app, try to go back & return the final page
            page_after_operation = pageController.check_activity_after_operation(plan, app, device, activity, page_need_crawl, node)
            if page_after_operation is None:
                Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
                page_now = page_after_operation
                del page_after_operation, node
                break
            # compare two pages before & after click .
            # update the after page . leave the new clickable/scrollable/longclickable/edittext nodes only.
            page_now = pageController.get_need_crawl_page(plan, app, device, page_need_crawl, page_after_operation)
            if pageController.page_is_crawlable(app, device, page_now):
                page_now.add_last_page(page_need_crawl)
                page_now.add_entry(node)
                # deep run
                page_now = crawl_nodes_in_an_activity(plan, app, device, activity, page_now, page_now)
            else:
                page_now = page_after_operation
            # if page no crawlable nodes , back to last Page, until has crawlable nodes, if back time >3, break
            page_now = pageController.recover_page_to_crawlable(plan, app, device, page_now)
    if page_need_crawl.editTextsNum > 0:
        for node in nodeController.get_random_nodes(page_need_crawl.editTexts):
            # if crash and not keep run , break from deep run .page_need_crawled will be None
            if page_now is None:
                Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
                del node
                break
            # sometimes the need tap node is not shown after one deep run
            if not nodeController.recover_node_shown(plan, app, device, page_now, page_need_crawl, node):
                del node
                continue
            device.save_screen(node, True)
            text = appController.get_random_text(8)
            appController.type_text(device, node, text)
            device.update_crawled_activity(node.currentActivity)
            device.update_crawled_nodes(node.nodeInfo)
            device.delete_uncrawled_nodes(node.nodeInfo)
            # if jump out the test app, try to go back & return the final page
            page_after_operation = pageController.check_activity_after_operation(plan, app, device, activity, page_need_crawl, node)
            if page_after_operation is None:
                Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
                page_now = page_after_operation
                del page_after_operation, node
                break
            # compare two pages before & after click .
            # update the after page . leave the new clickable/scrollable/longclickable/edittext nodes only.
            page_now = pageController.get_need_crawl_page(plan, app, device, page_need_crawl, page_after_operation)
            if pageController.page_is_crawlable(app, device, page_now):
                page_now.add_last_page(page_need_crawl)
                page_now.add_entry(node)
                # deep run
                page_now = crawl_nodes_in_an_activity(plan, app, device, activity, page_now, page_now)
            else:
                page_now = page_after_operation
            # if page no crawlable nodes , back to last Page, until has crawlable nodes, if back time >3, break
            page_now = pageController.recover_page_to_crawlable(plan, app, device, page_now)
    del plan, app, device, activity, page_need_crawl
    return page_now


def crawl_main_nodes(plan, app, device, page_before_run):
    device.update_uncrawled_nodes(page_before_run)
    page_now = PageInfo.Page()
    if pageController.page_is_crawlable(app, device, page_before_run):
        device.update_crawl_page(page_before_run.nodesInfoList)
        if page_before_run.clickableNodesNum > 0:
            page_now = crawl_clickable_nodes(plan, app, device, page_before_run, page_now, False)
        if page_before_run.longClickableNodesNum > 0:
            page_now = crawl_longclickable_nodes(plan, app, device, page_before_run, page_now, False)
        if page_before_run.editTextsNum > 0:
            page_now = crawl_edittext(plan, app, device, page_before_run, page_now, False)
    del plan, app, device, page_before_run
    return page_now


def run_init_cases(plan, app, device):
    Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : run init cases")
    for case in app.initCasesList:
        command = 'adb -s ' + device.id + ' shell am instrument -w -e class ' + case + ' ' + app.testPackageName + '/'\
                  + app.testRunner
        Saver.save_crawler_log_both(plan.logPath, device.logPath, command)
        os.system(command)
        del case, command
    del plan, app, device
    Saver.save_crawler_log_both(plan.logPath, device.logPath, "Run novice guide finish ...")


def crawl_init_nodes(plan, app, device, page_before_run):
    Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : run init nodes")
    device.update_uncrawled_nodes(page_before_run)
    if page_before_run.currentActivity != app.mainActivity or page_before_run.package != app.packageName:
        page_now = PageInfo.Page()
        if page_before_run.clickableNodesNum != 0:
            device.update_crawl_page(page_before_run.nodesInfoList)
            if page_before_run.clickableNodesNum > 0:
                page_now = crawl_clickable_nodes(plan, app, device, page_before_run, page_now, True)
            if page_before_run.longClickableNodesNum > 0:
                page_now = crawl_longclickable_nodes(plan, app, device, page_before_run, page_now, True)
            if page_before_run.editTextsNum > 0:
                page_now = crawl_edittext(plan, app, device, page_before_run, page_now, False)
        del plan, app, device, page_before_run
        return page_now
    else:
        Saver.save_crawler_log_both(plan.logPath, device.logPath, 'Is in ' + app.mainActivity)
        del plan, app, device
        return page_before_run


def init_application(plan, app, device):
    Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : init application")
    if Setting.RunInitNodes:
        appController.start_activity(device, app.packageName, app.launcherActivity)
        launcherPage = PageInfo.Page()
        while True:
            launcherPage = pageController.get_page_info(plan, app, device)
            if launcherPage.clickableNodesNum == 0:
                Saver.save_crawler_log_both(plan.logPath, device.logPath, 'scroll to left')
                appController.drag_screen_to_left(device)
            if launcherPage.clickableNodesNum != 0:
                Saver.save_crawler_log_both(plan.logPath, device.logPath, 'stop scroll')
                break
        Saver.save_crawler_log_both(plan.logPath, device.logPath, 'Step : init nodes run begin')
        crawl_init_nodes(plan, app, device, launcherPage)
        del launcherPage
    if Setting.RunInitCase:
        run_init_cases(plan, app, device)
    # when go in mainActivity, will add the nodes in MainActivity to device.unCrawledNodes
    # if crawl main Nodes , after start mainActivity, these nodes can't be added to the page, will get unCrawlable page
    device.unCrawledNodes = []
    del plan, app, device


def run_test(plan, app, device):
    if device.statue == "unlock":
        Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : Begin test ")

        # init device
        appController.clean_device_logcat(device)

        # uninstall & install apk
        if Setting.UnInstallApk:
            appController.uninstall_app(device, app.packageName)
            appController.uninstall_app(device, app.testPackageName)
        if Setting.InstallApk:
            if not appController.install_app(device, app.apkPath):
                device.update_crawl_statue("InstallExc")
            else:
                appController.install_app(device, app.testApkPath)
        else:
            if not appController.app_is_installed(device, app.packageName):
                if not appController.install_app(device, app.apkPath):
                    device.update_crawl_statue("InstallExc")
                elif appController.app_is_installed(device, app.testPackageName):
                    appController.install_app(device, app.testApkPath)

        if device.crawlStatue != "InstallExc":
            # init app
            device.update_crawl_statue("Initing")
            init_application(plan, app, device)

            # begin crawl
            device.update_crawl_statue("Running")
            if Setting.CrawlModel == 'Normal' or Setting.CrawlModel == 'Random':
                Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : begin to crawl main nodes")
                appController.start_activity(device, app.packageName, app.mainActivity)
                time.sleep(5)
                page = pageController.get_page_info(plan, app, device)
                device.update_begin_crawl_time()
                crawl_main_nodes(plan, app, device, page)
                del page

            crawl_activities(plan, app, device)
            device.endCrawlTime = datetime.datetime.now()
            Saver.save_logcat(plan, device)
            # clean unusable files
            pageController.remove_uidump_xml_file(device)

            # update & save result
            Saver.save_crawler_log_both(plan.logPath, device.logPath,
                                        "Step : " + device.id + " has Crawled " + str(len(device.hasCrawledNodes)) + " nodes.")
            Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : " + device.id + " there are " + str(
                len(device.unCrawledNodes)) + " unCrawled nodes .")
            Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : " + device.id + " has Crawled " + str(
                len(device.hasCrawledActivities)) + " activities .")
            if device.crawlStatue == 'Running':
                device.update_crawl_statue('Passed')
            if device.crawlStatue == "Passed":
                plan.passedDevice += 1
            else:
                plan.failedDevice += 1
    else:
        device.update_crawl_statue('DeviceExc')