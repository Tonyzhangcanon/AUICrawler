# -*- coding:utf-8 -*-
from config import Setting


def mack_crawl_result_html(plan, app):
    if Setting.CrawlModel == "Activity":
        crawlModel = u"Activity遍历"
    elif Setting.CrawlModel == "Normal":
        crawlModel = u"按序遍历"
    elif Setting.CrawlModel == "Random":
        crawlModel = u"随机遍历"
    if Setting.TimeModel == "Limit":
        timeModel = "                   <span style ='color: green;'>\n" \
                    "                   " + u"是" + \
                    "\n                   </span>\n"
    else:
        timeModel = "                   <span style ='color: red;'>\n" \
                    "                   " + u"否" + \
                    "\n                   </span>\n"
    if Setting.UnInstallApk:
        reInstallApk = "                   <span style ='color: green;'>\n" \
                       "                   " + u"是" + \
                       "\n                   </span>\n"
    else:
        reInstallApk = "                   <span style ='color: red;'>\n" \
                       "                   " + u"否" + \
                       "\n                   </span>\n"
    if Setting.SaveScreen:
        saveScreen = "                   <span style ='color: green;'>\n" \
                     "                   " + u"是" + \
                     "\n                   </span>\n"
    else:
        saveScreen = "                   <span style ='color: red;'>\n" \
                     "                   " + u"否" + \
                     "\n                   </span>\n"
    if Setting.KeepRun:
        keepRun = "                   <span style ='color: green;'>\n" \
                  "                   " + u"是" + \
                  "\n                   </span>\n"
    else:
        keepRun = "                   <span style ='color: red;'>\n" \
                  "                   " + u"否" + \
                  "\n                   </span>\n"
    if Setting.RunInitNodes:
        runInitNodes = "                   <span style ='color: green;'>\n" \
                       "                   " + u"是" + \
                       "\n                   </span>\n"
    else:
        runInitNodes = "                   <span style ='color: red;'>\n" \
                       "                   " + u"否" + \
                       "\n                   </span>\n"
    if Setting.RunInitCase:
        runInitCase = "                   <span style ='color: green;'>\n" \
                      "                   " + u"是" + \
                      "\n                   </span>\n"
    else:
        runInitCase = "                   <span style ='color: red;'>\n" \
                      "                   " + u"否" + \
                      "\n                   </span>\n"
    if Setting.Login:
        login = "                   <span style ='color: green;'>\n" \
                "                   " + u"是" + \
                "\n                   </span>\n"
    else:
        login = "                   <span style ='color: red;'>\n" \
                "                   " + u"否" + \
                "\n                   </span>\n"

    html_head = "<!DOCTYPE html public '-//W3C//DTD HTML 4.01 Transitional//EN'>\n" + "<html>\n" + "<head>\n" + \
           "    <META http-equiv='Content-Type' content='text/html; charset=UTF-8'>\n" + \
           "    <title>Crawl Test Results</title>\n" + "</head>\n"
    table = "<TABLE Align='center' width=1000px>\n" \
            "    <TR>\n" \
            "        <TD Align='center'>\n" \
            "         <span style='font-family:微软雅黑;font-size:30px;font-weight:normal;font-style:normal;text-decoration:none;color:#2674a6;'><strong>自动遍历测试报告</strong></span>\n" \
            "        </TD>\n" \
            "    </TR>\n" \
            "</table>\n" \
            "<div>\n" \
            "   <hr size=\"1\" width=\"90%\">\n" \
            "    <TABLE Align='center' class=\"details\"  border=0 cellpadding=5 cellspacing=2 width=85%>\n" \
            "        <tr>\n" \
            "            <td>\n" \
            "            <h1 style = font-size:15px;>测试结果</h1>\n" \
            "            </td>\n" \
            "            <Td colspan=\"6\"></Td>\n" \
            "        </tr>\n" \
            "        <tr valign=\"top\">\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                设备数量\n" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                通过\n" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                异常" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                开始时间" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                结束时间" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                执行Log" \
            "            </th>\n" \
            "        </tr>\n" \
            "       <tr valign=\"top\" class=\"Failure\">\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + plan.deviceNum + "</td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\"><span style =\"color: green;\">" + str(plan.passedDevice) + "</span></td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\"><span style =\"color: red;\">" + str(plan.failedDevice) + "</span></td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + str(plan.runCaseTime) + "</td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + str(plan.endTime) + "</td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">\n" \
            "               <a href=" + plan.logPath + "/CrawlerLog.txt" + ">\n" \
            "                   " + "CrawlerLog" + \
            "\n               </a>\n" \
            "            </td>\n" \
            "        </tr>\n" \
            "    </table>\n" \
            "    <TABLE Align='center' class=\"details\"  border=0 cellpadding=5 cellspacing=2 width=85%>\n" \
            "        <tr>\n" \
            "            <td>\n" \
            "            <h1 style = font-size:15px;>执行设置</h1>\n" \
            "            </td>\n" \
            "            <Td colspan=\"6\"></Td>\n" \
            "        </tr>\n" \
            "        <tr valign=\"top\">\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                执行模式\n" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                覆盖程度\n" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                是否限时" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                重新安装" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                是否截图" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                崩溃重启" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                初始化遍历" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                执行初始化Case" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                遍历中登录" \
            "            </th>\n" \
            "        </tr>\n" \
            "       <tr valign=\"top\" class=\"Failure\">\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + \
                            crawlModel + \
            "            </td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + \
                            str(Setting.CoverageLevel) + \
            "            </td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + \
                            timeModel + \
            "            </td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + \
                            reInstallApk + \
            "            </td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + \
                            saveScreen + \
            "            </td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + \
                            keepRun + \
            "            </td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + \
                            runInitNodes + \
            "            </td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + \
                            runInitCase + \
            "            </td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + \
                            login + \
            "            </td>\n" \
            "        </tr>\n" \
            "    </table>\n" \
            "    <TABLE Align='center' class=\"details\"  border=0 cellpadding=5 cellspacing=2 width=85%>\n" \
            "        <tr>\n" \
            "            <td>\n" \
            "            <h1 style = font-size:15px;>被测App</h1>\n" \
            "            </td>\n" \
            "            <Td colspan=\"6\"></Td>\n" \
            "        </tr>\n" \
            "        <tr valign=\"top\">\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                应用名称\n" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                版本名称\n" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                版本号" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                包名" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                Activity总数" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                安装包位置" \
            "            </th>\n" \
            "        </tr>\n" \
            "       <tr valign=\"top\" class=\"Failure\">\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + app.appName + "</td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + app.versionName + "</td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + app.versionCode + "</td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + app.packageName + "</td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + app.activityNum + "</td>\n" \
            "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + app.apkPath + "</td>\n" \
            "        </tr>\n" \
            "    </table>\n" \
            "    <TABLE Align='center' class=\"details\"  border=0 cellpadding=5 cellspacing=2 width=85%>\n" \
            "        <tr>\n" \
            "            <td>\n" \
            "            <h1 style = font-size:15px;>详细结果</h1>\n" \
            "            </td>\n" \
            "            <Td colspan=\"6\"></Td>\n" \
            "        </tr>\n" \
            "        <tr valign=\"top\">\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                设备名\n" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                设备ID\n" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                系统版本\n" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                覆盖Act数" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                Act覆盖率" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                操作控件数" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                遗漏控件数" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                控件覆盖率" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                异常退出" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                执行时长" \
            "            </th>\n" \
            "            <th style=\" color: #ffffff;font-weight: bold;text-align: center;background: #2674a6;white-space: nowrap;\">\n" \
            "                遍历结果" \
            "            </th>\n" \
            "        </tr>\n"
    device_result = ""
    for device in plan.deviceList:
        if device.name == device.model:
            name = device.name
        else:
            name = device.name + " " + device.model
        crawlActNum = str(len(device.hasCrawledActivities))
        actCover = str(float(crawlActNum)/float(app.activityNum))
        if len(actCover) == 3:
            actCover = actCover[2:] + "0%"
        elif len(actCover) == 4:
            actCover = actCover[2:] + "%"
            if actCover[0] == '0':
                actCover = actCover[1:]
        elif len(actCover) > 4:
            actCover = actCover[2:4] + "." + actCover[4] + "%"
            if actCover[0] == '0':
                actCover = actCover[1:]
        crawlNodeNum = str(len(device.hasCrawledNodes))
        unCrawlNodeNum = str(len(device.unCrawledNodes))
        nodesCover = str(float(crawlNodeNum)/(float(unCrawlNodeNum)+float(crawlNodeNum)))
        if len(nodesCover) == 3:
            nodesCover = nodesCover[2:] + "0%"
        elif len(nodesCover) == 4:
            nodesCover = nodesCover[2:]+"%"
            if nodesCover[0] == '0':
                nodesCover = nodesCover[1:]
        elif len(nodesCover) > 4:
            nodesCover = nodesCover[2:4] + "." + nodesCover[4] + "%"
            if nodesCover[0] == '0':
                nodesCover = nodesCover[1:]
        failedNum = str(device.failedTime)
        crawlTime = str((device.endCrawlTime - device.beginCrawlTime).seconds)
        if device.crawlStatue == "Passed":
            result = "                   <span style ='color: green;'>\n" \
                     "                   " + "Passed" + \
                     "\n                   </span>\n"
        elif device.crawlStatue == 'HasCrashed':
            result = "                   <span style ='color: red;'>\n" \
                     "                   " + "HasCrashed" + \
                     "\n                   </span>\n"
        elif device.crawlStatue == 'HasANR':
            result = "                   <span style ='color: red;'>\n" \
                     "                   " + "HasANR" + \
                     "\n                   </span>\n"
        else:
            result = "                   <span style ='color: red;'>\n" \
                     "                   " + device.crawlStatue + \
                     "\n                   </span>\n"
        result_body = "       <tr valign=\"top\" class=\"Failure\">\n" \
                      "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + name + "</td>\n" \
                      "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">\n" \
                      "                 <a href = " + device.logPath + "/" + " >\n" + \
                      "                      " + device.id + \
                      "\n                 </a>\n" \
                      "</td>\n" \
                      "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + device.version + "</td>\n" \
                      "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + crawlActNum + "</td>\n" \
                      "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + actCover + "</td>\n" \
                      "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + crawlNodeNum + "</td>\n" \
                      "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + unCrawlNodeNum + "</td>\n" \
                      "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + nodesCover + "</td>\n" \
                      "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">\n" \
                      "                 <a href = " + device.logPath + "/logcat.txt" + " >\n" + \
                      "                      " + failedNum + \
                      "\n                 </a>\n" \
                      "            </td>\n" \
                      "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">" + crawlTime + " 秒</td>\n" \
                      "            <td align=\"center\" style=\"background: #f5f5dc;white-space: nowrap;\">\n" \
                      "               <a href=" + device.logPath + "/CrawlerLog.txt" + ">\n" + \
                                        result + \
                      "               </a>\n" \
                      "            </td>\n" \
                      "       </tr>\n"
        device_result += result_body
    html_end = "        </table>\n"\
               "    </div>\n" \
               "</html>\n"
    result_html = html_head + table + device_result + html_end
    return result_html
