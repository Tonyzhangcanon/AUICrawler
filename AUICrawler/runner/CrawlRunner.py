# -*- coding:utf-8 -*-
__author__ = 'Zhang.zhiyang'

import random
import os
import time
import sys
import xml.dom.minidom
from AUICrawler.script import SaveLog
from PIL import Image
import pylab as pl

reload(sys)
sys.setdefaultencoding('utf-8')

curPath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(curPath)
global click_num
click_num = 1


def install_app(device, apkPath):
    SaveLog.save_crawler_log(device.logPath, 'Step : install app : ' + apkPath)
    command = 'adb -s ' + "\"" + device.id + "\"" + " install -r " + apkPath
    os.system(command)


def uninstall_app(device, packagename):
    SaveLog.save_crawler_log(device.logPath, 'Step : uninstall app : ' + packagename)
    command = 'adb -s ' + "\"" + device.id + "\"" + " uninstall " + packagename
    os.system(command)


def start_activity(device, packagename, activity):
    SaveLog.save_crawler_log(device.logPath, 'Step : start up activity : ' + activity)
    time1 = time.time()
    result = True
    while result:
        command = 'adb -s ' + device.id + ' shell am start -n ' + packagename + '/' + activity
        SaveLog.save_crawler_log(device.logPath, 'start up activity: ' + activity)
        os.popen(command)
        if time.time() - time1 < 10:
            top_activity_info = get_top_activity_info(device)
            top_packagename = top_activity_info['packagename']
            if top_packagename == packagename:
                result = False
        else:
            result = False


def save_screenshot(device, activity, node_info, normal):
    SaveLog.save_crawler_log(device.logPath, "Step : save screenshot ")
    activity = activity
    resource_id = node_info['resource_id']
    resource_id = resource_id[resource_id.find('/') + 1:]
    location = get_node_location(node_info)
    get_screenshot_command = 'adb -s ' + device.id + ' shell /system/bin/screencap -p /sdcard/screenshot.png'
    if normal:
        local_png = device.screenshotPath + '/' \
                    + str(activity) + '-' + str(resource_id) + '-' + str(location[0]) \
                    + '-' + str(location[1]) + '.png'
    else:
        local_png = device.screenshotPath + '/' \
                    + str(activity) + '-' + str(resource_id) + '-' + str(location[0]) \
                    + '-' + str(location[1]) + '-JumpOut' + '.png'
    pull_screenshot_command = 'adb -s ' + device.id + ' pull /sdcard/screenshot.png ' + local_png
    os.popen(get_screenshot_command)
    os.popen(pull_screenshot_command)
    # command = 'adb shell screencap -p | gsed s/' + '\r' + '$//> ' + local_png
    # os.popen(command)
    if normal:
        bounds = get_node_bounds(node_info)
        image = pl.array(Image.open(local_png))
        pl.figure(figsize=(float(device.screenResolution[0]) / 100, float(device.screenResolution[1]) / 100), dpi=100)
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


def save_logcat(plan, device, finish):
    SaveLog.save_crawler_log(plan.logPath, "Step : save device log : " + device.id)
    if not os.path.exists(os.getcwd()):
        os.makedirs(os.getcwd())
    command = 'adb -s ' + device.id + ' logcat -d >> ' + device.logPath + '/logcat.txt'
    os.popen(command)
    get_log_commend = 'adb -s ' + device.id + ' logcat -d'
    log = os.popen(get_log_commend).readlines()
    if not finish:
        for line in log:
            if line.find('System.err') != -1:
                device.update_crawl_statue('HasCrashed')
            elif line.find('ANR') != -1:
                device.update_crawl_statue('HasANR')


def save_result(plan, device):
    SaveLog.save_crawler_log(plan.logPath, "Step : save crawl result ...")


