#-*-coding:utf-8-*-
from aip import AipOcr

""" 你的 APPID AK SK """
APP_ID = '21485125'
API_KEY = 'G0SzMnDTCLhBCaXtN9AGXszv'
SECRET_KEY = 'HM6cwhLji3cZpii8l5LGY5ZgZwQsEoWZ'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


image = get_file_content('test.jpg')

""" 如果有可选参数 """
options = {}
options.setdefault("language_type", "CHN_ENG")

""" 带参数调用通用文字识别, 图片参数为本地图片 """
result = client.basicGeneral(image, options)
print(result)
