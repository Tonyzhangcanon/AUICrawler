# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#  - * Plan Setting * -
SaveScreen = False  # True ， False
SaveJumpOutScreen = False  # True , False
KeepRun = True  # True (Resume run when app Crash), False (Finish run when app Crash)

#  - * Crawl model* -
TimeModel = 'Normal'  # Limit (Exp crawl in 5 minutes ) , Normal
LimitTime = 15  # minutes . (set the crawl time)
CrawlModel = 'Normal'  # Random (crawl in random) ， Normal ， Activity (crawl all activities)
CoverageLevel = 1  # 0 < level <= 1 , Exp level = 0.6 , if there are 10 points in one page , coverage click 6 points .

#  - * Apk Install Setting * -
UnInstallApk = True  # True (uninstall app & testApp) , False
InstallApk = True  # True (install app & testApp) ,False
ApkPath = '/Users/admin/Downloads/Kuaiya-china-debug.apk'
TestApkPath = '/Users/admin/Downloads/Kuaiya-china-debug-androidTest.apk'

#  - * App Info Setting * -
AppMainActivity = {'com.dewmobile.kuaiya.debug': 'com.dewmobile.kuaiya.act.MainActivity',
                   'com.dewmobile.groupshare': 'com.dewmobile.kuaiya.act.MainActivity',
                   'packageName': 'MainActivity'}

FirstClickViews = {
    'com.dewmobile.kuaiya.debug': ['iv_transfer_to', 'guide_i_know', 'ok', 'edit_ok', 'button1', 'f1', 'l6', 'a2s'],
    'com.dewmobile.groupshare': ['iv_transfer_to', 'guide_i_know', 'ok', 'edit_ok', 'button1', 'iv_back'],
    'packageName': ['FirstClickView-1-id', 'FirstClickView-2-id']}

BackBtnViews = {
    'com.dewmobile.kuaiya.debug': ['back', 'iv_title_left', 'back_iv', 'iv_btn_back', 'iv_back', 'transfer_title_back',
                                   'c1', 'cu', 'ake', 'a2b'],
    'com.dewmobile.groupshare': ['back', 'iv_title_left', 'back_iv', 'iv_btn_back', 'iv_back'],

    'packageName': ['View-1-id', 'View-2-id']}  # finally tap in the page

UnCrawlViews = {'com.dewmobile.kuaiya.debug': {'view1-id': 'id', 'view2-text': 'text'},
                'com.dewmobile.groupshare': {'view1-id': 'id'},
                'packageName': {'view1-id': 'id', 'view2-text': 'text'}}

AuthorizationAlert = [['com.huawei.systemmanager', 'com.huawei.systemmanager:id/btn_allow', '允许']]

#  - * Run Init Robotium Case Setting * -
RunInitNodes = True  # True (run init nodes before run init Robotium Case) , False
RunInitCase = False  # True (run init Robotium case) , False
InitCases = {'com.dewmobile.kuaiya.debug': ['com.dewmobile.kuaiya.test.cases.host.initcase.RunGuidePage'],
             'packageName': ['case1', 'case2']}
TestRunner = 'com.android.test.runner.MultiDexTestRunner'

#  - * Login Setting * -
Login = True  # True (if crawl to the loginActivity, login & continue crawl)
AppLoginActivity = {'com.dewmobile.kuaiya.debug': 'com.dewmobile.kuaiya.es.ui.activity.LoginActivity',
                    'com.dewmobile.groupshare': 'com.dewmobile.kuaiya.es.ui.activity.LoginActivity',
                    'packageName': 'loginActivity'}

LoginViewList = {'com.dewmobile.kuaiya.debug': ['uk', 'um', 'up'],
                 'com.dewmobile.groupshare': ['username', 'password', 'btn_login'],
                 'packageName': ['AccountViewID', 'PasswordViewID', 'LoginBtnId']}

AccountList = {
    'com.dewmobile.kuaiya.debug': [['15600900870', '123456'], ['15210614522', '123456'], ['18600500279', '11111111'],
                                   ['13363167097', '123456']],
    'com.dewmobile.groupshare': [['13363167097', '123456'], ['15210614522', '123456']],
    'packageName': [['account1', 'password1'], ['account2', 'password2']]}

#  - * send crawl result email * -
SMTP_HOST = "smtp.dewmobile.net"  # Set mail smtp host
Mail_To_List = ["quality@dewmobile.net"]  # who will receive the result mail "quality@dewmobile.net"
Mail_User = "zhiyang.zhang@dewmobile.net"  # which account will be Use to send mail
Mail_Pass = "Tony546355"  # the password for login
