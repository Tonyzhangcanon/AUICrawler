# -*- coding:utf-8 -*-
import os
from script import Saver
from config import Setting


class App:
    def __init__(self, plan):
        Saver.save_crawler_log(plan.logPath, "Step : Init App ...")

        self.apkPath = Setting.ApkPath
        Saver.save_crawler_log(plan.logPath, 'Apk Path : ' + self.apkPath)

        self.appName = self.get_app_name()
        Saver.save_crawler_log(plan.logPath, 'App Name : ' + self.appName)

        self.versionCode = self.get_version_code()
        Saver.save_crawler_log(plan.logPath, 'VersionCode : ' + self.versionCode)

        self.versionName = self.get_version_name()
        Saver.save_crawler_log(plan.logPath, 'VersionName : ' + self.versionName)

        self.packageName = self.get_package_name(self.apkPath)
        Saver.save_crawler_log(plan.logPath, 'PackageName : ' + self.packageName)

        self.launcherActivity = self.get_launcher_activity()
        Saver.save_crawler_log(plan.logPath, 'LauncherActivity : ' + self.launcherActivity)

        self.mainActivity = self.get_main_activity()
        Saver.save_crawler_log(plan.logPath, 'MainActivity : ' + self.mainActivity)

        self.loginActivity = self.get_login_activity()
        Saver.save_crawler_log(plan.logPath, 'LoginActivity : ' + self.mainActivity)

        self.testApkPath = Setting.TestApkPath
        Saver.save_crawler_log(plan.logPath, 'Test Apk Path : ' + self.testApkPath)

        self.testPackageName = self.get_package_name(self.testApkPath)
        Saver.save_crawler_log(plan.logPath, 'Test Apk PackageName : ' + self.testPackageName)

        self.initCasesList = self.get_init_cases()
        Saver.save_crawler_log(plan.logPath, 'InitCaseList : ' + str(self.initCasesList))

        self.firstClickViews = self.get_view_list(Setting.FirstClickViews)
        Saver.save_crawler_log(plan.logPath, 'FirstClickViews : ' + str(self.firstClickViews))

        self.backBtnViews = self.get_view_list(Setting.BackBtnViews)
        Saver.save_crawler_log(plan.logPath, 'BackBtnViews : ' + str(self.backBtnViews))

        self.unCrawlViews = self.get_unCrawlViews()
        Saver.save_crawler_log(plan.logPath, 'UnCrawlViews : ' + str(self.unCrawlViews))

        self.loginViews = self.get_view_list(Setting.LoginViewList)
        Saver.save_crawler_log(plan.logPath, 'LoginViews : ' + str(self.loginViews))

        self.testRunner = Setting.TestRunner
        Saver.save_crawler_log(plan.logPath, 'TestRunner : ' + self.testRunner)

        self.activities = self.get_all_activities()

        self.activityNum = str(len(self.activities))

    def get_view_list(self, id_dict):
        try:
            id_list = id_dict[self.packageName]
            views = []
            if len(id_list) != 0:
                for device_id in id_list:
                    resource_id = self.packageName + ':id/' + device_id
                    views.append(resource_id)
                    del resource_id
            return views
        except:
            return []

    def get_unCrawlViews(self):
        try:
            unCrawlViews = []
            for key, value in Setting.UnCrawlViews[self.packageName].items():
                if value == 'id':
                    resource_id = self.packageName + ':id/' + key
                    unCrawlViews.append(resource_id)
                    del resource_id
                if value == 'text':
                    unCrawlViews.append(key)
                del key, value
            return unCrawlViews
        except:
            return []

    def get_app_name(self):
        try:
            command = 'aapt dump badging ' + self.apkPath
            result = os.popen(command).readlines()
            for line in result:
                name_head = "application-label-zh-CN:'"
                if name_head in line:
                    name = line[line.index(name_head) + len(name_head):len(line)-2]
                    del name_head
                    return name
                del line
            del command, result
            return ''
        except:
            return ""

    @staticmethod
    def get_package_name(apk_path):
        try:
            command = 'aapt dump badging ' + apk_path
            result = os.popen(command).readlines()
            for line in result:
                package_head = "package: name='"
                end = "' "
                if package_head in line:
                    package_name = line[line.index(package_head) + len(package_head):line.index(end)]
                    del command, result, package_head, end, apk_path
                    return package_name
            del command, result, apk_path
            return ''
        except:
            del apk_path
            return ""

    def get_version_code(self):
        try:
            command = 'aapt dump badging ' + self.apkPath
            result = os.popen(command).readlines()
            for line in result:
                version_code_head = "versionCode='"
                end = "' "
                if version_code_head in line:
                    line = line[line.index(version_code_head) + len(version_code_head):]
                    version_code = line[:line.index(end)]
                    del command, result, version_code_head, line
                    return version_code
            del command, result
            return ''
        except:
            return ''

    def get_version_name(self):
        try:
            command = 'aapt dump badging ' + self.apkPath
            result = os.popen(command).readlines()
            for line in result:
                version_name_head = "versionName='"
                end = "' "
                if version_name_head in line:
                    line = line[line.index(version_name_head) + len(version_name_head):]
                    version_name = line[:line.index(end)]
                    del command, result, line, version_name_head, end
                    return version_name
            del command, result
            return ''
        except:
            return ''

    def get_launcher_activity(self):
        try:
            command = 'aapt dump badging ' + self.apkPath
            result = os.popen(command).readlines()
            for line in result:
                activity_head = "launchable-activity: name='"
                end = "' "
                if activity_head in line:
                    activity_name = line[line.index(activity_head) + len(activity_head):line.index(end)]
                    del command, result, line, activity_head, end
                    return activity_name
            del command, result
            return ''
        except:
            return ''

    def get_main_activity(self):
        try:
            main_activity = Setting.AppMainActivity[self.packageName]
            return main_activity
        except:
            return ''

    def get_login_activity(self):
        try:
            login_activity = Setting.AppLoginActivity[self.packageName]
            return login_activity
        except:
            return ''

    def get_all_activities(self):
        try:
            activity_list = []
            command = 'aapt dump xmlstrings ' + self.apkPath + ' AndroidManifest.xml'
            result = os.popen(command).readlines()
            for line in result:
                if 'Activity' in line:
                    index = line.index(': ')
                    activity = line[index+len(': '):len(line) - 1]
                    if activity != self.launcherActivity and activity not in activity_list:
                        activity_list.append(activity)
                    del line, index, activity
            del command, result
            return activity_list
        except:
            return []

    def get_init_cases(self):
        try:
            init_cases = Setting.InitCases[self.packageName]
            return init_cases
        except:
            return []
