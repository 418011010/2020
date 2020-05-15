import time
from twilio.rest import Client
from memory_profiler import profile

send_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

#  短信收发费用0.028$


@profile
def send_message():
    account_sid = 'ACd615e71b7ad5f4686943f7e716e95b0f'
    auth_token = 'xxxxx'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body="I love you.",
                         from_='+12187890888',
                         to='+8613871115289'
                     )
    print('发送时间：%s \n状态：发送成功！' % send_time)
    print('接收短信号码：'+message.to)
    print('短信内容：\n' + message.body)  # 打印短信内容
    print('短信SID：' + message.sid)  # 打印SID


#send_message()  # 调用执行函数

if __name__ == "__main__":
    send_message()