def get_top_activity_info(device):
    SaveLog.save_crawler_log(device.logPath, "Step : get top activity info")
    # linux:
    # adb shell dumpsys activity | grep "mFocusedActivity"
    # windows:
    # adb shell dumpsys activity | findstr "mFocusedActivity"
    info = {}
    command = 'adb -s ' + device.id + ' shell dumpsys activity | grep "mFocusedActivity"'
    result = os.popen(command).read()
    if 'u0 ' in result:
        packagename = result[result.find('u0 ') + len('u0 '):result.find('/')]
    elif ' com.' in result:
        packagename = result[result.find(' com.') + 1:result.find('/')]
    info['packagename'] = packagename
    if ' t' in result:
        activity = result[result.find('/') + len('/'):result.find(' t')]
    else:
        activity = result[result.find('/') + len('/'):result.find('}')]
    info['activity'] = activity
    SaveLog.save_crawler_log(device.logPath, 'Top activity is :' + activity)
    SaveLog.save_crawler_log(device.logPath, 'Top package is :' + packagename)
    return info


def get_uidump_xml_file(device):
    get_xml_command = 'adb -s ' + device.id + ' shell ' + 'uiautomator dump /data/local/tmp/uidump.xml'
    SaveLog.save_crawler_log(device.logPath, 'get uidump.xml')
    os.popen(get_xml_command)
    pull_command = 'adb -s ' + device.id + ' pull /data/local/tmp/uidump.xml ' + device.logPath + '/Uidump.xml'
    SaveLog.save_crawler_log(device.logPath, 'pull uidump.xml')
    os.popen(pull_command)
    rm_command = 'adb -s ' + device.id + ' shell rm /data/local/tmp/uidump.xml'
    SaveLog.save_crawler_log(device.logPath, 'delete uidump.xml')
    os.popen(rm_command)


def remove_uidump_xml_file(device):
    SaveLog.save_crawler_log(device.logPath, "Step : remove uidunp xml")
    remove_xml_file = device.logPath + '/Uidump.xml'
    os.remove(remove_xml_file)


def get_nodes_info_list(device):
    SaveLog.save_crawler_log(device.logPath, "Step : get nodes info list")
    nodes_list = get_nodes_list(device)
    nodes_info_list = []
    for node in nodes_list:
        node_info = {'index': node.getAttribute('index'),
                     'text': node.getAttribute('text'),
                     'resource_id': node.getAttribute('resource-id'),
                     'class': node.getAttribute('class'),
                     'package': node.getAttribute('package'),
                     'bounds': node.getAttribute('bounds'),
                     'content_desc': node.getAttribute('content-desc')}
        nodes_info_list.append(node_info)
    return nodes_info_list


def get_nodes_list(device):
    SaveLog.save_crawler_log(device.logPath, "Step : get nodes list")
    try:
        dom = xml.dom.minidom.parse(device.logPath + '/Uidump.xml')
        root = dom.documentElement
        nodes = root.getElementsByTagName('node')
        SaveLog.save_crawler_log(device.logPath, len(nodes))
        return nodes
    except:
        return ''


def node_is_scrollable(node):
    if node.getAttribute('scrollable') == 'true':
        return True
    else:
        return False


def node_is_clickable(node):
    if node.getAttribute('clickable') == 'true':
        return True
    else:
        return False


def node_is_EditText(node):
    if node.getAttribute('class') == 'android.widget.EditText':
        return True
    else:
        return False


def node_is_shown(app, device, classname, resourceid, contentdesc, nodes):
    result = False
    for node in nodes:
        if node['package'] == app.packageName \
                and node['class'] == classname \
                and node['resource_id'] == resourceid \
                and node['content_desc'] == contentdesc:
            SaveLog.save_crawler_log(device.logPath, "node is shown")
            result = True
            break
    return result


def node_is_existed(app, device, resourceid, nodes):
    result = False
    for node in nodes:
        if node['package'] == app.packageName and node['resource_id'] == resourceid:
            result = True
            SaveLog.save_crawler_log(device.logPath, "node is existed")
            break
    return result


