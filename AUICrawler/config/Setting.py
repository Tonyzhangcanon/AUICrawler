# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#  - * Plan Setting * -
SaveScreen = False  # True ， False
SaveJumpOutScreen = False  # True , False
KeepRun = False  # True (Resume run when app Crash), False (Finish run when app Crash)

#  - * Crawl model* -
TimeModel = 'Normal'  # Limit (Exp crawl in 5 minutes ) , Normal
LimitTime = 15  # minutes . (set the crawl time)
CrawlModel = 'Normal'  # Random (crawl in random) ， Normal ， Activity (crawl all activities)
CoverageLevel = 1  # 0 < level <= 1 , Exp level = 0.6 , if there are 10 points in one page , coverage click 6 points .

#  - * Apk Install Setting * -
UnInstallApk = False  # True (uninstall app & testApp) , False
InstallApk = False  # True (install app & testApp) ,False
ApkPath = '/Users/admin/Downloads/xxxxx.apk'
TestApkPath = '/Users/admin/Downloads/xxxx-china-debug-androidTest.apk'

#  - * App Info Setting * -
AppMainActivity = 'com.xxxxx.MainActivity'
FirstClickViews = ['iv_transfer_to', 'guide_i_know', 'ok', 'edit_ok', 'button1', 'iv_back']
BackBtnViews = ['back', 'iv_title_left', 'back_iv', 'iv_btn_back', 'iv_back']  # finally tap in the page
UnCrawlViews = {'id': 'play_click',
                'id': 'fullscreen',
                'text': u'我的'}
AuthorizationAlert = [['com.huawei.systemmanager', 'com.huawei.systemmanager:id/btn_allow', '允许']]

#  - * Run Init Robotium Case Setting * -
RunInitNodes = False  # True (run init nodes before run init Robotium Case) , False
RunInitCase = False  # True (run init Robotium case) , False
InitCases = ['com.xxxxxxx.initcase.RunGuidePage']
TestRunner = 'com.android.test.runner.MultiDexTestRunner'

#  - * Login Setting * -
Login = False  # True (if crawl to the loginActivity, login & continue crawl)
AppLoginActivity = 'com.xxxxxx.LoginActivity'
LoginViewList = ['username', 'password', 'btn_login']  # [AccountViewID, PasswordViewID, LoginBtnId]
AccountList = [['xxxx', 'xxxx'],
               ['xxxx', 'xxx']]

#  - * send crawl result email * -
SMTP_HOST = "smtp.xxxx.com"  # Set mail smtp host
Mail_To_List = ["xxxxx@xxx.com", "xxxxx@xxx.com"]  # who will receive the result mail
Mail_User = "xxxxx@xxxx.com"  # which account will be Use to send mail
Mail_Pass = "******"  # the password for login
