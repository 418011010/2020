#-*-coding:utf-8-*-
import urllib.request
from urllib.request import urlopen
import re
import random
import time
import datetime
from dateutil.relativedelta import relativedelta
import mysql.connector
import sys
import json
import pyocr
import importlib
from collections import Counter
from pdfminer.pdfparser import  PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
from tqdm import tqdm
importlib.reload(sys)

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
    randdom_header = random.choice(headers)
    req = urllib.request.Request(url)
    req.add_header("Upgrade-Insecure-Requests", 1)
    req.add_header("User-Agent", randdom_header)
    req.add_header("GET", url)
    content = urllib.request.urlopen(req,timeout=second).read()
    return content.decode(encoding="utf-8")


def ppddff(URL, J):
    pdf0 = urlopen(URL)

    # 创建一个与文档关联的解析器

    parser = PDFParser(pdf0)

    # 创建一个PDF文档对象

    doc = PDFDocument()

    # 连接两者

    parser.set_document(doc)

    doc.set_parser(parser)

    # 初始化
    doc.initialize('')

    # 创建PDF资源管理器

    resources = PDFResourceManager()

    # 创建参数分析器

    laparam = LAParams()

    # 创建一个聚合器，并接收资源管理器，参数分析器作为参数

    device = PDFPageAggregator(resources, laparams=laparam)

    # 创建一个页面解释器

    interpreter = PDFPageInterpreter(resources, device)

    for page in doc.get_pages():

        # 使用页面解释器读取页面

        interpreter.process_page(page)

        # 使用聚合器读取页面页面内容

        layout = device.get_result()

        for out in layout:

            if hasattr(out, 'get_text'):  # 因为文档中不只有text文本

                txt = out.get_text()
                # print(type(txt))

                result = re.findall(r'双[杀击]', txt)
                # result = re.findall(r'双[杀击]', txt)
                if result:
                    print('\n' + str(result))
                    print(J)
                    print(URL)
                    with open('pdfreader.txt', 'a', encoding='utf-8') as f:
                        f.write('\n' + str(result) + '\n' + J + '\n' + URL)


def main():
    time1 = time.time()
    print(time.asctime(time.localtime(time1)))
    urlf = []
    for n in range(1, 10):
        urlf.append('http://reportapi.eastmoney.com/report/list?cb=datatable9813778&industryCode=*&pageSize=50&industry=*&rating=&ratingChange=&beginTime=2018-05-14&endTime=2020-05-14&pageNo={0}&fields=&qType=0&orgCode=&code=*&rcode=&_=1589466697703'.format(n))

    pbar = tqdm(urlf)
    for u in pbar:
        pbar.set_description("processing %s" % u[170:171])
        try:
            datas = get_content(u, my_headers, 30)
            #print('网页抓取成功')
            #print(datas)
            res = re.findall(r'"encodeUrl":"(.*?)"', datas)
            reslist = list(res)
            #print(reslist)
            #print(len(reslist))
            urllist = []
            for i in reslist:
                #print(type(i))
                urllist.append("http://data.eastmoney.com/report/zw_stock.jshtml?encodeUrl=" + str(i))

            #print(urllist)
            # uu = ['http://data.eastmoney.com/report/zw_stock.jshtml?encodeUrl=VGz4HJkVhdZud3DDbeo2N1caUHZ6ZrN4dCUGLSqIoWQ=', 'http://data.eastmoney.com/report/zw_stock.jshtml?encodeUrl=VGz4HJkVhdZud3DDbeo2N9IkpjKNngi6DIRfnXYTI2I=']
            for j in urllist:
                dd = get_content(j, my_headers, 30)
                r = re.findall(r'"attachUrl":"(.*?)"', dd)
                # print(r[0])
                ppddff(r[0], j)

        except Exception as e:
            print('网页打开异常', str(e))
        finally:
            time2 = time.time()
            print(time.asctime(time.localtime(time2)))


if __name__ == '__main__':
    main()
