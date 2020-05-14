#-*-coding:utf-8-*-
import urllib.request
import re
import random
import time
import datetime
from dateutil.relativedelta import relativedelta
import mysql.connector
import sys

#url1 = 'http://www.google.com'
url1 = 'http://www.weather.com.cn/weather/101200101.shtml'
url2 = 'http://www.tianqi.com/wuhan/7/'
#url2 = 'http://www.baidu.com'
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]


def get_content(url, headers,second):
    '''
    @获取403禁止访问的网页
    '''
    randdom_header = random.choice(headers)

    req = urllib.request.Request(url)

    #req.add_header("Host", "blog.csdn.net")
    #req.add_header("Referer", "http://www.weather.com.cn/weather/101200101.shtml")
    req.add_header("Upgrade-Insecure-Requests", 1)
    req.add_header("User-Agent", randdom_header)
    req.add_header("GET", url)

    content = urllib.request.urlopen(req,timeout=second).read()
    return content.decode(encoding = "utf-8")
    #except Exception as e:      #抛出超时异常
    #    print('网页打开异常', str(e))
    #return content
#print(get_content(url, my_headers))
#data=bytes(get_content(url, my_headers),encoding = "utf-8")

mapdict = {'中雨': 329, '中雨转大雨': 330, '中雪': 331, '中雪转大雪': 332, '冰冻': 333, '冰雹': 334, '冻雨': 335, '多云': 336,
               '多云转晴': 337, '多云转阴': 338, '大暴雨': 339, '大暴雨转特大暴雨': 340, '大雨': 341, '大雨转暴雨': 342, '大雨转阴': 343, '大雪': 344,
               '大雪转暴雪': 345, '小雨': 346,  '阴转小雨': 346, '阴转雨': 346, '小雨转雨夹雪': 346,'小雨转中雨': 347, '小雨到中雨': 347,  '小雪': 348, '小雪转中雪': 349, '强沙尘暴': 350, '扬沙': 351, '晴': 352,
               '暴雨': 353, '暴雨转大暴雨': 354, '暴雨转晴': 355, '暴雨转阴': 356, '暴雪': 357, '沙尘暴': 358, '浮尘': 359, '特大暴雨': 360,
               '阴': 361, '阵雨': 362, '阵雪': 363, '雨夹雪': 364, '雷阵雨': 365, '雷阵雨伴有冰雹': 366, '雷阵雨转晴': 367, '雷阵雨转阴': 368,
               '雾': 369, '中到大雨': 370, '中雨转小雨': 371, '中雨转晴': 372, '多云转小雨': 373, '多云转雨夹雪': 374, '大到暴雨': 375, '小到中雨': 376,
               '小雨转多云': 377, '小雨转晴': 378, '小雨转阴': 379, '雨转阴': 379, '晴转中雨': 380, '晴转多云': 381, '晴转小雨': 382, '阴转晴': 383,'晴转阴': 383, '晴转雨夹雪': 384,
               '阴转多云': 385, '阵雨转多云': 386, '雷阵雨转中雨': 387, '雷阵雨转小雨': 388}

updatetime = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
orglist = []
try:
    datas=get_content(url1, my_headers,20)
    print('网页抓取成功')
    #print(datas)
    #res = re.findall(r'<h1345>(.*?)</i34>',datas)

    res = re.findall(r'<h1>(.*?)日.*?</h1>[\s\S]*?<big class=.*?></big>[\s\S]*?<big class=.*?></big>[\s\S]*?<p title=.*? class="wea">(.*?)</p>[\s\S]*?<p class="tem">[\s\S]*?<span>(.*?)</span>/<i>(.*?)℃</i>',datas)
    reslist = list(res)
    #查看抓取
    #print(reslist)
    if len(reslist) == 0:
        print('数据过滤失败，使用备网站抓取..')
        log6 = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '数据过滤失败，使用备网站抓取..\n'
        with open('inject.log', 'a', encoding='utf-8') as f:
            f.write(log6)
        try:
            datas2 = get_content(url2, my_headers, 20)
            print('使用备网页数据抓取成功')
            res2 = re.findall(
                r'<dl>(.*?)</dl>\n<dd class="week">.*?</dd>\n<dd class="air"><b style="background-color.*?;" title="空气质量.*?</b></dd>\n<dd class="img"><img src=".*?" /></dd>\n<dd class="temp">(.*?)</dd>\n<dd class="txt">(.*?)℃ ~ <b>(.*?)</b>℃</dd>',
                datas2)
            #print(res2)
            #orglist = []
            for i in res2:
                orglist.append(list(i))

            for o in range(len(orglist)):
                orglist[o].insert(0, '480')
                cnw = str(orglist[o][2])
                # print(mapdict[cnw])
                orglist[o][2] = str(mapdict[cnw])
                orglist[o].insert(3, str(mapdict[cnw]))
                orglist[o][1] = str(datetime.date.today() + relativedelta(days=+(o)))
                orglist[o] = orglist[o] + updatetime

            #print(orglist)

        except Exception as e:  # 抛出超时异常
            print('网页2打开异常,未能抓取数据', str(e))
            log3 = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '网页2打开异常,未能抓取数据\n' + str(e) + '\n'
            with open('inject.log', 'a', encoding='utf-8') as f:
                f.write(log3)
            sys.exit()

    else :
        print('数据过滤成功，开始导入..')

    if len(reslist[0]) == 4:

        orglist = []
        for i in reslist:
            orglist.append(list(i))

        # month=time.strftime("%Y-%m-", time.localtime())
        # month=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print (month)
        # print(updatetime)

        for o in range(len(orglist)):
            orglist[o].insert(0, '480')
            cnw = str(orglist[o][2])
            # print(mapdict[cnw])
            orglist[o][2] = str(mapdict[cnw])
            orglist[o].insert(3, str(mapdict[cnw]))
            orglist[o][4], orglist[o][5] = orglist[o][5], orglist[o][4]
            orglist[o][1] = str(datetime.date.today() + relativedelta(days=+(o + 1)))
            orglist[o] = orglist[o] + updatetime
            #print(orglist[o])


