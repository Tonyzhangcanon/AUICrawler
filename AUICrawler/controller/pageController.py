# -*- coding:utf-8 -*-

import os
import datetime
import time
from script import Saver
from script import HtmlMaker
from script import MailSender
from module import PageInfo
from module import NodeInfo
from config import Setting
import appController
import nodeController
import xml.dom.minidom
import platform


def get_top_activity_info(device):
    Saver.save_crawler_log(device.logPath, "Step : get top activity info")
    # linux:
    # adb shell dumpsys activity | grep "mFocusedActivity"
    # windows:
    # adb shell dumpsys activity | findstr "mFocusedActivity"
    info = {}
    packagename = ''
    activity = ''
    # command = 'adb -s ' + device.id + ' shell dumpsys activity | grep "mFocusedActivity"'
    # sometime mResumedActivity is Right
    if platform.system() != 'Windows':
        command = 'adb -s ' + device.id + ' shell dumpsys activity | grep "mResumedActivity"'
    else:
        command = 'adb -s ' + device.id + ' shell dumpsys activity | findstr "mResumedActivity"'
    result = os.popen(command).read()
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
    except Exception as e:
        print (str(e))
        Saver.save_crawler_log(device.logPath, "no uidump xml")
    del device


def get_nodes_list(device):
    Saver.save_crawler_log(device.logPath, "Step : get nodes list")
    try:
        dom = xml.dom.minidom.parse(device.logPath + '/Uidump.xml')
        root = dom.documentElement
        nodes = root.getElementsByTagName('node')
        del dom, root, device
        return nodes
    except Exception as e:
        print (str(e))
        del device
        return ''


def get_page_info(plan, app, device):
    if Setting.TimeModel == 'Limit':
        time_now = datetime.datetime.now()
        if (time_now - device.beginCrawlTime).seconds > (Setting.LimitTime * 60):
            Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : crawl time out , finish crawl.")
            del plan, app, device, time_now
            return None
    Saver.save_crawler_log(device.logPath, "get all nodes in this page")
    page = PageInfo.Page()
    result = False
    t = 0
    while not result:
        try:
            if t > 2:
                Saver.save_crawler_log(device.logPath, "get page error after 3 times , click back .")
                appController.click_back(device)
                time.sleep(1)
                get_uidump_xml_file(device)
                break
            get_uidump_xml_file(device)
            dom = xml.dom.minidom.parse(device.logPath + '/Uidump.xml')
            result = True
        except Exception as e:
            t += 1
            print (str(e))
            result = False
    try:
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
        del result, dom, root, nodes, info, plan, app, device, t
        return page
    except Exception as e:
        print (str(e))
        del plan, app, device, t
        return page


# compare two pages before & after click .
# update the after page . leave the new clickable/scrollable/longclickable/edittext nodes only.
def get_need_crawl_page(plan, app, device, page_before_run, page_after_run):
    Saver.save_crawler_log(device.logPath, "Step : get need crawl page now ...")
    if page_after_run.nodesNum == 0:
        page_after_run = get_page_info(plan, app, device)
    new_nodes_num = 0
    if page_after_run is not None and page_after_run.nodesNum != 0:
        for node in page_after_run.nodesList:
            if node.nodeInfo in page_before_run.nodesInfoList:
                page_after_run.remove_clickable_node(node)
                page_after_run.remove_scrollable_node(node)
                page_after_run.remove_longclickable_node(node)
                page_after_run.remove_edit_text(node)
            # after type text in edit text, text & bounds will change , don't need to crawl the edit text again
            elif node.isEditText:
                info = [node.index, node.resource_id, node.package, node.content_desc]
                for n in page_before_run.editTexts:
                    i = [n.index, n.resource_id, n.package, n.content_desc]
                    if i == info:
                        page_after_run.remove_edit_text(node)
                        break
                    del i, n
            # if all new shown crawable nodes are both crawled, click back to recover page shown
            elif not device.is_in_hascrawled_nodes(node.nodeInfo) and not device.is_in_uncrawled_nodes(node.nodeInfo):
                new_nodes_num += 1
            del node
    if page_after_run.clickableNodesNum == page_after_run.longClickableNodesNum == page_after_run.editTextsNum == page_after_run.scrollableNodesNum == 0 \
            and new_nodes_num > 0:
        Saver.save_crawler_log(device.logPath,
                               "Step : no new unCrawled nodes , but has some unCrawlable nodes show , back ...")
        appController.click_back(device)
        page_after_run = get_page_info(plan, app, device)
        return get_need_crawl_page(plan, app, device, page_before_run, page_after_run)
    del plan, app, device, page_before_run
    return page_after_run


def page_is_crawlable(app, device, page):
    Saver.save_crawler_log(device.logPath, "Step : check page is crawlable or not")
    if page.nodesInfoList not in device.hasCrawledPage \
            and page.package == app.packageName \
            and not page.clickableNodesNum == page.scrollableNodesNum == page.longClickableNodesNum == page.editTextsNum == 0:
        Saver.save_crawler_log(device.logPath, "page is crawlable")
        del app, device, page
        return True
    else:
        Saver.save_crawler_log(device.logPath, "page is not crawlable")
        del app, device, page
        return False


