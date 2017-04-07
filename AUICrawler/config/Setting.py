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
ApkPath = '/Users/admin/Downloads/xxxxxxx.apk'
TestApkPath = '/Users/admin/Downloads/xxxxx-androidTest.apk'


#  - * App Info Setting * -
AppMainActivity = {'com.xxx.xxx': 'com.xxx.MainActivity',
                   'com.xxxx.xxx': 'com.xxxx.MainActivity',
                   'packageName': 'MainActivity'}

FirstClickViews = {'com.xxx.xxx': ['iv_transfer_to', 'guide_i_know', 'ok', 'edit_ok', 'button1', 'iv_back'],
                   'packageName': ['FirstClickView-1-id', 'FirstClickView-2-id']}

BackBtnViews = {'com.xxx.xxx': ['back', 'iv_title_left', 'back_iv', 'iv_btn_back', 'iv_back'],
                'packageName': ['View-1-id', 'View-2-id']}  # finally tap in the page

UnCrawlViews = {'com.xxxx.xxx': {'view1-id': 'id', 'view2-text': 'text'},
                'packageName': {'view1-id': 'id', 'view2-text': 'text'}}

AuthorizationAlert = [['com.huawei.systemmanager', 'com.huawei.systemmanager:id/btn_allow', '允许']]


#  - * Run Init Robotium Case Setting * -
RunInitNodes = True  # True (run init nodes before run init Robotium Case) , False
RunInitCase = False  # True (run init Robotium case) , False
InitCases = {'com.xxxx.xxxx': ['com.xxxx.xxxx.cases.xxxx'],
             'packageName': ['case1', 'case2']}
TestRunner = 'com.android.test.runner.MultiDexTestRunner'

#  - * Login Setting * -
Login = True  # True (if crawl to the loginActivity, login & continue crawl)
AppLoginActivity = {'com.xxx.xxx': 'com.xxx.LoginActivity',
                    'packageName': 'loginActivity'}

LoginViewList = {'com.xxx.xxx': ['username', 'password', 'btn_login'],
                 'packageName': ['AccountViewID', 'PasswordViewID', 'LoginBtnId']}

AccountList = {'com.xxx.xxx': [['xxxxx', 'xxxxxx'], ['xxxxx', 'xxxxx']],
               'packageName': [['account1', 'password1'], ['account2', 'password2']]}

#  - * send crawl result email * -
SMTP_HOST = "smtp.xxx.net"  # Set mail smtp host
Mail_To_List = ["xxx.xxx@xxx.net"]  # who will receive the result mail
Mail_User = "xxx.xxx@xxx.net"  # which account will be Use to send mail
Mail_Pass = "xxxxxx"  # the password for login
