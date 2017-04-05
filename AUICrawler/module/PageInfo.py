# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Page:
    def __init__(self):
        self.nodesList = []
        self.nodesInfoList = []
        self.nodesNum = 0
        self.clickableNodes = []
        self.clickableNodesNum = 0
        self.scrollableNodes = []
        self.scrollableNodesNum = 0
        self.longClickableNodes = []
        self.longClickableNodesNum = 0
        self.editTexts = []
        self.editTextsNum = 0
        self.backBtn = None
        self.currentActivity = ''
        self.package = ''
        self.entry = []
        self.entryNum = 0
        self.lastPage = None
        self.lastPageNum = 0

    def add_node(self, device, app, node):
        self.nodesList.append(node)
        if node is not None and node.bounds != '[0,0][0,0]':
            self.nodesList.append(node)
            self.nodesInfoList.append(node.nodeInfo)
            self.nodesNum += 1
            if not device.is_in_hascrawled_nodes(node.nodeInfo) \
                    and not device.is_in_uncrawled_nodes(node.nodeInfo) \
                    and not self.has_added(node.nodeInfo) \
                    and node.resource_id not in app.unCrawlViews \
                    and node.text not in app.unCrawlViews:
                if len(self.currentActivity) == 0:
                    self.currentActivity = node.currentActivity
                    self.package = node.package
                if node.resource_id in app.backBtnViews:
                    self.backBtn = node
                elif node.isEditText:
                    self.editTexts.append(node)
                    self.editTextsNum += 1
                else:
                    if (node.clickable == 'true' or node.checkable == 'true') and not node.isEditText:
                        self.clickableNodes.append(node)
                        self.clickableNodesNum += 1
                    if node.scrollable == 'true':
                        self.scrollableNodes.append(node)
                        self.scrollableNodesNum += 1
                    if node.longClickable == 'true':
                        self.longClickableNodes.append(node)
                        self.longClickableNodesNum += 1
        del device, app, node

    def update_back_btn(self, back_btn_node):
        if back_btn_node is not None:
            self.backBtn = back_btn_node
        del back_btn_node

    def remove_clickable_node(self, node):
        if node in self.clickableNodes:
            self.clickableNodes.remove(node)
            self.clickableNodesNum -= 1
        del node

    def remove_scrollable_node(self, node):
        if node in self.scrollableNodes:
            self.scrollableNodes.remove(node)
            self.scrollableNodesNum -= 1
        del node

    def remove_longclickable_node(self, node):
        if node in self.longClickableNodes:
            self.longClickableNodes.remove(node)
            self.longClickableNodesNum -= 1
        del node

    def remove_edit_text(self, node):
        if node in self.editTexts:
            self.editTexts.remove(node)
            self.editTextsNum -= 1
        del node

    def add_entry(self, node):
        self.entry.insert(0, node)
        self.entryNum += 1
        del node

    def add_last_page(self, page):
        self.lastPage = page
        self.lastPageNum += 1
        del page

    def has_added(self, node_info):
        for node in self.clickableNodes:
            if node.nodeInfo == node_info:
                del node_info
                return True
        for node in self.scrollableNodes:
            if node.nodeInfo == node_info:
                del node_info
                return True
        for node in self.longClickableNodes:
            if node.nodeInfo == node_info:
                del node_info
                return True
        for node in self.editTexts:
            if node.nodeInfo == node_info:
                del node_info
                return True

