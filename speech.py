#-*-coding:utf-8-*-
from aip import AipSpeech

APP_ID = "21438044"
API_KEY = "Tqbhwi5ccGciepEL2T2hvTpL"
SECRET_KEY = "GIsK6S8LudsHGidFHo5HvezKg5ri4ujL"


def text2mp3(text, mp3):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    with open(text, 'rb') as g:
        t = g.read()
    #textfile = "中新网7月20日电 据国家卫健委网站消息，7月19日0—24时，31个省(自治区、直辖市)和新疆生产建设兵团报告新增确诊病例22例，其中境外输入病例5例(四川3例，内蒙古1例，山东1例)，本土病例17例(均在新疆)；无新增死亡病例；新增疑似病例1例，为境外输入病例(在上海)。当日新增治愈出院病例24例，解除医学观察的密切接触者465人，重症病例较前一日增加2例。"
    res = client.synthesis(t, "zh", 1,
                           {
                               "vlo": 5,
                               "spd": 4,
                               "pit": 8,
                               "per": 4
                           }
                           )

    with open(mp3, "wb") as f:
        f.write(res)


#text2mp3('test.txt', 's1.mp3')
