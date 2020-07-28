#-*-coding:utf-8-*-

import win32gui
import win32api
import win32con
import time
import win32ui
from PIL import ImageGrab, Image
from speech import text2mp3
from pic2txt import gettxt, gettoken
from MP3play import trans_mp3_to_wav, playwave


def grabjpg(path, le, t, r, b):
    img = ImageGrab.grab((le, t, r, b))
    #print(img.size)
    #img.show()
    img.save(path, quality=90) #设置保存路径和图片格式


def getcont(HW):
    length = win32gui.SendMessage(HW, win32con.WM_GETTEXTLENGTH) + 1
    buf = win32gui.PyMakeBuffer(length)
    # 发送获取文本请求
    win32api.SendMessage(HW, win32con.WM_GETTEXT, length, buf)
    # 下面应该是将内存读取文本
    address, length = win32gui.PyGetBufferAddressAndLen(buf[:-1])
    text = win32gui.PyGetString(address, length)
    return text


def get_child_windows(parent):
    '''
    获得parent的所有子窗口句柄
     返回子窗口句柄列表
     '''
    if not parent:
        return
    hwndChildList = []
    win32gui.EnumChildWindows(parent, lambda hwndc, param: param.append(hwndc),  hwndChildList)
    return hwndChildList


def window_capture(filename, HW):
    # HW窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(HW)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    #print(w, h)
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)


classname = "WindowsForms10.Window.8.app.0.11c3e_r15_ad1"
classname1 = "WindowsForms10.Window.8.app.0.2bf8098_r15_ad1"
classname2 = "WindowsForms10.Window.8.app.0.13965fa_r9_ad1"
titlename = "TaskbarForm"


