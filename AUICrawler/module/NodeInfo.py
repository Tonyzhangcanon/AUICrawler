# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Node:
    def __init__(self, node):
        # get node detail by dump
        self.index = node.getAttribute('index')
        self.text = node.getAttribute('text').decode('utf-8')
        self.resource_id = node.getAttribute('resource-id')
        self.className = node.getAttribute('class')
        self.package = node.getAttribute('package')
        self.content_desc = node.getAttribute('content-desc').decode('utf-8')
        self.checkable = node.getAttribute('checkable')
        self.checked = node.getAttribute('checked')
        self.clickable = node.getAttribute('clickable')
        self.enabled = node.getAttribute('enabled')
        self.focusable = node.getAttribute('focusable')
        self.focused = node.getAttribute('focused')
        self.scrollable = node.getAttribute('scrollable')
        self.longClickable = node.getAttribute('long-clickable')
        self.password = node.getAttribute('passaword')
        self.selected = node.getAttribute('selected')
        self.bounds = self.get_node_bounds(node)

        self.location = self.get_node_location()

        # get CurrentActivity in running time
        self.currentActivity = ''

        # save the last click node , self is shown after click this last node
        # use to get recover way
        self.lastNode = self

        # save this in clicked nodes list
        # use it for check node has clicked or not before click
        self.nodeInfo = {'text': self.text,
                         'resource_id': self.resource_id,
                         'class': self.className,
                         'package': self.package,
                         'activity': self.currentActivity,
                         'checked': self.checked,
                         'selected': self.selected,
                         'bounds': self.bounds}

        self.isEditText = self.node_is_edittext()
        self.crawlOperation = ''

        self.recoverWay = []

    def node_is_edittext(self):
        if self.className == 'android.widget.EditText':
            return True
        else:
            return False

    @staticmethod
    def get_node_bounds(node):
        node_bounds = node.getAttribute('bounds')
        x_begin = int(node_bounds[node_bounds.find('[') + 1:node_bounds.find(',')])
        y_begin = int(node_bounds[node_bounds.find(',') + 1:node_bounds.find(']')])
        node_end = node_bounds[node_bounds.index(']') + 1:]
        x_end = int(node_end[node_end.find('[') + 1:node_end.find(',')])
        y_end = int(node_end[node_end.find(',') + 1:node_end.find(']')])
        bounds = [x_begin, y_begin, x_end, y_end]
        return bounds

    def get_node_location(self):
        location = []
        node_bounds = self.bounds
        x_begin = node_bounds[0]
        y_begin = node_bounds[1]
        x_end = node_bounds[2]
        y_end = node_bounds[3]
        x = (int(x_begin) + int(x_end)) / 2
        location.append(str(x))
        y = (int(y_begin) + int(y_end)) / 2
        location.append(str(y))
        return location

    def update_current_activity(self, activity):
        self.currentActivity = activity
        self.nodeInfo['activity'] = activity

    def update_last_node(self, node):
        self.lastNode = node

    def update_recover_way(self, way):
        self.recoverWay = way

    def clear_recover_way(self):
        self.recoverWay = []

    def update_operation(self, operation):
        self.crawlOperation = operation