def node_has_shown(app, device, classname, nodes):
    result = False
    SaveLog.save_crawler_log(device.logPath, 'find node')
    for node in nodes:
        if node['package'] == app.packageName and node['class'] == classname:
            SaveLog.save_crawler_log(device.logPath, 'node has shown')
            result = True
            break
    return result


# unused
def node_has_child(node):
    while True:
        n = len(root.childNodes)
        if (n > 1):
            print(n)
            print(root.childNodes)
            break
        root = root.firstChild
    print(n)
    print(len(root.childNodes))


def get_usable_nodes_num(device):
    SaveLog.save_crawler_log(device.logPath, "Step : get usable nodes num")
    get_uidump_xml_file(device)
    nodes = get_nodes_list(device)
    num_list = []
    if not len(nodes) == 0:
        clickable_num = 0
        scrollable_num = 0
        for node in nodes:
            if not node_is_EditText(node):
                if node_is_clickable(node):
                    clickable_num += 1
                if node_is_scrollable(node):
                    scrollable_num += 1
        SaveLog.save_crawler_log(device.logPath, 'clickable nodes num = ' + str(clickable_num))
        SaveLog.save_crawler_log(device.logPath, 'scrollable nodes num = ' + str(scrollable_num))
        num_list.append(clickable_num)
        num_list.append(scrollable_num)
        SaveLog.save_crawler_log(device.logPath, num_list)
        return num_list


def get_clickable_nodes(device):
    SaveLog.save_crawler_log(device.logPath, "Step : get clickable nodes")
    nodes = get_nodes_list(device)
    clickable_nodes = []
    if not len(nodes) == 0:
        for node in nodes:
            if not node_is_EditText(node) and node_is_clickable(node):
                node_info = {'index': node.getAttribute('index'),
                             'text': node.getAttribute('text'),
                             'resource_id': node.getAttribute('resource-id'),
                             'class': node.getAttribute('class'),
                             'package': node.getAttribute('package'),
                             'bounds': node.getAttribute('bounds'),
                             'content_desc': node.getAttribute('content-desc')}
                clickable_nodes.append(node_info)
        SaveLog.save_crawler_log(device.logPath, clickable_nodes)
        SaveLog.save_crawler_log(device.logPath, len(clickable_nodes))
    else:
        SaveLog.save_crawler_log(device.logPath, "no clickable nodes ...")
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


def get_node_bounds(node_info):
    bounds = []
    node_bounds = node_info['bounds']
    x_begin = int(node_bounds[node_bounds.find('[') + 1:node_bounds.find(',')])
    y_begin = int(node_bounds[node_bounds.find(',') + 1:node_bounds.find(']')])
    node_end = node_bounds[node_bounds.index(']') + 1:]
    x_end = int(node_end[node_end.find('[') + 1:node_end.find(',')])
    y_end = int(node_end[node_end.find(',') + 1:node_end.find(']')])
    bounds = [x_begin, y_begin, x_end, y_end]
    return bounds


def drag_screen_to_left(device):
    SaveLog.save_crawler_log(device.logPath, "Step : drag screen to left")
    x_max = str(int(device.screenResolution[0]) - 50)
    # x_min = str(int(resolution[0]) * 0.5)[:str(int(resolution[0]) * 0.5).index('.')]
    command = 'adb -s ' + device.id + ' shell input swipe ' + x_max + ' 100 ' + '20' + ' 100'
    os.popen(command)


def click_back(device):
    SaveLog.save_crawler_log(device.logPath, "Step : click back btn on device")
    command = 'adb -s ' + device.id + ' shell input keyevent 4'
    os.popen(command)


def click_point(device, x_point, y_point):
    command = 'adb -s ' + device.id + ' shell input tap ' + x_point + ' ' + y_point
    SaveLog.save_crawler_log(device.logPath, 'click screen :' + x_point + ',' + y_point)
    os.popen(command)