def main():
    while True:
        try:
            # 获取句柄
            #hwnd = win32gui.FindWindowEx(0, 0, classname, titlename)
            #hwnd = 3016382
            #print(win32api.GetSystemMetrics(win32con.SM_CXSCREEN))  # 获得屏幕分辨率X轴
            #print(win32api.GetSystemMetrics(win32con.SM_CYSCREEN))  # 获得屏幕分辨率Y轴
            hwnd = win32gui.FindWindow(classname, None)
            hwnd1 = win32gui.FindWindow(classname1, titlename)
            hwnd2 = win32gui.FindWindow(classname2, titlename)
            if hwnd:
                #获取窗口左上角和右下角坐标
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                #print(getcont(hwnd)) 这句有bug
                #print(left, top, right, bottom)
                # clist = get_child_windows(hwnd)
                # print(clist)

                if top <= 950 <= left and win32api.GetSystemMetrics(win32con.SM_CXSCREEN) == 1920:
                    #time.sleep(1)
                    #grabjpg('test.jpg', left, 838, right, 1048)
                    #window_capture('test.jpg', hwnd)
                    time.sleep(0.5)
                    win32api.keybd_event(win32con.VK_SNAPSHOT, 0)
                    time.sleep(0.5)
                    im = ImageGrab.grabclipboard()
                    im.save("screen.png")
                    img = Image.open('screen.png')
                    #width, height = img.size
                    # 前两个坐标点是左上角坐标
                    # 后两个坐标点是右下角坐标
                    # width在前， height在后
                    box = (left, 948, right, 1048)
                    region = img.crop(box)
                    region.save('alarm.jpg')
                    ak = gettoken()
                    gettxt('alarm.jpg', ak, 'alarm.txt')
                    text2mp3('alarm.txt', 'alarm.mp3')
                    trans_mp3_to_wav('alarm.mp3', 'alarm.wav')
                    playwave('alarm.wav')
                    time.sleep(2)
                elif top <= 900 <= left and win32api.GetSystemMetrics(win32con.SM_CXSCREEN) == 1280:
                    time.sleep(0.5)
                    win32api.keybd_event(win32con.VK_SNAPSHOT, 0)
                    time.sleep(0.5)
                    im = ImageGrab.grabclipboard()
                    im.save("screen.png")
                    img = Image.open('screen.png')
                    #width, height = img.size
                    # 前两个坐标点是左上角坐标
                    # 后两个坐标点是右下角坐标
                    # width在前， height在后
                    box = (left, 884, right, 984)
                    region = img.crop(box)
                    region.save('alarm.jpg')
                    #grabjpg('test.jpg', left, 774, right, 984)
                    # window_capture('test.jpg', hwnd)
                    ak = gettoken()
                    gettxt('alarm.jpg', ak, 'alarm.txt')
                    text2mp3('alarm.txt', 'alarm.mp3')
                    trans_mp3_to_wav('alarm.mp3', 'alarm.wav')
                    playwave('alarm.wav')
                    time.sleep(2)
                elif top <= 580 <= left and win32api.GetSystemMetrics(win32con.SM_CXSCREEN) == 1366:
                    time.sleep(0.5)
                    win32api.keybd_event(win32con.VK_SNAPSHOT, 0)
                    time.sleep(0.5)
                    im = ImageGrab.grabclipboard()
                    im.save("screen.png")
                    img = Image.open('screen.png')
                    #width, height = img.size
                    # 前两个坐标点是左上角坐标
                    # 后两个坐标点是右下角坐标
                    # width在前， height在后
                    box = (left, 628, right, 728)
                    region = img.crop(box)
                    region.save('alarm.jpg')
                    #grabjpg('test.jpg', left, 774, right, 984)
                    # window_capture('test.jpg', hwnd)
                    ak = gettoken()
                    gettxt('alarm.jpg', ak, 'alarm.txt')
                    text2mp3('alarm.txt', 'alarm.mp3')
                    trans_mp3_to_wav('alarm.mp3', 'alarm.wav')
                    playwave('alarm.wav')
                    time.sleep(2)
                else:
                    print('小播工作中...')
                    time.sleep(2)
                    continue

            elif hwnd1 or hwnd2:
                #获取窗口左上角和右下角坐标
                left, top, right, bottom = win32gui.GetWindowRect(hwnd1 if hwnd1 else hwnd2)
                #print(getcont(hwnd)) 这句有bug
                #print(left, top, right, bottom)
                # clist = get_child_windows(hwnd)
                # print(clist)

                if top <= 900 and win32api.GetSystemMetrics(win32con.SM_CXSCREEN) == 1920:
                    grabjpg('test.jpg', left, 838, right, 1048)
                    #window_capture('test.jpg', hwnd)
                    ak = gettoken()
                    gettxt('test.jpg', ak, 'test.txt')
                    text2mp3('test.txt', 's1.mp3')
                    trans_mp3_to_wav('s1.mp3', 's1.wav')
                    playwave('s1.wav')
                    time.sleep(2)
                elif top <= 835 and win32api.GetSystemMetrics(win32con.SM_CXSCREEN) == 1280:
                    grabjpg('test.jpg', left, 774, right, 984)
                    # window_capture('test.jpg', hwnd)
                    ak = gettoken()
                    gettxt('test.jpg', ak, 'test.txt')
                    text2mp3('test.txt', 's1.mp3')
                    trans_mp3_to_wav('s1.mp3', 's1.wav')
                    playwave('s1.wav')
                    time.sleep(2)
                elif top <= 580 and win32api.GetSystemMetrics(win32con.SM_CXSCREEN) == 1366:
                    grabjpg('test.jpg', left, 518, right, 728)
                    # window_capture('test.jpg', hwnd)
                    ak = gettoken()
                    gettxt('test.jpg', ak, 'test.txt')
                    text2mp3('test.txt', 's1.mp3')
                    trans_mp3_to_wav('s1.mp3', 's1.wav')
                    playwave('s1.wav')
                    time.sleep(2)
            else:
                print('小播工作中....')
                time.sleep(2)

        except BaseException as e:
            #print("未找到目标窗口")
            print(e)
            time.sleep(2)


if __name__ == '__main__':
    main()


