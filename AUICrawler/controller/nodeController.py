# -*- coding:utf-8 -*-

import random
from script import Saver
from config import Setting
import appController
import pageController


def find_node_by_info(app, classname, resourceid, contentdesc, page):
    result = False
    for node in page.nodesList:
        if node.package == app.packageName \
                and node.className == classname \
                and node.resource_id == resourceid \
                and contentdesc == contentdesc:
            result = True
            break
        del node
    del app, classname, resourceid, contentdesc, page
    return result


def get_node_by_id(page, resource_id):
    for node in page.nodesList:
        if node.resource_id == resource_id:
            del page, resource_id
            return node
        del node


def node_is_shown_in_page(device, node, page):
    if node in page.nodesList:
        Saver.save_crawler_log(device.logPath, "node is shown in page now")
        del device, node, page
        return True
    else:
        Saver.save_crawler_log(device.logPath, "node is not shown in page now")
        del device, node, page
        return False


def get_node_recover_way(app, device, page_now, page_before_run, node, way):
    Saver.save_crawler_log(device.logPath, "Step : get node recover way ,node info : " + str(node.nodeInfo))
    way_this_deep = way
    result = False
    if page_before_run is not None and page_before_run.entryNum != 0:
        entry = page_before_run.entry
        if entry is app.loginActivityEntry:
            Saver.save_crawler_log(device.logPath, "node shown because login , can't find the way . ")
            result = True
        else:
            Saver.save_crawler_log(device.logPath, entry.resource_id)
            if page_now is not None and entry.nodeInfo in page_now.nodesInfoList:
                way_this_deep.insert(0, entry)
                node.update_recover_way(way_this_deep)
                Saver.save_crawler_log(device.logPath, "get the node recover way success. ")
                Saver.save_crawler_log(device.logPath, str(way_this_deep))
                result = True
    if not result:
        if page_before_run is not None and page_before_run.lastPageNum != 0:
            p = page_before_run.lastPage
            entry = page_before_run.entry
            Saver.save_crawler_log(device.logPath, entry.resource_id)
            way_this_deep.insert(0, entry)
            result = get_node_recover_way(app, device, page_now, p, node, way_this_deep)
    if result:
        del device, page_now, page_before_run, node, way, way_this_deep
        return True
    else:
        Saver.save_crawler_log(device.logPath, "get the node recover way false. ")
        del device, page_now, page_before_run, node, way, way_this_deep
        return False


def recover_node_shown(plan, app, device, page_now, page_before_run, node):
    t = 1
    if node.nodeInfo in page_now.nodesInfoList:
        return True
    else:
        r = False
    while page_now is not None and page_now.nodesNum != 0 and node.nodeInfo not in page_now.nodesInfoList:
        if get_node_recover_way(app, device, page_now, page_before_run, node, []):
            r = True
            break
        Saver.save_crawler_log(device.logPath, "Step : no recover way , click back")
        device.save_screen_jump_out(page_now.package, page_now.currentActivity)
        appController.click_back(device)
        page_now = pageController.get_page_info(plan, app, device)
        t += 1
        if t > 2:
            Saver.save_crawler_log(device.logPath, "can't find the node after back 3 times.")
            try:
                appController.start_activity(device,app.packageName,page_now.currentActivity)
            except:
                appController.start_activity(device,app.packageName,app.mainActivity)
            page_now = pageController.get_page_info(plan, app, device)
        if t > 3:
            Saver.save_crawler_log(device.logPath, "can't find the node after restart app")
            break
    if r:
        Saver.save_crawler_log(device.logPath, "Step : recover node shown")
        for n in node.recoverWay:
            device.save_screen(n, False)
            if n.crawlOperation == 'tap':
                appController.tap_node(device, n)
            elif n.crawlOperation == 'longclick':
                appController.long_click_node(device, n)
            elif n.crawlOperation == 'type':
                s = appController.get_random_text(8)
                appController.type_text(device, n, s)
                del s
            page_now = pageController.check_page_after_operation(plan, app, device, page_before_run, node)
            del n
        if node.nodeInfo in page_now.nodesInfoList:
            del plan, app, device, page_now, page_before_run, node, t
            return True
    del plan, app, device, page_now, page_before_run, node, t
    return r


def get_random_nodes(nodes_list):
    if Setting.CrawlModel == 'Normal':
        return nodes_list
    else:
        if len(nodes_list) * float(Setting.CoverageLevel) < 1:
            num = 1
        else:
            num = int(len(nodes_list) * float(Setting.CoverageLevel))
        return random.sample(nodes_list, num)