def click_node(device, packagename, resourceid, nodes_now):
    SaveLog.save_crawler_log(device.logPath, "Step : click node ")
    for node in nodes_now:
        if node['package'] == packagename and node['resource_id'] == resourceid:
            node_location = get_node_location(node)
            print('click ' + packagename + ' ' + resourceid)
            click_point(device, node_location[0], node_location[1])


def ui_has_changed(device, nodes_old, nodes_now):
    SaveLog.save_crawler_log(device.logPath, "Step : check ui ")
    new_nodes = []
    if len(nodes_now) != 0:
        for node in nodes_now:
            if not node in nodes_old:
                new_nodes.append(node)
        if (len(new_nodes)) == 0:
            SaveLog.save_crawler_log(device.logPath, 'no change')
            return new_nodes
        else:
            SaveLog.save_crawler_log(device.logPath, 'new nodes num :' + str(len(new_nodes)))
            return new_nodes
    else:
        return new_nodes


def keyboard_is_shown(device):
    SaveLog.save_crawler_log(device.logPath, "Step : check keyboard")
    command = 'adb -s ' + device.id + ' shell dumpsys input_method'
    result = os.popen(command).read()
    key = 'mInputShown='
    keyboard_status = result[result.index(key) + len(key):result.index(key) + len(key) + 5]
    if keyboard_status == 'true':
        SaveLog.save_crawler_log(device.logPath, "keyboard is shown ")
        return True
    else:
        SaveLog.save_crawler_log(device.logPath, "keyboard is not shown")
        return False


def huawei_authorization(device, nodes):
    SaveLog.save_crawler_log(device.logPath, "Step : check huawei authorization")
    if len(nodes) != 0:
        for node in nodes:
            if node['package'] == 'com.huawei.systemmanager' \
                    and node['resource_id'] == 'com.huawei.systemmanager:id/btn_allow' \
                    and node['text'] == '允许':
                location = get_node_location(node)
                SaveLog.save_crawler_log(device.logPath, 'close huawei authorization View')
                click_point(device, location[0], location[1])
                get_uidump_xml_file(device)
                nodes = get_clickable_nodes(device)
    return nodes


def check_activity(app, device, top_app_package, clickable_nodes):
    SaveLog.save_crawler_log(device.logPath, "Step : check activity")
    # get nodes info list now
    get_uidump_xml_file(device)
    nodes_info_list = get_nodes_info_list(device)
    # check activity
    if node_is_shown(app, device, 'android.widget.Button', '', '下载QQ', nodes_info_list):
        SaveLog.save_crawler_log(device.logPath, 'close qq download  page')
        click_back(device)
        get_uidump_xml_file(device)
        clickable_nodes = get_clickable_nodes(device)
        nodes_info_list = get_nodes_info_list(device)
    if node_is_shown(app, device, 'android.widget.RelativeLayout', app.packageName + ':id/umeng_socialize_titlebar',
                     '', nodes_info_list):
        SaveLog.save_crawler_log(device.logPath, 'close weibo web')
        click_back(device)
        get_uidump_xml_file(device)
        clickable_nodes = get_clickable_nodes(device)
    times = 0
    while top_app_package != app.packageName:
        SaveLog.save_crawler_log(device.logPath, 'back to ' + app.packageName)
        click_back(device)
        times += 1
        top_activity_info = get_top_activity_info(device)
        top_app_package = top_activity_info['packagename']
        if top_app_package == app.packageName:
            get_uidump_xml_file(device)
            clickable_nodes = get_clickable_nodes(device)
            break
        if times > 3:
            SaveLog.save_crawler_log(device.logPath,
                                     "can't back to " + app.packageName + " after click back 3 times , Restart app")
            start_activity(device, app.packageName, app.mainActivity)
            get_uidump_xml_file(device)
            clickable_nodes = get_clickable_nodes(device)
            break
    return clickable_nodes


