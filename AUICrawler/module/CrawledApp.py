# -*- coding:utf-8 -*-
import os
from AUICrawler.script import SaveLog
from AUICrawler.script import Setting
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class App:
    def __init__(self, plan):
        SaveLog.save_crawler_log(plan.logPath, "Step : Init App ...")

        self.apkPath = Setting.ApkPath
        SaveLog.save_crawler_log(plan.logPath, 'Apk Path : ' + self.apkPath)

        self.versionCode = self.get_version_code()
        SaveLog.save_crawler_log(plan.logPath, 'VersionCode : ' + self.versionCode)

        self.versionName = self.get_version_name()
        SaveLog.save_crawler_log(plan.logPath, 'VersionName : ' + self.versionName)

        self.packageName = self.get_package_name(self.apkPath)
        SaveLog.save_crawler_log(plan.logPath, 'PackageName : ' + self.packageName)

        self.launcherActivity = self.get_launcher_activity()
        SaveLog.save_crawler_log(plan.logPath, 'LauncherActivity : ' + self.launcherActivity)

        self.mainActivity = Setting.AppMainActivity
        SaveLog.save_crawler_log(plan.logPath, 'MainActivity : ' + self.mainActivity)

        self.testApkPath = Setting.TestApkPath
        SaveLog.save_crawler_log(plan.logPath, 'Test Apk Path : ' + self.testApkPath)

        self.testPackageName = self.get_package_name(self.testApkPath)
        SaveLog.save_crawler_log(plan.logPath, 'Test Apk PackageName : ' + self.testPackageName)

        self.initCasesList = Setting.InitCases
        SaveLog.save_crawler_log(plan.logPath, 'InitCaseList : ' + str(self.initCasesList))

        self.firstClickViews = self.get_view_list(Setting.FirstClickViews)
        SaveLog.save_crawler_log(plan.logPath, 'FirstClickViews : ' + str(self.firstClickViews))

        self.backBtnViews = self.get_view_list(Setting.BackBtnViews)
        SaveLog.save_crawler_log(plan.logPath, 'BackBtnViews : ' + str(self.backBtnViews))

        self.unClickViews = self.get_view_list(Setting.UnClickViews)
        SaveLog.save_crawler_log(plan.logPath, 'UnClickViews : ' + str(self.unClickViews))

        self.testRunner = Setting.TestRunner
        SaveLog.save_crawler_log(plan.logPath, 'TestRunner : ' + self.testRunner)

    def get_view_list(self, id_list):
        views = []
        if len(id_list) != 0:
            for id in id_list:
                resource_id = self.packageName + ':id/' + id
                views.append(resource_id)
        return views

    @staticmethod
    def get_package_name(apk_path):
        command = 'aapt dump badging ' + apk_path
        result = os.popen(command).readlines()
        for line in result:
            package_head = "package: name='"
            end = "' "
            if package_head in line:
                package_name = line[line.index(package_head) + len(package_head):line.index(end)]
                return package_name

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
