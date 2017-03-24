# -*- coding:utf-8 -*-
__author__ = 'Zhang.zhiyang'

import random
import os
import time
import sys
import xml.dom.minidom
from AUICrawler.script import Saver
from PIL import Image
from AUICrawler.module.PageInfo import Page
from AUICrawler.module.NodeInfo import Node
from AUICrawler.script import Setting
import pylab as pl

reload(sys)
sys.setdefaultencoding('utf-8')

curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)
global page_need_crawled
global screenshot_num
global jump_out_time
screenshot_num = 1
jump_out_time = 1


def install_app(device, apk_path):
    Saver.save_crawler_log(device.logPath, 'Step : install app : ' + apk_path)
    command = 'adb -s ' + "\"" + device.id + "\"" + " install -r " + apk_path
    os.system(command)


def uninstall_app(device, package_name):
    Saver.save_crawler_log(device.logPath, 'Step : uninstall app : ' + package_name)
    command = 'adb -s ' + "\"" + device.id + "\"" + " uninstall " + package_name
    os.system(command)


def start_activity(device, packagename, activity):
    Saver.save_crawler_log(device.logPath, 'Step : start up activity : ' + activity)
    time1 = time.time()
    result = False
    while not result:
        command = 'adb -s ' + device.id + ' shell am start -n ' + packagename + '/' + activity
        os.popen(command)
        if time.time() - time1 < 10:
            top_activity_info = get_top_activity_info(device)
            top_packagename = top_activity_info['packagename']
            top_activity = top_activity_info['activity']
            if top_packagename == packagename and top_activity == activity:
                result = True
        else:
            result = True


def kill_app(app):
    c = 'adb shell  am force-stop ' + app.packageName
    os.popen(c)


def save_logcat(plan, device, finish):
    Saver.save_crawler_log(plan.logPath, "Step : save device log : " + device.id)
    if not os.path.exists(os.getcwd()):
        os.makedirs(os.getcwd())
    command = 'adb -s ' + device.id + ' logcat -d >> ' + device.logPath + '/logcat.txt'
    os.popen(command)
    if not finish:
        get_log_commend = 'adb -s ' + device.id + ' logcat -d'
        log = os.popen(get_log_commend).readlines()
        for line in log:
            if line.find('System.err') != -1:
                device.update_crawl_statue('HasCrashed')
            elif line.find('ANR') != -1:
                device.update_crawl_statue('HasANR')


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
    except:
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
    return info


def get_uidump_xml_file(device):
    get_xml_command = 'adb -s ' + device.id + ' shell ' + 'uiautomator dump /data/local/tmp/uidump.xml'
    os.popen(get_xml_command)
    pull_command = 'adb -s ' + device.id + ' pull /data/local/tmp/uidump.xml ' + device.logPath + '/Uidump.xml'
    os.popen(pull_command)
    rm_command = 'adb -s ' + device.id + ' shell rm /data/local/tmp/uidump.xml'
    os.popen(rm_command)


def remove_uidump_xml_file(device):
    Saver.save_crawler_log(device.logPath, "Step : remove uidunp xml")
    remove_xml_file = device.logPath + '/Uidump.xml'
    os.remove(remove_xml_file)


def get_nodes_list(device):
    Saver.save_crawler_log(device.logPath, "Step : get nodes list")
    try:
        dom = xml.dom.minidom.parse(device.logPath + '/Uidump.xml')
        root = dom.documentElement
        nodes = root.getElementsByTagName('node')
        return nodes
    except:
        return ''


def node_is_scrollable(node):
    if node.scrollable == 'true':
        return True
    else:
        return False


def node_is_clickable(node):
    if node.clickable == 'true':
        return True
    else:
        return False


def node_is_longclickable(node):
    if node.longClickable == 'true':
        return True
    else:
        return False


def node_is_edittext(node):
    if node.className == 'android.widget.EditText':
        return True
    else:
        return False


def get_clickable_nodes(device):
    Saver.save_crawler_log(device.logPath, "Step : get clickable nodes")
    nodes = get_nodes_list(device)
    clickable_nodes = []
    if not len(nodes) == 0:
        for node in nodes:
            if not node_is_edittext(node) and node_is_clickable(node):
                node_info = {'index': node.getAttribute('index'),
                             'text': node.getAttribute('text'),
                             'resource_id': node.getAttribute('resource-id'),
                             'class': node.getAttribute('class'),
                             'package': node.getAttribute('package'),
                             'bounds': node.getAttribute('bounds'),
                             'content_desc': node.getAttribute('content-desc')}
                clickable_nodes.append(node_info)
        Saver.save_crawler_log(device.logPath, clickable_nodes)
        Saver.save_crawler_log(device.logPath, len(clickable_nodes))
    else:
        Saver.save_crawler_log(device.logPath, "no clickable nodes ...")
    return clickable_nodes