def get_nodes_after_click(device, app):
    SaveLog.save_crawler_log(device.logPath, 'Step : get nodes after click')
    get_uidump_xml_file(device)
    nodes_after_click = get_clickable_nodes(device)
    # check authorization
    nodes_after_click = huawei_authorization(device, nodes_after_click)
    # wait loading
    nodes_list_after_click = get_nodes_info_list(device)
    time_now = time.time()
    while node_has_shown(app, device, 'android.widget.ProgressBar', nodes_list_after_click):
        SaveLog.save_crawler_log(device.logPath, 'loading...')
        get_uidump_xml_file(device)
        nodes_list_after_click = get_nodes_info_list(device)
        if not node_has_shown(app, device, 'android.widget.ProgressBar', nodes_list_after_click):
            nodes_after_click = get_clickable_nodes(device)
            break
        if time.time() - time_now > 5:
            SaveLog.save_crawler_log(device.logPath, 'time out 5s , back')
            click_back(device)
            break
    return nodes_after_click


def app_is_running(device, app):
    SaveLog.save_crawler_log(device.logPath, "Step : check app is running or not")
    command = "adb -s " + device.id + " shell top -n 1 | grep " + app.packageName
    output = os.popen(command)
    lines = output.readlines()
    if len(lines) == 0:
        SaveLog.save_crawler_log(device.logPath, "app is not running")
        return False
    else:
        SaveLog.save_crawler_log(device.logPath, "app is running")
        return True


def node_is_enabled_to_crawl(plan, app, device, node, nodes):
    SaveLog.save_crawler_log(device.logPath, "Step : check node statue ...")
    node_location = get_node_location(node)
    if node in nodes \
            and node not in plan.hasClickedNodes \
            and node['resource_id'] not in app.unClickViews \
            and node_location[0] != 0 \
            and node_location[1] != 0 \
            and node['package'] == app.packageName:
        SaveLog.save_crawler_log(device.logPath, "Node is enabled to crawl , continue ...")
        return True
    else:
        SaveLog.save_crawler_log(device.logPath, "Node is disabled to crawl , break ...")
        return False


def clean_device_logcat(device):
    SaveLog.save_crawler_log(device.logPath, "Step : clean device logcat cache")
    command = 'adb -s ' + device.id + ' logcat -c'
    os.popen(command)


def back_to_last_page(device, last_page_nodes_list, nodes_list_end_run, nodes_infos_now):
    SaveLog.save_crawler_log(device.logPath, "Step ：back to last page")
    click_back(device)
    get_uidump_xml_file(device)
    nodes_infos_after_back = get_nodes_info_list(device)
    clickable_nodes_now = get_clickable_nodes(device)
    if nodes_infos_after_back != last_page_nodes_list \
            and nodes_infos_after_back != nodes_infos_now \
            and nodes_list_end_run in clickable_nodes_now:
        new_clickable_nodes = ui_has_changed(device, nodes_list_end_run, clickable_nodes_now)
        for n_node in new_clickable_nodes:
            n_node_location = get_node_location(n_node)
            click_point(device, n_node_location[0], n_node_location[1])
            get_uidump_xml_file(device)
            nodes_infos_after = get_nodes_info_list(device)
            if nodes_infos_after == last_page_nodes_list:
                break
            else:
                back_to_last_page(device, nodes_infos_after_back, new_clickable_nodes, nodes_infos_after)


# must change , no save the clicked nodes info ,find the way from the clicked nodes .
def get_recover_way(device, clickable_nodes_now, lastnode_id, way):
    SaveLog.save_crawler_log(device.logPath, "Step : get the recover way ")
    if lastnode_id != 0:
        print(lastnode_id)
        # result = NodeInfo.objects.get(id=lastnode_id)
        # last_node = {'index': result.index, 'text': result.text, 'resource_id': result.resourceid,
        #              'class': result.classname, 'location': result.location,
        #              'package': result.packagename, 'content_desc': result.contentdesc}
        # way.append(last_node)
        # find_result = False
        # for node in clickable_nodes_now:
        #     location = get_node_location(node)
        #     if node['index'] == last_node['index'] and node['text'] == last_node['text'] and node['resourcr_id'] == \
        #             last_node['resource_id'] and node['class'] == last_node['class'] and node['package'] == last_node[
        #         'package'] and node['content_desc'] == last_node['content_desc'] and location == result.location:
        #         find_result = True
        #         break
        # if not find_result:
        #     get_recover_way(clickable_nodes_now, result.lastnodeid, way)


