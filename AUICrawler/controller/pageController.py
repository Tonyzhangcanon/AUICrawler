# -*- coding:utf-8 -*-

import os
import datetime
import time
from script import Saver
from module import PageInfo
from module import NodeInfo
from config import Setting
import appController
import nodeController
import xml.dom.minidom


def get_top_activity_info(device):
    Saver.save_crawler_log(device.logPath, "Step : get top activity info")
    # linux:
    # adb shell dumpsys activity | grep "mFocusedActivity"
    # windows:
    # adb shell dumpsys activity | findstr "mFocusedActivity"
    info = {}
    # command = 'adb -s ' + device.id + ' shell dumpsys activity | grep "mFocusedActivity"'
    # sometime mResumedActivity is Right
    try:
        command = 'adb -s ' + device.id + ' shell dumpsys activity | grep "mResumedActivity"'
        result = os.popen(command).read()
        packagename = ''
        activity = ''
        if 'u0' not in result and ' com.' not in result:
            result = os.popen(command).read()

        if 'u0 ' in result:
            packagename = result[result.find('u0 ') + len('u0 '):result.find('/')]
        elif ' com.' in result:
            packagename = result[result.find(' com.') + 1:result.find('/')]
        if ' t' in result:
            activity = result[result.find('/') + len('/'):result.find(' t')]
        elif '}' in result:
            activity = result[result.find('/') + len('/'):result.find('}')]
    except Exception, e:
        print (str(e))
        command = 'adb -s ' + device.id + ' shell dumpsys activity | findstr "mResumedActivity"'
        result = os.popen(command).read()
        packagename = ''
        activity = ''
        if 'u0' not in result and ' com.' not in result:
            result = os.popen(command).read()

        if 'u0 ' in result:
            packagename = result[result.find('u0 ') + len('u0 '):result.find('/')]
        elif ' com.' in result:
            packagename = result[result.find(' com.') + 1:result.find('/')]
        if ' t' in result:
            activity = result[result.find('/') + len('/'):result.find(' t')]
        elif '}' in result:
            activity = result[result.find('/') + len('/'):result.find('}')]

    info['packagename'] = packagename
    info['activity'] = activity
    Saver.save_crawler_log(device.logPath, 'Top activity is :' + activity)
    Saver.save_crawler_log(device.logPath, 'Top package is :' + packagename)
    del command, result, packagename, activity, device
    return info


def get_uidump_xml_file(device):
    get_xml_command = 'adb -s ' + device.id + ' shell ' + 'uiautomator dump /data/local/tmp/uidump.xml'
    os.system(get_xml_command)
    pull_command = 'adb -s ' + device.id + ' pull /data/local/tmp/uidump.xml ' + device.logPath + '/Uidump.xml'
    os.system(pull_command)
    rm_command = 'adb -s ' + device.id + ' shell rm /data/local/tmp/uidump.xml'
    os.system(rm_command)
    del device, get_xml_command, pull_command, rm_command


def remove_uidump_xml_file(device):
    try:
        Saver.save_crawler_log(device.logPath, "Step : remove uidunp xml")
        remove_xml_file = device.logPath + '/Uidump.xml'
        os.remove(remove_xml_file)
        del remove_xml_file
    except Exception, e:
        print (str(e))
        Saver.save_crawler_log(device.logPath, "no uidump xml")
    del device


def get_nodes_list(device):
    Saver.save_crawler_log(device.logPath, "Step : get nodes list")
    try:
        dom = xml.dom.minidom.parse(device.logPath + '/Uidump.xml')
        root = dom.documentElement
        nodes = root.getElementsByTagName('node')
        del dom, root
        return nodes
    except Exception, e:
        print (str(e))
        return ''
    del device