except Exception as e:      #抛出超时异常

    if len(orglist) == 0 :

        print('网页1打开异常，使用网页2抓取数据', str(e))
        log2 = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '网页1打开异常，使用网页2抓取数据\n' + str(e) + '\n'
        with open('inject.log', 'a', encoding='utf-8') as f:
            f.write(log2)
        try:
            datas2 = get_content(url2, my_headers, 20)
            print('使用备网页数据抓取成功')
            res2=re.findall(r'<dl>(.*?)</dl>\n<dd class="week">.*?</dd>\n<dd class="air"><b style="background-color.*?;" title="空气质量.*?</b></dd>\n<dd class="img"><img src=".*?" /></dd>\n<dd class="temp">(.*?)</dd>\n<dd class="txt">(.*?)℃ ~ <b>(.*?)</b>℃</dd>',datas2)
            #print(res2)
            orglist = []
            for i in res2:
                orglist.append(list(i))

            for o in range(len(orglist)):
                orglist[o].insert(0, '480')
                cnw = str(orglist[o][2])
                # print(mapdict[cnw])
                orglist[o][2] = str(mapdict[cnw])
                orglist[o].insert(3, str(mapdict[cnw]))
                orglist[o][1] = str(datetime.date.today() + relativedelta(days=+(o)))
                orglist[o] = orglist[o] + updatetime

            #print(orglist)




        except Exception as e:  # 抛出超时异常
            print('网页2打开异常,未能抓取数据', str(e))
            log3 = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '网页2打开异常,未能抓取数据\n' + str(e) + '\n'
            with open('inject.log', 'a', encoding='utf-8') as f:
                f.write(log3)
            sys.exit()




config = {
      'user': 'root',
      'password': 'coship',
      'host': '172.200.11.74',
      'database': 'vasms2',
      'charset': 'utf8',
      "connection_timeout": 20,
      "use_pure": True
}




try:
    mydb = mysql.connector.connect(**config)
except  Exception as e:

    print("数据库连接失败：" + str(e))
    log4 = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '数据库连接失败\n' + str(e) + '\n'
    with open('inject.log', 'a', encoding='utf-8') as f:
        f.write(log4)
    sys.exit()


#print(mydb)


sql = "replace INTO wfs_t_weather (cId, date,dayTid,nightTid,low,high,createTime,updateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
mycs = mydb.cursor(dictionary=True)

try:

    mycs.executemany(sql, orglist)
    mydb.commit()    # 数据表内容有更新，必须使用到该语句
    print('已更新' + str(mycs.rowcount) + '条数据')

    if __name__ == "__main__":
        print('天气数据已导入至' + str(datetime.date.today() + relativedelta(days=+6)))

    log = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '成功导入数据\n' + str(orglist) + '\n'

    with open('inject.log', 'a', encoding='utf-8') as f:
        f.write(log)

except  Exception as e:
    mydb.rollback()
    print("导入失败：" + str(e))
    log5 = (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + '导入失败\n' + str(e) + '\n'
    with open('inject.log', 'a', encoding='utf-8') as f:
        f.write(log5)
finally:
    mycs.close()
    mydb.close()
