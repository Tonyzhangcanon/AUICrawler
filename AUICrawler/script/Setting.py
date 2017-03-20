# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#  - * Plan Setting * -
AppProduct = 1  # Exp : kuaiya:1 ,kuaina:2 , omnivideo:3 , freewifi:4 , kuaiya_lite:5 , leya:6 ,kuaiya_ios:8
SaveScreen = True  # True ， False
SaveJumpOutScreen = True  # True , False
KeepRun = True  # True (Resume run when app Crash), False (Finish run when app Crash)

#  - * Crawl model* -
TimeModel = 'Normal'  # Limit (Exp crawl in 5 minutes ) , Normal
LimitTime = '300'  # seconds . (set the crawl time)
CrawlModel = 'Normal'  # Random (crawl in random) ， Normal ， Activity (crawl all activities)
CoverageLevel = 1  # 0 < level <= 1 , Exp level = 0.6 , if there are 10 points in one page , coverage click 6 points .

#  - * Apk Install Setting * -
UnInstallApk = True  # True (uninstall app & testApp) , False
InstallApk = True  # True (install app & testApp) ,False
ApkPath = '/Users/admin/Downloads/Kuaiya-china-debug.apk'
TestApkPath = '/Users/admin/Downloads/Kuaiya-china-debug-androidTest.apk'

#  - * App Info Setting * -
AppMainActivity = 'com.dewmobile.kuaiya.act.MainActivity'
FirstClickViews = ['iv_transfer_to', 'guide_i_know', 'ok', 'edit_ok', 'button1', 'iv_back']
BackBtnViews = ['back', 'iv_title_left', 'back_iv', 'iv_btn_back', 'iv_back']  # finally tap in the page
UnClickViews = ['tips', 'tv_exchange', 'll_exchange,']
AuthorizationAlert = [['com.huawei.systemmanager', 'com.huawei.systemmanager:id/btn_allow', '允许']]

#  - * Run Init Robotium Case Setting * -
RunInitNodes = True  # True (run init nodes before run init Robotium Case) , False
RunInitCase = True  # True (run init Robotium case) , False
InitCases = ['com.dewmobile.kuaiya.test.cases.host.initcase.RunGuidePage']
TestRunner = 'com.android.test.runner.MultiDexTestRunner'

#  - * Login Setting * -
Login = False  # True (if crawl to the loginActivity, login & continue crawl)
AppLoginActivity = 'com.dewmobile.kuaiya.es.ui.activity.LoginActivity'
AccountViewID = 'username'
PasswordViewID = 'password'
LoginBtnId = 'btn_login'
Account = '15210614522'
Password = '123456'
