# -*- coding:utf-8 -*-

import sys
import os
import random
import datetime
from config import Setting
from script import Saver
import pageController

reload(sys)
sys.setdefaultencoding('utf-8')


def install_app(device, apk_path):
    try:
        if os.path.exists(apk_path):
            Saver.save_crawler_log(device.logPath, 'Step : install app : ' + apk_path)
            command = 'adb -s ' + device.id + " install -r " + apk_path
            os.system(command)
            del device, apk_path, command
    except Exception as e:
        Saver.save_crawler_log(device.logPath, str(e))
        del device, apk_path, e
        Saver.save_crawler_log(device.logPath, 'install app catch exception')


def uninstall_app(device, package_name):
    try:
        Saver.save_crawler_log(device.logPath, 'Step : uninstall app : ' + package_name)
        command = 'adb -s ' + device.id + " uninstall " + package_name
        os.system(command)
        del device, package_name, command
    except Exception as e:
        Saver.save_crawler_log(device.logPath, str(e))
        del device, package_name
        Saver.save_crawler_log(device.logPath, 'uninstall app catch exception')


def app_is_installed(device, package_name):
    Saver.save_crawler_log(device.logPath, "Step : check app is installed or not")
    command = 'adb -s ' + device.id + " shell pm list package"
    result = os.popen(command)
    lines = result.readlines()
    for line in lines:
        if package_name in line and (package_name + '.') not in line:
            print "app is installed"
            del command, result, lines, device, line, package_name
            return True
        del line
    Saver.save_crawler_log(device.logPath, "app is not installed")
    del command, result, lines, device, package_name
    return False


def app_is_running(device, app):
    Saver.save_crawler_log(device.logPath, "Step : check app is running or not")
    command = "adb -s " + device.id + " shell top -n 1"
    output = os.popen(command)
    lines = output.readlines()
    for line in lines:
        if app.packageName in line:
            Saver.save_crawler_log(device.logPath, "app is running")
            del command, output, lines, device, app, line
            return True
        del line
    Saver.save_crawler_log(device.logPath, "app is not running")
    del command, output, lines, device, app
    return False


def clean_device_logcat(device):
    Saver.save_crawler_log(device.logPath, "Step : clean device logcat cache")
    command = 'adb -s ' + device.id + ' logcat -c'
    os.system(command)
    del device, command


def start_activity(device, packagename, activity):
    Saver.save_crawler_log(device.logPath, 'Step : start up activity : ' + activity)
    time1 = datetime.datetime.now()
    command = 'adb -s ' + device.id + ' shell am start -n ' + packagename + '/' + activity
    try:
        os.system(command)
        while True:
            start_activity_time = (datetime.datetime.now() - time1).seconds
            if start_activity_time < 10:
                top_activity_info = pageController.get_top_activity_info(device)
                top_packagename = top_activity_info['packagename']
                top_activity = top_activity_info['activity']
                if top_packagename == packagename and top_activity == activity:
                    Saver.save_crawler_log(device.logPath, 'use time : ' + str(start_activity_time) + ' seconds')
                    del top_activity_info, top_packagename, top_activity
                    return True
                del top_activity_info, top_packagename, top_activity
            else:
                break
            del start_activity_time
        del device, packagename, activity, time1, command
        return False
    except Exception as e:
        Saver.save_crawler_log(device.logPath, str(e))
        del device, packagename, activity, e, time1, command
        return False


def kill_app(app):
    command = 'adb shell am force-stop ' + app.packageName
    os.system(command)
    del command, app


def drag_screen_to_left(device):
    Saver.save_crawler_log(device.logPath, "Step : drag screen to left")
    # x_max = str(int(device.screenResolution[0]) - 50)
    # x_min = str(int(resolution[0]) * 0.5)[:str(int(resolution[0]) * 0.5).index('.')]
    # command = 'adb -s ' + device.id + ' shell input swipe ' + x_max + ' 100 ' + '20' + ' 100'
    command = 'adb -s ' + device.id + ' shell input keyevent 22'
    os.system(command)
    del command, device


def drag_screen_to_right(device):
    Saver.save_crawler_log(device.logPath, "Step : drag screen to right")
    command = 'adb -s ' + device.id + ' shell input keyevent 21'
    os.system(command)
    del command, device


def click_back(device):
    Saver.save_crawler_log(device.logPath, "Step : click back btn on device")
    command = 'adb -s ' + device.id + ' shell input keyevent 4'
    os.system(command)
    del command, device


def click_point(device, x_point, y_point):
    command = 'adb -s ' + device.id + ' shell input tap ' + x_point + ' ' + y_point
    Saver.save_crawler_log(device.logPath, 'click screen :' + x_point + ',' + y_point)
    os.system(command)
    del command, device, x_point, y_point


def long_click_point(device, x, y):
    command = 'adb -s' + device.id + 'shell input swipe ' + x + ' ' + y + ' ' + x + ' ' + y + ' 1000'
    Saver.save_crawler_log(device.logPath, 'long click screen :' + x + ',' + y)
    os.system(command)
    del device, x, y, command


def keyboard_is_shown(device):
    Saver.save_crawler_log(device.logPath, "Step : check keyboard")
    command = 'adb -s ' + device.id + ' shell dumpsys input_method'
    result = os.popen(command).read()
    key = 'mInputShown='
    keyboard_status = result[result.index(key) + len(key):result.index(key) + len(key) + 5]
    if 'true' in keyboard_status:
        Saver.save_crawler_log(device.logPath, "keyboard is shown ")
        del device, command, result, key, keyboard_status
        return True
    else:
        Saver.save_crawler_log(device.logPath, "keyboard is not shown")
        del device, command, result, key, keyboard_status
        return False


def close_sys_alert(plan, app, device, page_now):
    if page_now is None:
        return page_now
    for node in page_now.clickableNodes:
        info = [node.package, node.resource_id, node.text]
        if info in Setting.AuthorizationAlert:
            Saver.save_crawler_log(device.logPath, "Step : close sys alert")
            device.save_screen(node, False)
            tap_node(device, node)
            page_now = pageController.get_page_info(plan, app, device)
    del plan, app, device
    return page_now


def tap_node(device, node):
    Saver.save_crawler_log(device.logPath, "tap node ")
    location = node.location
    click_point(device, location[0], location[1])
    node.update_operation('tap')
    del location, device, node


def long_click_node(device, node):
    Saver.save_crawler_log(device.logPath, "long click node")
    location = node.location
    long_click_point(device, location[0], location[1])
    node.update_operation('longclick')
    del device, node, location


def get_random_text(length):
    text = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    for i in range(length):
        text += chars[random.randint(0, len(chars) - 1)]
    del length, chars
    return text


def type_text(device, edittext, text):
    Saver.save_crawler_log(device.logPath, "type : " + text)
    tap_node(device, edittext)
    command = 'adb -s ' + device.id + ' shell input text ' + text
    os.system(command)
    edittext.update_operation('type')
    del device, edittext, text, command
