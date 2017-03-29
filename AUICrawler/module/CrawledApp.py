# -*- coding:utf-8 -*-
import os
from script import Saver
from config import Setting
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


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

        self.mainActivity = Setting.AppMainActivity
        Saver.save_crawler_log(plan.logPath, 'MainActivity : ' + self.mainActivity)

        self.loginActivity = Setting.AppLoginActivity
        Saver.save_crawler_log(plan.logPath, 'LoginActivity : ' + self.mainActivity)

        self.testApkPath = Setting.TestApkPath
        Saver.save_crawler_log(plan.logPath, 'Test Apk Path : ' + self.testApkPath)

        self.testPackageName = self.get_package_name(self.testApkPath)
        Saver.save_crawler_log(plan.logPath, 'Test Apk PackageName : ' + self.testPackageName)

        self.initCasesList = Setting.InitCases
        Saver.save_crawler_log(plan.logPath, 'InitCaseList : ' + str(self.initCasesList))

        self.firstClickViews = self.get_view_list(Setting.FirstClickViews)
        Saver.save_crawler_log(plan.logPath, 'FirstClickViews : ' + str(self.firstClickViews))

        self.backBtnViews = self.get_view_list(Setting.BackBtnViews)
        Saver.save_crawler_log(plan.logPath, 'BackBtnViews : ' + str(self.backBtnViews))

        self.unCrawlViews = self.get_unCrawlViews()
        Saver.save_crawler_log(plan.logPath, 'UnClickViews : ' + str(self.unCrawlViews))

        self.loginViews = self.get_view_list(Setting.LoginViewList)
        Saver.save_crawler_log(plan.logPath, 'LoginViews : ' + str(self.loginViews))

        self.testRunner = Setting.TestRunner
        Saver.save_crawler_log(plan.logPath, 'TestRunner : ' + self.testRunner)

        self.activities = self.get_all_activities()

        self.activityNum = str(len(self.activities))

    def get_view_list(self, id_list):
        views = []
        if len(id_list) != 0:
            for id in id_list:
                resource_id = self.packageName + ':id/' + id
                views.append(resource_id)
        return views

    def get_unCrawlViews(self):
        unCrawlViews = []
        for key, value in Setting.UnCrawlViews.items():
            if key == 'id':
                resource_id = self.packageName + ':id/' + value
                unCrawlViews.append(resource_id)
            if key == 'text':
                unCrawlViews.append(value)
        return unCrawlViews

    def get_app_name(self):
        try:
            command = 'aapt dump badging ' + self.apkPath
            result = os.popen(command).readlines()
            for line in result:
                name_head = "application-label-zh-CN:'"
                if name_head in line:
                    name = line[line.index(name_head) + len(name_head):len(line)-2]
                    return name
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
                    return package_name
        except:
            return ""

    def get_version_code(self):
        command = 'aapt dump badging ' + self.apkPath
        result = os.popen(command).readlines()
        for line in result:
            version_code_head = "versionCode='"
            end = "' "
            if version_code_head in line:
                line = line[line.index(version_code_head) + len(version_code_head):]
                version_code = line[:line.index(end)]
                return version_code

    def get_version_name(self):
        command = 'aapt dump badging ' + self.apkPath
        result = os.popen(command).readlines()
        for line in result:
            version_name_head = "versionName='"
            end = "' "
            if version_name_head in line:
                line = line[line.index(version_name_head) + len(version_name_head):]
                version_name = line[:line.index(end)]
                return version_name

    def get_launcher_activity(self):
        command = 'aapt dump badging ' + self.apkPath
        result = os.popen(command).readlines()
        for line in result:
            activity_head = "launchable-activity: name='"
            end = "' "
            if activity_head in line:
                activity_name = line[line.index(activity_head) + len(activity_head):line.index(end)]
                return activity_name

    def get_all_activities(self):
        activity_list = []
        command = 'aapt dump xmlstrings ' + self.apkPath + ' AndroidManifest.xml'
        result = os.popen(command).readlines()
        for line in result:
            if 'Activity' in line:
                index = line.index(': ')
                activity = line[index+len(': '):len(line) - 1]
                if activity != self.launcherActivity and activity not in activity_list:
                    activity_list.append(activity)
        return activity_list
