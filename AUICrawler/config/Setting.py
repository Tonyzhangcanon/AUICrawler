# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#  - * Jenkins Host * -
JenkinsHost = '127.0.0.0:8080'

#  - * Plan Setting * -
SaveScreen = True  # True ， False
SaveJumpOutScreen = True  # True , False
KeepRun = True  # True (Resume run when app Crash), False (Finish run when app Crash)

#  - * Crawl model* -
TimeModel = 'Normal'  # Limit (Exp crawl in 5 minutes ) , Normal
LimitTime = 15  # minutes . (set the crawl time)
CrawlModel = 'Normal'  # Random (crawl in random) ， Normal ， Activity (crawl all activities)
CoverageLevel = 1  # 0 < level <= 1 , Exp level = 0.6 , if there are 10 points in one page , coverage click 6 points .

#  - * Apk Install Setting * -
UnInstallApk = False  # True (uninstall app & testApp) , False
InstallApk = False  # True (install app & testApp) ,False
ApkPath = '/Users/zhangzhiyang/Downloads/zhihu_beta_1008.apk'
TestApkPath = '/Users/admin/Downloads/xxxxx-androidTest.apk'

#  - * App Info Setting * -
AppMainActivity = {'com.zhihu.android': '.app.ui.activity.MainActivity',
                   'com.xxxx.xxx': 'com.xxxx.MainActivity',
                   'packageName': 'MainActivity'}

FirstClickViews = {'com.zhihu.android': ['itext_left_func', 'snackbar_action', 'button1'],
                   'packageName': ['FirstClickView-1-id', 'FirstClickView-2-id']}

BackBtnViews = {'com.xxx.xxx': ['back', 'iv_title_left', 'back_iv', 'iv_btn_back', 'iv_back'],
                'packageName': ['View-1-id', 'View-2-id']}  # finally tap in the page

UnCrawlViews = {'com.xxxx.xxx': {'view1-id': 'id', 'view2-text': 'text'},
                'packageName': {'view1-id': 'id', 'view2-text': 'text'}}

AuthorizationAlert = [['com.huawei.systemmanager', 'com.huawei.systemmanager:id/btn_allow', '允许'],
                      ['com.google.android.packageinstaller', 'com.android.packageinstaller:id/permission_allow_button',
                       '允许']]

#  - * Run Init Robotium Case Setting * -
RunInitNodes = True  # True (run init nodes before run init Robotium Case) , False
RunInitCase = False  # True (run init Robotium case) , False
InitCases = {'com.xxxx.xxxx': ['com.xxxx.xxxx.cases.xxxx'],
             'packageName': ['case1', 'case2']}
TestRunner = 'com.android.test.runner.MultiDexTestRunner'

#  - * Login Setting * -
Login = True  # True (if crawl to the loginActivity, login & continue crawl)
AppLoginActivity = {'com.zhihu.android': '.app.ui.activity.HostActivity',
                    'packageName': 'loginActivity'}

LoginViewList = {'com.zhihu.android': ['edit_text', 'password', 'btn_progress'],
                 'packageName': ['AccountViewID', 'PasswordViewID', 'LoginBtnId']}

AccountList = {'com.zhihu.android': [['15210614522', 'www.zhiyang.net'], ['xxxxx', 'xxxxx']],
               'packageName': [['account1', 'password1'], ['account2', 'password2']]}

#  - * send crawl result email * -
SMTP_HOST = "smtp.gmail.com"  # Set mail smtp host
Failed_Mail_To_List = ["zhangzhiyang@zhihu.com"]  # who will receive the failed exception mail
Result_Mail_To_List = ["zhangzhiyang@zhihu.com"]  # who will receivr the result mail
Mail_User = "zhangzhiyang@zhihu.com"  # which account will be Use to send mail
Mail_Pass = "www.zhangzhiyang.net"  # the password for login