def get_node_location(node_info):
    location = []
    node_bounds = node_info['bounds']
    x_begin = node_bounds[node_bounds.find('[') + 1:node_bounds.find(',')]
    y_begin = node_bounds[node_bounds.find(',') + 1:node_bounds.find(']')]
    node_end = node_bounds[node_bounds.index(']') + 1:]
    x_end = node_end[node_end.find('[') + 1:node_end.find(',')]
    y_end = node_end[node_end.find(',') + 1:node_end.find(']')]
    x = (int(x_begin) + int(x_end)) / 2
    location.append(str(x))
    y = (int(y_begin) + int(y_end)) / 2
    location.append(str(y))
    return location


def drag_screen_to_left(device):
    Saver.save_crawler_log(device.logPath, "Step : drag screen to left")
    # x_max = str(int(device.screenResolution[0]) - 50)
    # x_min = str(int(resolution[0]) * 0.5)[:str(int(resolution[0]) * 0.5).index('.')]
    # command = 'adb -s ' + device.id + ' shell input swipe ' + x_max + ' 100 ' + '20' + ' 100'
    command = 'adb -s ' + device.id + ' shell input keyevent 22'
    os.popen(command)


def drag_screen_to_right(device):
    Saver.save_crawler_log(device.logPath, "Step : drag screen to right")
    command = 'adb -s ' + device.id + ' shell input keyevent 21'
    os.popen(command)


def click_back(device):
    Saver.save_crawler_log(device.logPath, "Step : click back btn on device")
    command = 'adb -s ' + device.id + ' shell input keyevent 4'
    os.popen(command)


def click_point(device, x_point, y_point):
    command = 'adb -s ' + device.id + ' shell input tap ' + x_point + ' ' + y_point
    Saver.save_crawler_log(device.logPath, 'click screen :' + x_point + ',' + y_point)
    os.popen(command)


def long_click_point(device, x, y):
    command = 'adb -s' + device.id + 'shell input swipe ' + x + ' ' + y + ' ' + x + ' ' + y + ' 1000'
    Saver.save_crawler_log(device.logPath, 'long click screen :' + x + ',' + y)
    os.popen(command)


def keyboard_is_shown(device):
    Saver.save_crawler_log(device.logPath, "Step : check keyboard")
    command = 'adb -s ' + device.id + ' shell dumpsys input_method'
    result = os.popen(command).read()
    key = 'mInputShown='
    keyboard_status = result[result.index(key) + len(key):result.index(key) + len(key) + 5]
    if keyboard_status == 'true':
        Saver.save_crawler_log(device.logPath, "keyboard is shown ")
        return True
    else:
        Saver.save_crawler_log(device.logPath, "keyboard is not shown")
        return False


def close_sys_alert(plan, app, device, page_now):
    if page_now is None:
        return page_now
    for node in page_now.clickableNodes:
        info = [node.package, node.resource_id, node.text]
        if info in Setting.AuthorizationAlert:
            Saver.save_crawler_log(device.logPath, "Step : close sys alert")
            save_screen(device, node, False)
            tap_node(device, node)
            page_now = get_page_info(plan, app, device)
    return page_now


def app_is_running(device, app):
    Saver.save_crawler_log(device.logPath, "Step : check app is running or not")
    command = "adb -s " + device.id + " shell top -n 1 | grep " + app.packageName
    output = os.popen(command)
    lines = output.readlines()
    if len(lines) == 0:
        Saver.save_crawler_log(device.logPath, "app is not running")
        return False
    else:
        Saver.save_crawler_log(device.logPath, "app is running")
        return True


def clean_device_logcat(device):
    Saver.save_crawler_log(device.logPath, "Step : clean device logcat cache")
    command = 'adb -s ' + device.id + ' logcat -c'
    os.popen(command)


