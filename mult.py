#-*-coding:utf-8-*-
import time
import random
import sys
from multiprocessing import Process

#多线程
def run(name):
    print('%s running' % name)
    time.sleep(random.randrange(2, 6))
    print('%s running end' % name)


# 必须加,号
p1 = Process(target=run, args=('anne',))
p2 = Process(target=run, args=('alice',))
p3 = Process(target=run, args=('bb',))
p4 = Process(target=run, args=('hh',))


def main():
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    time.sleep(1)
    p1.terminate()
    print('主线程')


if __name__ == '__main__':
    main()


