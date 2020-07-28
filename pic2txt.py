#-*-coding:utf-8-*-

import requests
import base64

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
            #print(outlist)
            out = []
            for i in outlist:
                out.append(i['words'])
            print(out)
            out = str(out).encode()

            with open(OUTPUT, "wb") as f:
                f.write(out)
    else:
        print('图片超出限制')
        err = '图片超出限制'.encode()
        with open(OUTPUT, "wb") as f:
            f.write(err)


def gettoken():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=G0SzMnDTCLhBCaXtN9AGXszv&client_secret=HM6cwhLji3cZpii8l5LGY5ZgZwQsEoWZ'
    response = requests.get(host)
    if response:
        dic = response.json()
        return dic['access_token']


if __name__ == "__main__":
    ak = gettoken()
    #print(ak)
    gettxt('test.jpg', ak, 'test.txt')