def recover_need_click_view(device, way):
    SaveLog.save_crawler_log(device.logPath, "Step : recover need click view")
    if len(way) != 0:
        for node in way[::-1]:
            location = eval(node['location'])
            click_point(device, location[0], location[1])
            time.sleep(2)


def run_init_nodes(plan, app, device, node, last_nodes, clickable_nodes, activity_before_run, last_node_id, nodes_list):
    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, "Step : run init nodes")
    node_id = last_node_id
    # get top activity now
    top_activity_info = get_top_activity_info(device)
    top_app_package = top_activity_info['packagename']
    top_activity = top_activity_info['activity']
    if top_activity != app.mainActivity:
        SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Check activity')
        clickable_nodes = check_activity(app, device, top_app_package, clickable_nodes)
        nodes_info_list = get_nodes_info_list(device)
        SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Get new nodes')
        if len(clickable_nodes) == 0:
            get_uidump_xml_file(device)
            clickable_nodes = get_clickable_nodes(device)
        new_nodes_infos = ui_has_changed(device, last_nodes, clickable_nodes)
        if len(new_nodes_infos) != 0:
            SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Run in for')
            # click every node in for
            back_btn = {}
            for node_info in new_nodes_infos:
                # if node has clicked so don't click again
                get_uidump_xml_file(device)
                nodes = get_clickable_nodes(device)
                node_location = get_node_location(node_info)
                if node_is_enabled_to_crawl(plan, app, device, node_info, nodes):
                    if node_info['resource_id'] in app.backBtnViews:
                        back_btn = node_info
                        continue
                    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Click node')
                    save_screenshot(device, top_activity, node_info, True)
                    click_point(device, node_location[0], node_location[1])
                    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Add clicked node')
                    plan.update_clicked_nodes(node_info)
                    # check ui , if this page has shown before , so don't run again
                    if keyboard_is_shown(device):
                        click_back(device)
                    top_activity_info_after_click = get_top_activity_info(device)
                    top_activity_after_click = top_activity_info_after_click['activity']
                    top_app_package_after_click = top_activity_info_after_click['packagename']
                    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Upload node info')
                    # node_id = upload_node_info(product, versionName, runCaseTime, device, screen_resolution, node_info,
                    #                            top_activity, top_activity_after_click, last_node_id)
                    # get nodes after click
                    nodes_after_click = get_nodes_after_click(device, app)
                    nodes_after_click = check_activity(app, device, top_app_package_after_click, nodes_after_click)
                    new_nodes_infos = ui_has_changed(device, clickable_nodes, nodes_after_click)
                    if nodes_after_click != last_nodes and len(new_nodes_infos) != 0:
                        SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Run new nodes ...')
                        node_id = run_init_nodes(plan, app, device, node_info, nodes_after_click, clickable_nodes,
                                                 top_activity, node_id, nodes_info_list)
                    # check node , if node has not shown , click last node to mack it shown.
                    get_uidump_xml_file(device)
                    nodes = get_clickable_nodes(device)
                    if node_info not in nodes and len(node) != 0:
                        if node in nodes:
                            location = get_node_location(node)
                            click_point(device, location[0], location[1])
                        else:
                            way = []
                            get_recover_way(device, nodes, last_node_id, way)
                            recover_need_click_view(device, way)
            SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Exit in for')

            nodes_infos_now = get_nodes_info_list(device)
            if nodes_infos_now != nodes_list:
                if len(back_btn) != 0 and back_btn in nodes_infos_now:
                    btn_location = get_node_location(back_btn)
                    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Click Back Btn in this page ...')
                    save_screenshot(device, top_activity, node_info, True)
                    click_point(device, btn_location[0], btn_location[1])
                else:
                    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'back to last page')
                    back_to_last_page(device, nodes_list, new_nodes_infos, nodes_infos_now)

            # get top activity now
            top_activity_info = get_top_activity_info(device)
            top_activity_after_run = top_activity_info['activity']
            if top_activity_after_run != activity_before_run and top_activity_after_run != app.mainActivity:
                SaveLog.save_crawler_log(plan.logPathm, device.logPath, 'back to last activity')
                click_back(device)
    else:
        SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Is in ' + app.mainActivity)
    return node_id