def get_page_info(plan, app, device):
    if Setting.TimeModel == 'Limit':
        time_now = int(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
        if (time_now - device.beginCrawlTime) > (Setting.LimitTime * 100):
            Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : crawl time out , finish crawl.")
            return None
    Saver.save_crawler_log(device.logPath, "get all nodes in this page")
    page = Page()
    result = False
    while not result:
        try:
            get_uidump_xml_file(device)
            dom = xml.dom.minidom.parse(device.logPath + '/Uidump.xml')
            result = True
        except:
            result = False
    root = dom.documentElement
    nodes = root.getElementsByTagName('node')
    Saver.save_crawler_log(device.logPath, len(nodes))
    info = get_top_activity_info(device)
    for node in nodes:
        n = Node(node)
        n.update_current_activity(info['activity'])
        if n.resource_id in app.firstClickViews:
            save_screen(device, n, False)
            tap_node(device, n)
            page = get_page_info(plan, app, device)
            if page is not None:
                page.add_entry(n)
        page.add_node(device, app, n)
    page = close_sys_alert(plan, app, device, page)
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
    return page_after_run


def find_node_by_info(app, device, classname, resourceid, contentdesc, page):
    result = False
    for node in page.nodesList:
        if node.package == app.packageName and node.className == classname and node.resource_id == resourceid and contentdesc == contentdesc:
            result = True
            break
    return result


def get_node_by_id(page, id):
    for node in page.nodesInfoList:
        if node.resource_id == id:
            return node


def node_is_shown_in_page(device, node, page):
    if node in page.nodesList:
        Saver.save_crawler_log(device.logPath, "node is shown in page now")
        return True
    else:
        Saver.save_crawler_log(device.logPath, "node is not shown in page now")
        return False


def tap_node(device, node):
    Saver.save_crawler_log(device.logPath, "tap node ")
    location = node.location
    click_point(device, location[0], location[1])
    node.update_operation('tap')


def long_click_node(device, node):
    Saver.save_crawler_log(device.logPath, "long click node")
    location = node.location
    long_click_point(device, location[0], location[1])
    node.update_operation('longclick')


def get_random_text(length):
    text = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    for i in range(length):
        text += chars[random.randint(0, len(chars) - 1)]
    return text


def type_text(device, edittext, text):
    tap_node(device, edittext)
    command = 'adb -s ' + device.id + ' shell input text ' + text
    os.popen(command)
    edittext.update_operation('type')


def page_is_crawlable(app, device, page):
    Saver.save_crawler_log(device.logPath, "Step : check page is crawlable or not")
    if page.nodesInfoList not in device.hasCrawlPage \
            and page.package == app.packageName \
            and (page.clickableNodesNum != 0
                 or page.scrollableNodesNum != 0
                 or page.longClickableNodesNum != 0
                 or page.editTextsNum != 0):
        Saver.save_crawler_log(device.logPath, "page is crawlable")
        return True
    else:
        Saver.save_crawler_log(device.logPath, "page is not crawlable")
        return False


def get_node_recover_way(device, page_now, page_before_run, node, way):
    Saver.save_crawler_log(device.logPath, "Step : get node recover way ,node info : " + str(node.nodeInfo))
    way_this_deep = way
    result = False
    if page_before_run is not None and page_before_run.entryNum != 0:
        for entry in page_before_run.entry:
            Saver.save_crawler_log(device.logPath, entry.resource_id)
            if page_now is not None and entry.nodeInfo in page_now.nodesInfoList:
                way_this_deep.insert(0, entry)
                node.update_recover_way(way_this_deep)
                Saver.save_crawler_log(device.logPath, "get the node recover way success. ")
                Saver.save_crawler_log(device.logPath, str(way_this_deep))
                result = True
                break
    if not result:
        if page_before_run is not None and page_before_run.lastPageNum != 0:
            Saver.save_crawler_log(device.logPath, "have " + str(page_before_run.lastPageNum) + ' entries')
            p = page_before_run.lastPage
            for e in page_before_run.entry:
                Saver.save_crawler_log(device.logPath, e.resource_id)
                way_this_deep.insert(page_before_run.entry.index(e), e)
            result = get_node_recover_way(device, page_now, p, node, way_this_deep)
    if result:
        return True
    else:
        Saver.save_crawler_log(device.logPath, "get the node recover way false. ")
        return False


def recover_node_shown(plan, app, device, page_now, page_before_run, node):
    t = 1
    r = False
    while page_now is not None and page_now.nodesNum != 0 and node.nodeInfo not in page_now.nodesInfoList:
        if get_node_recover_way(device, page_now, page_before_run, node, []):
            r = True
            break
        Saver.save_crawler_log(device.logPath, "Step : no recover way , click back")
        save_screen_jump_out(device, page_now.package, page_now.currentActivity)
        click_back(device)
        page_now = get_page_info(plan, app, device)
        t += 1
        if t > 3:
            Saver.save_crawler_log(device.logPath, "can't find the node after back 3 times.")
            break
    if r:
        Saver.save_crawler_log(device.logPath, "Step : recover node shown")
        for n in node.recoverWay:
            save_screen(device, n, False)
            if n.crawlOperation == 'tap':
                tap_node(device, n)
            elif n.crawlOperation == 'longclick':
                long_click_node(device, n)
            elif n.crawlOperation == 'type':
                t = get_random_text(8)
                type_text(device, n, t)
            check_page_after_operation(plan, app, device)
    if t < 4:
        r = True
    return r


def check_activity_after_operation(plan, app, device, crawl_activity):
    Saver.save_crawler_log(device.logPath, "Step : Check page after operation")
    # if app crashed after crawl , save log & start app ,comtinue
    if Setting.TimeModel == 'Limit':
        time_now = int(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
        if (time_now - device.beginCrawlTime) > (Setting.LimitTime * 100):
            Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : crawl time out , finish crawl.")
            return None
    while True:
        info = get_top_activity_info(device)
        package = info['packagename']
        activity = info['activity']
        if len(package) != 0:
            break
    times = 0
    while activity != crawl_activity:
        if not app_is_running(device, app):
            save_logcat(plan, device, False)
            clean_device_logcat(device)
            if Setting.KeepRun:
                start_activity(device, app.packageName, crawl_activity)
            else:
                Saver.save_crawler_log_both(plan.logPath, device.logPath,
                                            "Step : crawl app " + device.crawlStatue + ', break crawling..')
                return None
        Saver.save_crawler_log(device.logPath, 'back to ' + crawl_activity)
        save_screen_jump_out(device, package, activity)
        click_back(device)
        time.sleep(2)
        times += 1
        top_activity_info = get_top_activity_info(device)
        package = top_activity_info['packagename']
        activity = top_activity_info['activity']
        if times > 3:
            Saver.save_crawler_log(device.logPath,
                                   "can't back to " + crawl_activity + " after click back 3 times , Restart app")
            start_activity(device, app.packageName, crawl_activity)
            top_activity_info = get_top_activity_info(device)
            top_app_package = top_activity_info['packagename']
            if top_app_package == app.packageName:
                break
    return get_page_info(plan, app, device)


# if jump out the test app, try to go back & return the final page
def check_page_after_operation(plan, app, device):
    Saver.save_crawler_log(device.logPath, "Step : Check page after operation")
    # if app crashed after crawl , save log & start app ,comtinue

    if Setting.TimeModel == 'Limit':
        time_now = int(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
        if (time_now - device.beginCrawlTime) > (Setting.LimitTime * 100):
            Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : crawl time out , finish crawl.")
            return None
    while True:
        info = get_top_activity_info(device)
        package = info['packagename']
        activity = info['activity']
        if len(package) != 0:
            break
    times = 0
    while package != app.packageName:
        if not app_is_running(device, app):
            save_logcat(plan, device, False)
            clean_device_logcat(device)
            if Setting.KeepRun:
                start_activity(device, app.packageName, app.mainActivity)
            else:
                Saver.save_crawler_log_both(plan.logPath, device.logPath,
                                            "Step : crawl app " + device.crawlStatue + ', break crawling..')
                return None
        Saver.save_crawler_log(device.logPath, 'back to ' + app.packageName)
        save_screen_jump_out(device, package, activity)
        click_back(device)
        times += 1
        top_activity_info = get_top_activity_info(device)
        package = top_activity_info['packagename']
        activity = top_activity_info['activity']
        if times > 3:
            Saver.save_crawler_log(device.logPath,
                                   "can't back to " + app.packageName + " after click back 3 times , Restart app")
            start_activity(device, app.packageName, app.mainActivity)
            top_activity_info = get_top_activity_info(device)
            top_app_package = top_activity_info['packagename']
            if top_app_package == app.packageName:
                break
    # if keyboard shown , click device back btn to close keyboard
    if keyboard_is_shown(device):
        click_back(device)
    if activity == 'com.mob.tools.MobUIShell':
        Saver.save_crawler_log(device.logPath, "close login web QQ/Weibo")
        click_back(device)
    page = get_page_info(plan, app, device)
    if page is not None and page.currentActivity == Setting.AppLoginActivity and Setting.Login:
        accountView = get_node_by_id(page, app.loginViews[0])
        passwordView = get_node_by_id(page, app.loginViews[1])
        loginBtn = get_node_by_id(page, app.loginViews[2])
        account = device.accountInfo[0]
        password = device.accountInfo[1]
        save_screen(device, accountView, True)
        type_text(device, accountView, account)
        if keyboard_is_shown(device):
            click_back(device)
        type_text(device, passwordView, password)
        if keyboard_is_shown(device):
            click_back(device)
        tap_node(device, loginBtn)
        page = check_page_after_operation(plan, app, device)
    return page


def save_screen(device, node, model):
    if Setting.SaveScreen:
        try:
            global screenshot_num
            Saver.save_crawler_log(device.logPath, "Step : save screenshot ")
            get_screenshot_command = 'adb -s ' + device.id + ' shell /system/bin/screencap -p /sdcard/screenshot.png'
            activity = node.currentActivity
            resource_id = node.resource_id
            resource_id = resource_id[resource_id.find('/') + 1:]
            location = node.location
            if model:
                local_png = device.screenshotPath + '/' + str(screenshot_num) + '-' + str(activity) + '-' + str(
                    resource_id) + '-' + str(location[0]) + '-' + str(location[1]) + '.png'
            else:
                local_png = device.screenshotPath + '/' + str(screenshot_num) + '-' + 'unCrawl' + '-' + str(
                    activity) + '-' + str(
                    resource_id) + '-' + str(location[0]) + '-' + str(location[1]) + '.png'
            pull_screenshot_command = 'adb -s ' + device.id + ' pull /sdcard/screenshot.png ' + local_png
            os.popen(get_screenshot_command)
            os.popen(pull_screenshot_command)
            screenshot_num += 1
            # command = 'adb shell screencap -p | gsed s/' + '\r' + '$//> ' + local_png
            # os.popen(command)
            bounds = node.bounds
            image = pl.array(Image.open(local_png))
            pl.figure(figsize=(float(device.screenResolution[0]) / 100, float(device.screenResolution[1]) / 100),
                      dpi=100)
            pl.imshow(image)
            x = [bounds[0], bounds[0], bounds[2], bounds[2], bounds[0]]
            y = [bounds[1], bounds[3], bounds[3], bounds[1], bounds[1]]
            pl.axis('off')
            pl.axis('scaled')
            pl.axis([0, int(device.screenResolution[0]), int(device.screenResolution[1]), 0])
            pl.plot(x[:5], y[:5], 'r', linewidth=2)
            pl.savefig(local_png)
            im = Image.open(local_png)
            box = (float(device.screenResolution[0]) / 8, float(device.screenResolution[1]) / 9,
                   float(device.screenResolution[0]) * 65 / 72, float(device.screenResolution[1]) * 8 / 9)
            region = im.crop(box)
            region.save(local_png)
            pl.close()
        except:
            Saver.save_crawler_log(device.logPath, "save screen error")


def save_screen_jump_out(device, package, activity):
    if Setting.SaveJumpOutScreen:
        try:
            global jump_out_time, screenshot_num
            Saver.save_crawler_log(device.logPath, "Step : jump out . save screenshot ")
            get_screenshot_command = 'adb -s ' + device.id + ' shell /system/bin/screencap -p /sdcard/screenshot.png'
            local_png = device.screenshotPath + '/' + str(screenshot_num) + '-' + str(package) + '-' + str(
                activity) + '-Jump' + str(jump_out_time) + '.png'
            pull_screenshot_command = 'adb -s ' + device.id + ' pull /sdcard/screenshot.png ' + local_png
            os.popen(get_screenshot_command)
            os.popen(pull_screenshot_command)
            screenshot_num += 1
            jump_out_time += 1
        except:
            Saver.save_crawler_log(device, "save screen error")


def no_uncrawled_clickable_nodes_now(device, page_now):
    if page_now is None:
        return True
    Saver.save_crawler_log(device.logPath, "Step : Check there are uncCrawled clickable Nodes in the page now or not")
    result = True
    for node in page_now.nodesList:
        if node_is_clickable(node) and device.is_in_uncrawled_nodes(node.nodeInfo):
            result = False
            break
    if result:
        Saver.save_crawler_log(device.logPath, "no uncrawled  clickable nodes in this page now")
        return True
    else:
        Saver.save_crawler_log(device.logPath, "have some uncrawled clickable nodes in this page now")
        return False


def no_uncrawled_scrollable_nodes_now(device, page_now):
    if page_now is None:
        return True
    Saver.save_crawler_log(device.logPath,
                           "Step : Check there are uncCrawled scrollable Nodes in the page now or not")
    result = True
    for node in page_now.scrollableNodes:
        if device.is_in_uncrawled_nodes(node.nodeInfo):
            result = False
            break
    if result:
        Saver.save_crawler_log(device.logPath, "no uncrawled  scrollable nodes in this page now")
        return True
    else:
        Saver.save_crawler_log(device.logPath, "have some uncrawled scrollable nodes in this page now")
        return False


def no_uncrawled_longclickable_nodes_now(device, page_now):
    if page_now is None:
        return True
    Saver.save_crawler_log(device.logPath,
                           "Step : Check there are uncCrawled longClickable Nodes in the page now or not")
    result = True
    for node in page_now.longClickableNodes:
        if device.is_in_uncrawled_nodes(node.nodeInfo):
            result = False
            break
    if result:
        Saver.save_crawler_log(device.logPath, "no uncrawled  longClickable nodes in this page now")
        return True
    else:
        Saver.save_crawler_log(device.logPath, "have some uncrawled longClickable nodes in this page now")
        return False


def no_uncrawled_edit_text_now(device, page_now):
    if page_now is None:
        return True
    Saver.save_crawler_log(device.logPath,
                           "Step : Check there are uncCrawled editTexts in the page now or not")
    result = True
    for node in page_now.editTexts:
        if device.is_in_uncrawled_nodes(node.nodeInfo):
            result = False
            break
    if result:
        Saver.save_crawler_log(device.logPath, "no uncrawled  editTexts in this page now")
        return True
    else:
        Saver.save_crawler_log(device.logPath, "have some uncrawled editTexts in this page now")
        return False


# if page no crawlable nodes , back to last Page, until has crawlable nodes, if back time >3, break
def recover_page_to_crawlable(plan, app, device, page_now):
    t = 1
    while page_now is not None and no_uncrawled_clickable_nodes_now(device, page_now) \
            and no_uncrawled_longclickable_nodes_now(device, page_now) \
            and no_uncrawled_edit_text_now(device, page_now):
        if page_now.backBtn is not None \
                and node_is_shown_in_page(device, page_now.backBtn, page_now):
            Saver.save_crawler_log(device.logPath, "Step : find the back btn and tap ")
            save_screen(device, page_now.backBtn, False)
            tap_node(device, page_now.backBtn)
            t += 1
            page_now = get_page_info(plan, app, device)
        else:
            Saver.save_crawler_log(device.logPath, "Step : no back btn , click back")
            save_screen_jump_out(device, page_now.package, page_now.currentActivity)
            click_back(device)
            page_now = get_page_info(plan, app, device)
            t += 1
        if t > 2:
            break
    return page_now


def get_random_nodes(nodes_list):
    if Setting.CrawlModel == 'Normal':
        return nodes_list
    else:
        if len(nodes_list) * float(Setting.CoverageLevel) < 1:
            num = 1
        else:
            num = int(len(nodes_list) * float(Setting.CoverageLevel))
        return random.sample(nodes_list, num)


def crawl_clickable_nodes(plan, app, device, page_before_run, page_now, init):
    for node in get_random_nodes(page_before_run.clickableNodes):
        # if crash and not keep run , break from deep run .page_need_crawled will be None
        if page_now is None:
            Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
            break
        # sometimes the need tap node is not shown after one deep run
        if not recover_node_shown(plan, app, device, page_now, page_before_run, node):
            continue
        save_screen(device, node, True)
        tap_node(device, node)
        device.update_crawled_activity(node.currentActivity)
        device.update_crawled_nodes(node.nodeInfo)
        device.delete_uncrawled_nodes(node.nodeInfo)
        # if jump out the test app, try to go back & return the final page
        page_after_operation = check_page_after_operation(plan, app, device)
        if page_after_operation is None:
            Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
            page_now = page_after_operation
            break
        # compare two pages before & after click .
        # update the after page . leave the new clickable/scrollable/longclickable/edittext nodes only.
        page_now = get_need_crawl_page(plan, app, device, page_before_run, page_after_operation)
        if page_is_crawlable(app, device, page_now):
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
        page_now = recover_page_to_crawlable(plan, app, device, page_now)
    return page_now


def crawl_longclickable_nodes(plan, app, device, page_before_run, page_now, init):
    for node in get_random_nodes(page_before_run.longClickableNodes):
        # if crash and not keep run , break from deep run .page_need_crawled will be None
        if page_now is None:
            Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
            break
        # sometimes the need tap node is not shown after one deep run
        if not recover_node_shown(plan, app, device, page_now, page_before_run, node):
            continue
        save_screen(device, node, True)
        long_click_node(device, node)
        device.update_crawled_activity(node.currentActivity)
        device.update_crawled_nodes(node.nodeInfo)
        device.delete_uncrawled_nodes(node.nodeInfo)
        # if jump out the test app, try to go back & return the final page
        page_after_operation = check_page_after_operation(plan, app, device)
        if page_after_operation is None:
            Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
            page_now = page_after_operation
            break
        # compare two pages before & after click .
        # update the after page . leave the new clickable/scrollable/longclickable/edittext nodes only.
        page_now = get_need_crawl_page(plan, app, device, page_before_run, page_after_operation)
        if page_is_crawlable(app, device, page_now):
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
        page_now = recover_page_to_crawlable(plan, app, device, page_now)
    return page_now


def crawl_edittext(plan, app, device, page_before_run, page_now, init):
    for node in get_random_nodes(page_before_run.editTexts):
        # if crash and not keep run , break from deep run .page_need_crawled will be None
        if page_now is None:
            Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
            break
        # sometimes the need tap node is not shown after one deep run
        if not recover_node_shown(plan, app, device, page_now, page_before_run, node):
            continue
        save_screen(device, node, True)
        text = get_random_text(8)
        type_text(device, node, text)
        device.update_crawled_activity(node.currentActivity)
        device.update_crawled_nodes(node.nodeInfo)
        device.delete_uncrawled_nodes(node.nodeInfo)
        # if jump out the test app, try to go back & return the final page
        page_after_operation = check_page_after_operation(plan, app, device)
        if page_after_operation is None:
            Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
            page_now = page_after_operation
            break
        # compare two pages before & after click .
        # update the after page . leave the new clickable/scrollable/longclickable/edittext nodes only.
        page_now = get_need_crawl_page(plan, app, device, page_before_run, page_after_operation)
        if page_is_crawlable(app, device, page_now):
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
        page_now = recover_page_to_crawlable(plan, app, device, page_now)
    return page_now


def crawl_activities(plan, app, device):
    if Setting.CrawlModel == 'Activity':
        for activity in app.activities:
            start_activity(device, app.packageName, app.mainActivity)
            time.sleep(3)
            start_activity(device, app.packageName, activity)
            time.sleep(2)
            info = get_top_activity_info(device)
            if info['activity'] == activity:
                page = get_page_info(plan, app, device)
                crawl_nodes_in_an_activity(plan, app, device, activity, page, page)
                kill_app(app)


def crawl_nodes_in_an_activity(plan, app, device, activity, page_need_crawl, page_now):
    if page_need_crawl.clickableNodesNum > 0:
        for node in get_random_nodes(page_need_crawl.clickableNodes):
            # if crash and not keep run , break from deep run .page_need_crawled will be None
            if page_now is None:
                Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
                break
            # sometimes the need tap node is not shown after one deep run
            if not recover_node_shown(plan, app, device, page_now, page_need_crawl, node):
                continue
            save_screen(device, node, True)
            tap_node(device, node)
            device.update_crawled_activity(node.currentActivity)
            device.update_crawled_nodes(node.nodeInfo)
            device.delete_uncrawled_nodes(node.nodeInfo)
            # if jump out the test app, try to go back & return the final page
            page_after_operation = check_activity_after_operation(plan, app, device, activity)
            if page_after_operation is None:
                Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
                page_now = page_after_operation
                break
            # compare two pages before & after click .
            # update the after page . leave the new clickable/scrollable/longclickable/edittext nodes only.
            page_now = get_need_crawl_page(plan, app, device, page_need_crawl, page_after_operation)
            if page_is_crawlable(app, device, page_now):
                page_now.add_last_page(page_need_crawl)
                page_now.add_entry(node)
                # deep run
                page_now = crawl_nodes_in_an_activity(plan, app, device, activity, page_now, page_now)
            else:
                page_now = page_after_operation
            # if page no crawlable nodes , back to last Page, until has crawlable nodes, if back time >3, break
            page_now = recover_page_to_crawlable(plan, app, device, page_now)
    if page_need_crawl.longClickableNodesNum > 0:
        for node in get_random_nodes(page_need_crawl.longClickableNodes):
            # if crash and not keep run , break from deep run .page_need_crawled will be None
            if page_now is None:
                Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
                break
            # sometimes the need tap node is not shown after one deep run
            if not recover_node_shown(plan, app, device, page_now, page_need_crawl, node):
                continue
            save_screen(device, node, True)
            long_click_node(device, node)
            device.update_crawled_activity(node.currentActivity)
            device.update_crawled_nodes(node.nodeInfo)
            device.delete_uncrawled_nodes(node.nodeInfo)
            # if jump out the test app, try to go back & return the final page
            page_after_operation = check_activity_after_operation(plan, app, device, activity)
            if page_after_operation is None:
                Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
                page_now = page_after_operation
                break
            # compare two pages before & after click .
            # update the after page . leave the new clickable/scrollable/longclickable/edittext nodes only.
            page_now = get_need_crawl_page(plan, app, device, page_need_crawl, page_after_operation)
            if page_is_crawlable(app, device, page_now):
                page_now.add_last_page(page_need_crawl)
                page_now.add_entry(node)
                # deep run
                page_now = crawl_nodes_in_an_activity(plan, app, device, activity, page_now, page_now)
            else:
                page_now = page_after_operation
            # if page no crawlable nodes , back to last Page, until has crawlable nodes, if back time >3, break
            page_now = recover_page_to_crawlable(plan, app, device, page_now)
    if page_need_crawl.editTextsNum > 0:
        for node in get_random_nodes(page_need_crawl.editTexts):
            # if crash and not keep run , break from deep run .page_need_crawled will be None
            if page_now is None:
                Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
                break
            # sometimes the need tap node is not shown after one deep run
            if not recover_node_shown(plan, app, device, page_now, page_need_crawl, node):
                continue
            save_screen(device, node, True)
            text = get_random_text(8)
            type_text(device, node, text)
            device.update_crawled_activity(node.currentActivity)
            device.update_crawled_nodes(node.nodeInfo)
            device.delete_uncrawled_nodes(node.nodeInfo)
            # if jump out the test app, try to go back & return the final page
            page_after_operation = check_activity_after_operation(plan, app, device, activity)
            if page_after_operation is None:
                Saver.save_crawler_log(device.logPath, 'Jump out to crawl')
                page_now = page_after_operation
                break
            # compare two pages before & after click .
            # update the after page . leave the new clickable/scrollable/longclickable/edittext nodes only.
            page_now = get_need_crawl_page(plan, app, device, page_need_crawl, page_after_operation)
            if page_is_crawlable(app, device, page_now):
                page_now.add_last_page(page_need_crawl)
                page_now.add_entry(node)
                # deep run
                page_now = crawl_nodes_in_an_activity(plan, app, device, activity, page_now, page_now)
            else:
                page_now = page_after_operation
            # if page no crawlable nodes , back to last Page, until has crawlable nodes, if back time >3, break
            page_now = recover_page_to_crawlable(plan, app, device, page_now)
    return page_now


def crawl_main_nodes(plan, app, device, page_before_run):
    global page_need_crawled
    page_need_crawled = Page()
    if page_is_crawlable(app, device, page_before_run):
        device.update_crawl_page(page_before_run.nodesInfoList)
        if page_need_crawled.clickableNodesNum > 0:
            page_need_crawled = crawl_clickable_nodes(plan, app, device, page_before_run, page_need_crawled, False)
        if page_need_crawled.longClickableNodesNum > 0:
            page_need_crawled = crawl_longclickable_nodes(plan, app, device, page_before_run, page_need_crawled, False)
        if page_need_crawled.editTextsNum > 0:
            page_need_crawled = crawl_edittext(plan, app, device, page_before_run, page_need_crawled, False)
    return page_need_crawled


def run_init_cases(plan, app, device):
    Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : run init cases")
    for case in app.initCasesList:
        command = 'adb -s ' + device.id + ' shell am instrument -w -e class ' + case + ' ' + app.testPackageName + '/' + app.testRunner
        Saver.save_crawler_log_both(plan.logPath, device.logPath, command)
        os.popen(command)
    Saver.save_crawler_log_both(plan.logPath, device.logPath, "Run novice guide finish ...")


def crawl_init_nodes(plan, app, device, page_before_run):
    Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : run init nodes")
    if page_before_run.currentActivity != app.mainActivity or page_before_run.package != app.packageName:
        global page_need_crawled
        page_need_crawled = Page()
        if page_before_run.clickableNodesNum != 0:
            device.update_crawl_page(page_before_run.nodesInfoList)
            if page_need_crawled.clickableNodesNum > 0:
                page_need_crawled = crawl_clickable_nodes(plan, app, device, page_before_run, page_need_crawled, True)
            if page_need_crawled.longClickableNodesNum > 0:
                page_need_crawled = crawl_longclickable_nodes(plan, app, device, page_before_run, page_need_crawled, True)
            if page_need_crawled.editTextsNum > 0:
                page_need_crawled = crawl_edittext(plan, app, device, page_before_run, page_need_crawled, False)
        return page_need_crawled
    else:
        Saver.save_crawler_log_both(plan.logPath, device.logPath, 'Is in ' + app.mainActivity)
        return page_before_run


def init_application(plan, app, device):
    Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : init application")
    if Setting.RunInitNodes:
        start_activity(device, app.packageName, app.launcherActivity)
        launcherPage = Page()
        while True:
            launcherPage = get_page_info(plan, app, device)
            if launcherPage.clickableNodesNum == 0:
                Saver.save_crawler_log_both(plan.logPath, device.logPath, 'scroll to left')
                drag_screen_to_left(device)
            if launcherPage.clickableNodesNum != 0:
                Saver.save_crawler_log_both(plan.logPath, device.logPath, 'stop scroll')
                break
        Saver.save_crawler_log_both(plan.logPath, device.logPath, 'Step : init nodes run begin')
        crawl_init_nodes(plan, app, device, launcherPage)
    if Setting.RunInitCase:
        run_init_cases(plan, app, device)
    # when go in mainActivity, will add the nodes in MainActivity to device.unCrawledNodes
    # if crawl main Nodes , after start mainActivity, these nodes can't be added to the page, will get unCrawlable page
    device.unCrawledNodes = []


def run_test(plan, app, device):
    Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : run test ")
    device.update_crawl_statue("Running")

    # init device
    clean_device_logcat(device)

    # uninstall & install apk
    if Setting.UnInstallApk:
        uninstall_app(device, app.packageName)
        uninstall_app(device, app.testPackageName)
    if Setting.InstallApk:
        install_app(device, app.apkPath)
        install_app(device, app.testApkPath)

    # init app
    init_application(plan, app, device)

    # begin crawl
    if Setting.CrawlModel == 'Normal':
        Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : begin to crawl main nodes")
        start_activity(device, app.packageName, app.mainActivity)
        time.sleep(5)
        page = get_page_info(plan, app, device)
        device.update_begin_crawl_time()
        crawl_main_nodes(plan, app, device, page)

    crawl_activities(plan, app, device)

    # clean unusable files
    remove_uidump_xml_file(device)

    # update & save result
    Saver.save_crawler_log_both(plan.logPath, device.logPath,
                                "Step : " + device.id + " has Crawled " + str(len(device.hasCrawledNodes)) + " nodes.")
    Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : " + device.id + " there are " + str(
        len(device.unCrawledNodes)) + " unCrawled nodes .")
    Saver.save_crawler_log_both(plan.logPath, device.logPath, "Step : " + device.id + " has Crawled " + str(
        len(device.hasCrawledActivities)) + " activities .")
    if device.crawlStatue == 'Running':
        device.update_crawl_statue('Passed')