def get_page_info(plan, app, device):
    if Setting.TimeModel == 'Limit':
        time_now = datetime.datetime.now()
        if (time_now - device.beginCrawlTime).seconds > (Setting.LimitTime * 60):
            Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : crawl time out , finish crawl.")
            del time_now
            return None
    Saver.save_crawler_log(device.logPath, "get all nodes in this page")
    page = PageInfo.Page()
    result = False
    while not result:
        try:
            get_uidump_xml_file(device)
            dom = xml.dom.minidom.parse(device.logPath + '/Uidump.xml')
            result = True
        except Exception, e:
            print (str(e))
            result = False
    root = dom.documentElement
    nodes = root.getElementsByTagName('node')
    Saver.save_crawler_log(device.logPath, len(nodes))
    info = get_top_activity_info(device)
    for node in nodes:
        n = NodeInfo.Node(node)
        n.update_current_activity(info['activity'])
        if n.resource_id in app.firstClickViews:
            device.save_screen(n, False)
            appController.tap_node(device, n)
            page = get_page_info(plan, app, device)
        page.add_node(device, app, n)
        del node, n
    page = appController.close_sys_alert(plan, app, device, page)
    del result, dom, root, nodes, info, plan, app, device
    return page


# compare two pages before & after click .
# update the after page . leave the new clickable/scrollable/longclickable/edittext nodes only.
def get_need_crawl_page(plan, app, device, page_before_run, page_after_run):
    Saver.save_crawler_log(device.logPath, "Step : get need crawl page now ...")
    if len(page_after_run.nodesList) == 0:
        page_after_run = get_page_info(plan, app, device)
    if page_after_run is not None and len(page_after_run.nodesList) != 0:
        for node in page_after_run.nodesList:
            if node in page_before_run.nodesList:
                page_after_run.remove_clickable_node(node)
                page_after_run.remove_scrollable_node(node)
                page_after_run.remove_longclickable_node(node)
                page_after_run.remove_edit_text(node)
            # after type text in edit text, text & bounds will change , don't need to crawl the edit text again
            if node.isEditText:
                info = [node.index, node.resource_id, node.package, node.content_desc]
                for n in page_after_run.editTexts:
                    i = [n.index, n.resource_id, n.package, n.content_desc]
                    if i == info:
                        page_after_run.remove_edit_text(n)
                        break
                    del i, n
            del node
    del plan, app, device, page_before_run
    return page_after_run


def page_is_crawlable(app, device, page):
    Saver.save_crawler_log(device.logPath, "Step : check page is crawlable or not")
    if page.nodesInfoList not in device.hasCrawlPage \
            and page.package == app.packageName \
            and (page.clickableNodesNum != 0
                 or page.scrollableNodesNum != 0
                 or page.longClickableNodesNum != 0
                 or page.editTextsNum != 0):
        Saver.save_crawler_log(device.logPath, "page is crawlable")
        del app, device, page
        return True
    else:
        Saver.save_crawler_log(device.logPath, "page is not crawlable")
        del app, device, page
        return False


def check_activity_after_operation(plan, app, device, crawl_activity):
    Saver.save_crawler_log(device.logPath, "Step : Check page after operation")
    # if app crashed after crawl , save log & start app ,comtinue
    if Setting.TimeModel == 'Limit':
        time_now = datetime.datetime.now()
        if (time_now - device.beginCrawlTime).seconds > (Setting.LimitTime * 60):
            Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : crawl time out , finish crawl.")
            del plan, app, device, crawl_activity, time_now
            return None
        del time_now
    while True:
        info = get_top_activity_info(device)
        package = info['packagename']
        activity = info['activity']
        if len(package) != 0:
            break
    times = 0
    while activity != crawl_activity:
        if not appController.app_is_running(device, app):
            Saver.save_logcat(plan, device, False)
            appController.clean_device_logcat(device)
            if Setting.KeepRun:
                appController.start_activity(device, app.packageName, crawl_activity)
            else:
                Saver.save_crawler_log_both(plan.logPath, device.logPath,
                                            "Step : crawl app " + device.crawlStatue + ', break crawling..')
                return None
        Saver.save_crawler_log(device.logPath, 'back to ' + crawl_activity)
        device.save_screen_jump_out(package, activity)
        appController.click_back(device)
        time.sleep(2)
        times += 1
        top_activity_info = get_top_activity_info(device)
        package = top_activity_info['packagename']
        activity = top_activity_info['activity']
        if times > 3:
            Saver.save_crawler_log(device.logPath,
                                   "can't back to " + crawl_activity + " after click back 3 times , Restart app")
            appController.start_activity(device, app.packageName, crawl_activity)
            top_activity_info = get_top_activity_info(device)
            top_app_package = top_activity_info['packagename']
            if top_app_package == app.packageName:
                del package, top_activity_info, top_app_package
                break
    del plan, app, device, crawl_activity, activity
    return get_page_info(plan, app, device)