def init_application(plan, app, device, node, last_nodes, last_node_id):
    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, "Step : init application")
    get_uidump_xml_file(device)
    clickable_nodes = get_clickable_nodes(device)
    # check authorization
    clickable_nodes = huawei_authorization(device, clickable_nodes)
    time.sleep(5)
    while True:
        usable_node_num_list = get_usable_nodes_num(device)
        clickable_num = usable_node_num_list[0]
        # scrollable_num = usable_node_num_list[1]
        clickable_nodes = huawei_authorization(device, clickable_nodes)
        if clickable_num == 0:
            SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'scroll to left')
            drag_screen_to_left(device)
        if clickable_num != 0:
            SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'stop scroll')
            break
    top_activity_info = get_top_activity_info(device)
    top_activity_now = top_activity_info['activity']
    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'init run begin')
    nodes_info_list = get_nodes_info_list(device)
    last_node_id = run_init_nodes(plan, app, device, node, last_nodes, clickable_nodes, top_activity_now, last_node_id,
                                  nodes_info_list)
    return last_node_id


def run_novice_guide(plan, device, app):
    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, "Step : run novice guide")
    for case in app.initCasesList:
        command = 'adb -s ' + device.id + ' shell am instrument -w -e class ' + case + ' ' + app.testPackageName + '/' + app.testRunner
        SaveLog.save_crawler_log_both(plan.logPath, device.logPath, command)
        os.popen(command)
    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, "Run novice guide finish ...")