def check_activity_after_operation(plan, app, device, crawl_activity, page_before_run, node):
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
            Saver.save_error_logcat(plan, device)
            appController.clean_device_logcat(device)
            HtmlMaker.make_failed_result_html(plan, app)
            MailSender.send_failed_mail_first(plan, app, device)
            if not re_crawl_mack_error_node(plan, app, device, page_before_run, node,
                                            crawl_activity) and Setting.KeepRun:
                appController.kill_app(app)
                appController.start_activity(device, app.packageName, crawl_activity)
                device.statue = device.get_device_statue()
                if device.statue != "unlock":
                    Saver.save_crawler_log_both(plan.logPath, device.logPath,
                                                "Step : device " + device.crawlStatue + ', break crawling..')
                    return None
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
    del crawl_activity, activity, page_before_run, node, times
    return get_page_info(plan, app, device)


def re_crawl_mack_error_node(plan, app, device, page_before_run, node, activity):
    appController.start_activity(device, app.packageName, activity)
    page_now = get_page_info(plan, app, device)
    if nodeController.recover_node_shown(plan, app, device, page_now, page_before_run, node):
        device.save_make_error_node_screen(node)
        if node.crawlOperation == 'tap':
            appController.tap_node(device, node)
        elif node.crawlOperation == 'longclick':
            appController.long_click_node(device, node)
        elif node.crawlOperation == 'type':
            t = appController.get_random_text(8)
            appController.type_text(device, node, t)
        if not appController.app_is_running(device, app):
            Saver.save_error_logcat(plan, device)
            HtmlMaker.make_failed_result_html(plan, app)
            MailSender.send_failed_mail_necessary(plan, app, device, node)
            del plan, app, device, page_before_run, node, activity, page_now
            return False
        else:
            HtmlMaker.make_failed_result_html(plan, app)
            MailSender.send_failed_mail_un_necessary(plan, app, device)
    del plan, app, device, page_before_run, node, activity, page_now
    return True


def login_by_account(plan, page, app, device):
    account_view = nodeController.get_node_by_id(page, app.loginViews[0])
    password_view = nodeController.get_node_by_id(page, app.loginViews[1])
    login_btn = nodeController.get_node_by_id(page, app.loginViews[2])
    account = device.accountInfo[0]
    password = device.accountInfo[1]
    if account_view in page.editTexts and password_view in page.editTexts and login_btn in page.clickableNodes:
        Saver.save_crawler_log(device.logPath, "Login begin .")
        appController.type_text(device, account_view, account)
        if appController.keyboard_is_shown(device):
            appController.click_back(device)
        appController.type_text(device, password_view, password)
        if appController.keyboard_is_shown(device):
            appController.click_back(device)
        appController.tap_node(device, login_btn)
        time0 = time.time()
        while True:
            time1 = time.time()
            if time1 - time0 > 10:
                Saver.save_crawler_log(device.logPath, "Login failed , time out .")
                appController.click_back(device)
                break
            info = get_top_activity_info(device)
            if info['activity'] != app.loginActivity:
                Saver.save_crawler_log(device.logPath, "Login successful .")
                break
    else:
        appController.click_back(device)
    del page, account_view, password_view, login_btn, account, password
    return get_page_info(plan, app, device)


# if jump out the test app, try to go back & return the final page
def check_page_after_operation(plan, app, device, page_before_run, node):
    Saver.save_crawler_log(device.logPath, "Step : Check page after operation")
    # if app crashed after crawl , save log & start app ,continue
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
            Saver.save_error_logcat(plan, device)
            appController.clean_device_logcat(device)
            HtmlMaker.make_failed_result_html(plan, app)
            MailSender.send_failed_mail_first(plan, app, device)
            if not re_crawl_mack_error_node(plan, app, device, page_before_run, node,
                                            app.launcherActivity) and Setting.KeepRun:
                appController.kill_app(app)
                appController.start_activity(device, app.packageName, app.launcherActivity)
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
            appController.start_activity(device, app.packageName, app.launcherActivity)
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
    if page is not None and page.currentActivity == app.loginActivity and Setting.Login:
        app.update_loginactivity_entry(node)
        page = login_by_account(plan, page, app, device)
    del plan, app, device, page_before_run, node
    return page


def no_uncrawled_nodes_now(device, page_now):
    if page_now is None:
        Saver.save_crawler_log(device.logPath, "Step : page_now is None")
        del device, page_now
        return True
    Saver.save_crawler_log(device.logPath,
                           "Step : Check there are uncCrawled nodes in the page now or not")
    for node in page_now.nodesList:
        if node.is_clickable() and device.is_in_uncrawled_nodes(node.nodeInfo):
            Saver.save_crawler_log(device.logPath, "have some uncrawled clickcable nodes in this page now")
            del device, page_now, node
            return False
        if node.is_longclickable() and device.is_in_uncrawled_nodes(node.nodeInfo):
            Saver.save_crawler_log(device.logPath, "have some uncrawled longclickable nodes in this page now")
            del device, page_now, node
            return False
        if node.is_edittext() and device.is_in_uncrawled_nodes(node.nodeInfo):
            Saver.save_crawler_log(device.logPath, "have some uncrawled editexts in this page now")
            del device, page_now, node
            return False
        if node.is_scrollable() and device.is_in_uncrawled_nodes(node.nodeInfo):
            Saver.save_crawler_log(device.logPath, "have some uncrawled scrollable nodes in this page now")
            del device, page_now, node
            return False
        del node
    Saver.save_crawler_log(device.logPath, "no uncrawled nodes in this page now")
    del device, page_now
    return True


# if page no crawlable nodes , back to last Page, until has crawlable nodes, if back time >3, break
def recover_page_to_crawlable(plan, app, device, page_now):
    t = 1
    while page_now is not None and no_uncrawled_nodes_now(device, page_now):
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
    del plan, app, device, t
    return page_now
