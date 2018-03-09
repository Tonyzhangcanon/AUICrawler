# -*- coding:utf-8 -*-
import os
from script import Saver
from config import Setting


class App:
    def __init__(self, plan):
        Saver.save_crawler_log(plan.logPath, "Step : Init App ...")

        self.apkPath = Setting.ApkPath
        Saver.save_crawler_log(plan.logPath, 'Apk Path : ' + self.apkPath)

        self.appName = self.get_app_name(plan)
        Saver.save_crawler_log(plan.logPath, 'App Name : ' + self.appName)

        self.versionCode = self.get_version_code(plan)
        Saver.save_crawler_log(plan.logPath, 'VersionCode : ' + self.versionCode)

        self.versionName = self.get_version_name(plan)
        Saver.save_crawler_log(plan.logPath, 'VersionName : ' + self.versionName)

        self.packageName = self.get_package_name(plan, self.apkPath)
        Saver.save_crawler_log(plan.logPath, 'PackageName : ' + self.packageName)

        self.launcherActivity = self.get_launcher_activity(plan)
        Saver.save_crawler_log(plan.logPath, 'LauncherActivity : ' + self.launcherActivity)

        self.mainActivity = self.get_main_activity(plan)
        Saver.save_crawler_log(plan.logPath, 'MainActivity : ' + self.mainActivity)

        self.loginActivity = self.get_login_activity(plan)
        Saver.save_crawler_log(plan.logPath, 'LoginActivity : ' + self.loginActivity)

        self.testApkPath = Setting.TestApkPath
        Saver.save_crawler_log(plan.logPath, 'Test Apk Path : ' + self.testApkPath)

        self.testPackageName = self.get_package_name(plan, self.testApkPath)
        Saver.save_crawler_log(plan.logPath, 'Test Apk PackageName : ' + self.testPackageName)

        self.initCasesList = self.get_init_cases(plan)
        Saver.save_crawler_log(plan.logPath, 'InitCaseList : ' + str(self.initCasesList))

        self.firstClickViews = self.get_view_list(plan, Setting.FirstClickViews)
        Saver.save_crawler_log(plan.logPath, 'FirstClickViews : ' + str(self.firstClickViews))

        self.backBtnViews = self.get_view_list(plan, Setting.BackBtnViews)
        Saver.save_crawler_log(plan.logPath, 'BackBtnViews : ' + str(self.backBtnViews))

        self.unCrawlViews = self.get_unCrawlViews(plan)
        Saver.save_crawler_log(plan.logPath, 'UnCrawlViews : ' + str(self.unCrawlViews))

        self.loginViews = self.get_view_list(plan, Setting.LoginViewList)
        Saver.save_crawler_log(plan.logPath, 'LoginViews : ' + str(self.loginViews))

        self.loginActivityEntry = None

        self.testRunner = Setting.TestRunner
        Saver.save_crawler_log(plan.logPath, 'TestRunner : ' + self.testRunner)

        self.activities = self.get_all_activities(plan)

        self.activityNum = str(len(self.activities))
        Saver.save_crawler_log(plan.logPath, 'Activity num : ' + self.activityNum)

    def get_view_list(self, plan, id_dict):
        try:
            id_list = id_dict[self.packageName]
            views = []
            if len(id_list) != 0:
                for device_id in id_list:
                    resource_id = self.packageName + ':id/' + device_id
                    views.append(resource_id)
                    del resource_id
            del id_list, plan
            return views
        except Exception as e:
            Saver.save_crawler_log(plan.logPath, str(e))
            del id_dict, e, plan
            return []

    def get_unCrawlViews(self, plan):
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
        except Exception as e:
            Saver.save_crawler_log(plan.logPath, str(e))
            del plan, e
            return []

    def get_app_name(self, plan):
        try:
            command = 'aapt dump badging ' + self.apkPath
            result = os.popen(command).readlines()
            for line in result:
                name_head = "application-label-zh-CN:'"
                if name_head in line:
                    name = line[line.index(name_head) + len(name_head):len(line) - 2]
                    del plan, name_head
                    return name
                del line
            del plan, command, result
            return ''
        except Exception as e:
            Saver.save_crawler_log(plan.logPath, str(e))
            del plan, e
            return ""

    @staticmethod
    def get_package_name(plan, apk_path):
        try:
            command = 'aapt dump badging ' + apk_path
            result = os.popen(command).readlines()
            end = "' "
            package_head = "package: name='"
            for line in result:
                if package_head in line:
                    package_name = line[line.index(package_head) + len(package_head):line.index(end)]
                    del command, result, package_head, end, apk_path, line
                    return package_name
                del line
            del command, result, apk_path, end, package_head
            return ''
        except Exception as e:
            Saver.save_crawler_log(plan.logPath, str(e))
            del apk_path, e
            return ""

    def get_version_code(self, plan):
        try:
            command = 'aapt dump badging ' + self.apkPath
            result = os.popen(command).readlines()
            version_code_head = "versionCode='"
            end = "' "
            for line in result:
                if version_code_head in line:
                    line = line[line.index(version_code_head) + len(version_code_head):]
                    version_code = line[:line.index(end)]
                    del plan, command, result, version_code_head, end, line
                    return version_code
                del line
            del plan, command, result, version_code_head, end
            return ''
        except Exception as e:
            Saver.save_crawler_log(plan.logPath, str(e))
            del plan, e
            return ''

    def get_version_name(self, plan):
        try:
            command = 'aapt dump badging ' + self.apkPath
            result = os.popen(command).readlines()
            version_name_head = "versionName='"
            end = "' "
            for line in result:
                if version_name_head in line:
                    line = line[line.index(version_name_head) + len(version_name_head):]
                    version_name = line[:line.index(end)]
                    del plan, command, result, line, version_name_head, end
                    return version_name
                del line
            del plan, command, result, version_name_head, end
            return ''
        except Exception as e:
            Saver.save_crawler_log(plan.logPath, str(e))
            del plan, e
            return ''

    def get_launcher_activity(self, plan):
        try:
            command = 'aapt dump badging ' + self.apkPath
            result = os.popen(command).readlines()
            activity_head = "launchable-activity: name='"
            end = "' "
            for line in result:
                if activity_head in line:
                    activity_name = line[line.index(activity_head) + len(activity_head):line.index(end)]
                    del plan, command, result, line, activity_head, end
                    return activity_name
            del plan, command, result, activity_head, end
            return ''
        except Exception as e:
            Saver.save_crawler_log(plan.logPath, str(e))
            del plan, e
            return ''

    def get_main_activity(self, plan):
        try:
            main_activity = Setting.AppMainActivity[self.packageName]
            del plan
            return main_activity
        except Exception as e:
            Saver.save_crawler_log(plan.logPath, str(e))
            del plan, e
            return ''

    def get_login_activity(self, plan):
        try:
            login_activity = Setting.AppLoginActivity[self.packageName]
            del plan
            return login_activity
        except Exception as e:
            Saver.save_crawler_log(plan.logPath, str(e))
            del plan, e
            return ''

    def get_all_activities(self, plan):
        try:
            activity_list = []
            command = 'aapt dump xmlstrings ' + self.apkPath + ' AndroidManifest.xml'
            result = os.popen(command).readlines()
            for line in result:
                if 'Activity' in line:
                    index = line.index(': ')
                    activity = line[index + len(': '):len(line) - 1]
                    if activity != self.launcherActivity and activity not in activity_list:
                        activity_list.append(activity)
                    del index, activity
                del line
            del plan, command, result
            return activity_list
        except Exception as e:
            Saver.save_crawler_log(plan.logPath, str(e))
            del plan, e
            return []

    def get_init_cases(self, plan):
        try:
            init_cases = Setting.InitCases[self.packageName]
            del plan
            return init_cases
        except Exception as e:
            Saver.save_crawler_log(plan.logPath, str(e))
            del e, plan
            return []

    def update_loginactivity_entry(self, node):
        self.loginActivityEntry = node
        del node
