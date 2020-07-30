#-*-coding:utf-8-*-

import requests
import base64
from datetime import datetime

'''
通用文字识别
'''


def gettxt(PICPATH,AK,OUTPUT):
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    f = open(PICPATH, 'rb')
    img = base64.b64encode(f.read())
    #print(len(str(img)))
    if len(str(img)) < 4000000:
        params = {"image": img}
        #access_token = '[调用鉴权接口获取的token]'
        request_url = request_url + "?access_token=" + AK
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers)
        if response:
            #print(response.json())
            outlist = response.json().get('words_result')
            #print(outlist[-2:])
            out = []
            for i in outlist:
                out.append(i['words'])
            #print(out[-2:])
            if len(out) == 0 or out[0] in ['处理成功', '9.2', '2']:
                with open(OUTPUT, "wb") as f:
                    f.write(''.encode())
            else:
                print(out[-2:])
                out = str(out[-2:]).encode()
                with open(OUTPUT, "wb") as f:
                    f.write(out)
    else:
        print('图片超出限制')
        err = '图片超出限制'.encode()
        with open(OUTPUT, "wb") as f:
            f.write(err)


# def gettoken():
#     # client_id 为官网获取的AK， client_secret 为官网获取的SK
#     host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=&client_secret='
#     response = requests.get(host)
#     #dt = datetime.now()
#     #first = int(dt.timestamp())
#
#     if response:
#         dic = response.json()
#         print(dic)
#         return dic['access_token']

def gettoken():
    try:
        with open('token', "rb") as f:
            cc = f.read()
        c1 = str(cc, 'utf-8')
        #print(c1)
        c2 = eval(c1)
        #print(type(c2))
        dt = datetime.now()
        now = int(dt.timestamp())
        if now - c2['gettime'] <= 2500000:
            return c2['access_token']
        else:
            host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=&client_secret='
            response = requests.get(host)
            dt = datetime.now()
            gettime = int(dt.timestamp())
            # print(gettime)
            if response:
                dic = response.json()
                dic['gettime'] = gettime

                with open('token', "wb") as f:
                    f.write(str(dic).encode())
                return dic['access_token']
    except FileNotFoundError as e:
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=&client_secret='
        response = requests.get(host)
        dt = datetime.now()
        gettime = int(dt.timestamp())
        #print(gettime)
        if response:
            dic = response.json()
            dic['gettime'] = gettime

            with open('token', "wb") as f:
                f.write(str(dic).encode())
            return dic['access_token']


if __name__ == "__main__":
    ak = gettoken()
    #print(ak)
    gettxt('alarmS.jpg', ak, 'test.txt')