# if jump out the test app, try to go back & return the final page
def check_page_after_operation(plan, app, device):
    Saver.save_crawler_log(device.logPath, "Step : Check page after operation")
    # if app crashed after crawl , save log & start app ,comtinue
    if Setting.TimeModel == 'Limit':
        time_now = datetime.datetime.now()
        if (time_now - device.beginCrawlTime).seconds > (Setting.LimitTime * 60):
            Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : crawl time out , finish crawl.")
            del plan, app, device, time_now
            return None
    while True:
        info = get_top_activity_info(device)
        package = info['packagename']
        activity = info['activity']
        if len(package) != 0:
            del info
            break
        del info
    times = 0
    while package != app.packageName:
        if not appController.app_is_running(device, app):
            Saver.save_logcat(plan, device, False)
            appController.clean_device_logcat(device)
            if Setting.KeepRun:
                appController.start_activity(device, app.packageName, app.mainActivity)
            else:
                Saver.save_crawler_log_both(plan.logPath, device.logPath,
                                            "Step : crawl app " + device.crawlStatue + ', break crawling..')
                del plan, app, device, package, activity
                return None
        Saver.save_crawler_log(device.logPath, 'back to ' + app.packageName)
        device.save_screen_jump_out(package, activity)
        appController.click_back(device)
        times += 1
        top_activity_info = get_top_activity_info(device)
        package = top_activity_info['packagename']
        activity = top_activity_info['activity']
        if times > 3:
            Saver.save_crawler_log(device.logPath,
                                   "can't back to " + app.packageName + " after click back 3 times , Restart app")
            appController.start_activity(device, app.packageName, app.mainActivity)
            top_activity_info = get_top_activity_info(device)
            top_app_package = top_activity_info['packagename']
            if top_app_package == app.packageName:
                del top_activity_info, times, top_app_package
                break
    # if keyboard shown , click device back btn to close keyboard
    if appController.keyboard_is_shown(device):
        appController.click_back(device)
    if activity == 'com.mob.tools.MobUIShell':
        Saver.save_crawler_log(device.logPath, "close login web QQ/Weibo")
        appController.click_back(device)
    page = get_page_info(plan, app, device)
    if page is not None and page.currentActivity == Setting.AppLoginActivity and Setting.Login:
        accountView = nodeController.get_node_by_id(page, app.loginViews[0])
        passwordView = nodeController.get_node_by_id(page, app.loginViews[1])
        loginBtn = nodeController.get_node_by_id(page, app.loginViews[2])
        account = device.accountInfo[0]
        password = device.accountInfo[1]
        device.save_screen(accountView, True)
        appController.type_text(device, accountView, account)
        if appController.keyboard_is_shown(device):
            appController.click_back(device)
        appController.type_text(device, passwordView, password)
        if appController.keyboard_is_shown(device):
            appController.click_back(device)
        appController.tap_node(device, loginBtn)
        page = check_page_after_operation(plan, app, device)
        del accountView, passwordView, loginBtn, account, password, plan, app, device
    return page