def run_main_nodes_in_random(plan, app, device, node, last_nodes, clickable_nodes, activity_before_run, last_node_id,
                             nodes_list):
    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, "Step : run main nodes in random ")
    node_id = last_node_id
    # get top activity now
    top_activity_info = get_top_activity_info(device)
    top_app_package = top_activity_info['packagename']
    top_activity = top_activity_info['activity']
    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Check activity')
    clickable_nodes = check_activity(app, device, top_app_package, clickable_nodes)
    nodes_info_list = get_nodes_info_list(device)
    top_activity_info = get_top_activity_info(device)
    top_activity = top_activity_info['activity']
    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Get new nodes')
    if len(clickable_nodes) == 0:
        get_uidump_xml_file(device)
        clickable_nodes = get_clickable_nodes(device)
    new_nodes_infos = ui_has_changed(device, last_nodes, clickable_nodes)
    if len(new_nodes_infos) != 0:
        SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Run in for')
        # click every node in for
        if len(new_nodes_infos) * float(plan.coverageLevel) < 1:
            num = 1
        else:
            num = int(len(new_nodes_infos) * float(plan.coverageLevel))
        back_btn = {}
        for node_info in random.sample(new_nodes_infos, num):
            # if node has clicked so don't click again
            get_uidump_xml_file(device)
            nodes = get_clickable_nodes(device)
            node_location = get_node_location(node_info)
            if node_is_enabled_to_crawl(plan, app, device, node_info, nodes):
                if node_info['resource_id'] in app.backBtnViews:
                    back_btn = node_info
                    continue
                SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Click node')
                save_screenshot(device, top_activity, node_info, True)
                click_point(device, node_location[0], node_location[1])
                SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Add clicked node')
                plan.update_clicked_nodes(node_info)
                # check ui , if this page has shown before , so don't run again
                if keyboard_is_shown(device):
                    click_back(device)
                # get nodes after click
                top_activity_info_after_click = get_top_activity_info(device)
                top_activity_after_click = top_activity_info_after_click['activity']
                top_app_package_after_click = top_activity_info_after_click['packagename']
                if top_app_package_after_click != app.packageName:
                    save_screenshot(device, top_activity, node_info, False)
                if not app_is_running(device, app):
                    save_logcat(device, device, False)
                SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Upload node info')
                # node_id = upload_node_info(product, versionName, runCaseTime, device, screen_resolution, node_info,
                #                            top_activity,
                #                            top_activity_after_click, last_node_id)

                nodes_after_click = get_nodes_after_click(device, app)
                nodes_after_click = check_activity(app, device, top_app_package_after_click, nodes_after_click)
                new_nodes_infos = ui_has_changed(device, clickable_nodes, nodes_after_click)
                # contrast nodes
                if len(new_nodes_infos) == 0:
                    nodes_infos_now = get_nodes_info_list(device)
                    if nodes_infos_now != nodes_info_list:
                        SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Close top unusable view')
                        click_back(device)
                if nodes_after_click != last_nodes and len(new_nodes_infos) != 0:
                    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Run new nodes ...')
                    run_main_nodes_in_random(plan, app, device, node_info, nodes_after_click, clickable_nodes,
                                             top_activity, node_id, nodes_info_list)
                # check node , if node has not shown , click last node to mack it shown.
                get_uidump_xml_file(device)
                nodes = get_clickable_nodes(device)
                if node_info not in nodes and len(nodes) != 0:
                    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Recover views shown')
                    if node in nodes:
                        location = get_node_location(node)
                        click_point(device, location[0], location[1])
                    else:
                        SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Recover views by way')
                        way = []
                        get_recover_way(device, nodes, last_node_id, way)
                        recover_need_click_view(device, way)
        SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Exit in for')
        nodes_infos_now = get_nodes_info_list(device)
        if nodes_infos_now != nodes_list:
            if len(back_btn) != 0 and back_btn in nodes_infos_now:
                btn_location = get_node_location(back_btn)
                SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Click Back Btn in this page ...')
                save_screenshot(device, top_activity, node_info, True)
                click_point(device, btn_location[0], btn_location[1])
            else:
                SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Back to last page')
                back_to_last_page(device, nodes_list, new_nodes_infos, nodes_infos_now)
        # get top activity now
        top_activity_info_run = get_top_activity_info(device)
        top_activity_after_run = top_activity_info_run['activity']
        top_package_after_run = top_activity_info_run['packagename']
        if top_activity_after_run != activity_before_run:
            SaveLog.save_crawler_log_both(plan.logPath, device.logPath, 'Back to last activity')
            click_back(device)
        check_activity(app, device, top_package_after_run, clickable_nodes)


def run_test(plan, app, device):
    SaveLog.save_crawler_log_both(plan.logPath, device.logPath, "Step : run test ")
    device.update_crawl_statue("Running")
    last_node_id = 0
    app.versionName += ","
    ini_nodes = []
    ini_node = {}

    uninstall_app(device, app.packageName)
    install_app(device, app.apkPath)

    uninstall_app(device, app.testPackageName)
    install_app(device, app.testApkPath)

    clean_device_logcat(device)

    start_activity(device, app.packageName, app.launcherActivity)
    last_node_id = init_application(plan, app, device, ini_node, ini_nodes, last_node_id)

    time.sleep(5)
    run_novice_guide(plan, device, app)
    start_activity(device, app.packageName, app.mainActivity)
    get_uidump_xml_file(device)
    clickable_nodes = get_clickable_nodes(device)
    nodes_info_list = get_nodes_info_list(device)

    run_main_nodes_in_random(plan, app, device, ini_node, ini_nodes, clickable_nodes, app.mainActivity, last_node_id,
                             nodes_info_list)
    remove_uidump_xml_file(device)
    if device.crawlStatue == 'Running':
        device.update_crawl_statue('Passed')
