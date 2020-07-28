#-*-coding:utf-8-*-
import time
import json
import requests
params = {
    'g':Course,
    'm':Player,
    'a':record
}
data = {
    'course_id': (None, 188),
    'lesson_id': (None, 2628),
    'end_time': (None, 400),
    'request_id': (None, 'a805fc6a22cd9fb0c4cc65848982da10')
}

URL = 'https://www.hbskills.org.cn/index.php'
resp = requests.post(URL, files=data, params=params,
                     verify=False, timeout=10)

print(resp.status_code)
print(resp.request.url)
print(resp.request.body)
print(resp.text)