def no_uncrawled_clickable_nodes_now(device, page_now):
    if page_now is None:
        del page_now, device
        return True
    Saver.save_crawler_log(device.logPath, "Step : Check there are uncCrawled clickable Nodes in the page now or not")
    result = True
    for node in page_now.nodesList:
        if node.is_clickable() and device.is_in_uncrawled_nodes(node.nodeInfo):
            result = False
            del node
            break
        del node
    if result:
        Saver.save_crawler_log(device.logPath, "no uncrawled  clickable nodes in this page now")
        del device, page_now
        return True
    else:
        Saver.save_crawler_log(device.logPath, "have some uncrawled clickable nodes in this page now")
        del device, page_now
        return False


def no_uncrawled_scrollable_nodes_now(device, page_now):
    if page_now is None:
        del device, page_now
        return True
    Saver.save_crawler_log(device.logPath,
                           "Step : Check there are uncCrawled scrollable Nodes in the page now or not")
    result = True
    for node in page_now.scrollableNodes:
        if device.is_in_uncrawled_nodes(node.nodeInfo):
            result = False
            del node
            break
        del node
    if result:
        Saver.save_crawler_log(device.logPath, "no uncrawled  scrollable nodes in this page now")
        del device, page_now, result
        return True
    else:
        Saver.save_crawler_log(device.logPath, "have some uncrawled scrollable nodes in this page now")
        del device, page_now, result
        return False


def no_uncrawled_longclickable_nodes_now(device, page_now):
    if page_now is None:
        del device, page_now
        return True
    Saver.save_crawler_log(device.logPath,
                           "Step : Check there are uncCrawled longClickable Nodes in the page now or not")
    result = True
    for node in page_now.longClickableNodes:
        if device.is_in_uncrawled_nodes(node.nodeInfo):
            result = False
            del node
            break
        del node
    if result:
        Saver.save_crawler_log(device.logPath, "no uncrawled  longClickable nodes in this page now")
        del device, page_now, result
        return True
    else:
        Saver.save_crawler_log(device.logPath, "have some uncrawled longClickable nodes in this page now")
        del device, page_now, result
        return False


def no_uncrawled_edit_text_now(device, page_now):
    if page_now is None:
        del device, page_now
        return True
    Saver.save_crawler_log(device.logPath,
                           "Step : Check there are uncCrawled editTexts in the page now or not")
    result = True
    for node in page_now.editTexts:
        if device.is_in_uncrawled_nodes(node.nodeInfo):
            result = False
            del node
            break
        del node
    if result:
        Saver.save_crawler_log(device.logPath, "no uncrawled  editTexts in this page now")
        del device, page_now, result
        return True
    else:
        Saver.save_crawler_log(device.logPath, "have some uncrawled editTexts in this page now")
        del device, page_now, result
        return False


# if page no crawlable nodes , back to last Page, until has crawlable nodes, if back time >3, break
def recover_page_to_crawlable(plan, app, device, page_now):
    t = 1
    while page_now is not None and no_uncrawled_clickable_nodes_now(device, page_now) \
            and no_uncrawled_longclickable_nodes_now(device, page_now) \
            and no_uncrawled_edit_text_now(device, page_now):
        if page_now.backBtn is not None \
                and nodeController.node_is_shown_in_page(device, page_now.backBtn, page_now):
            Saver.save_crawler_log(device.logPath, "Step : find the back btn and tap ")
            device.save_screen(page_now.backBtn, False)
            appController.tap_node(device, page_now.backBtn)
            t += 1
            page_now = get_page_info(plan, app, device)
        else:
            Saver.save_crawler_log(device.logPath, "Step : no back btn , click back")
            device.save_screen_jump_out(page_now.package, page_now.currentActivity)
            appController.click_back(device)
            page_now = get_page_info(plan, app, device)
            t += 1
        if t > 2:
            break
    return page_now
