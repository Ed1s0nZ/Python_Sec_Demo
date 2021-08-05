# 1. 定义portscan函数，用来进行TCP 端口扫描
# 2. 启动多线程运行扫描函数

import socket
from threading import Thread
import time


# 2. 启动多线程运行扫描函数
def main(target):
    print("开始扫描: %s" % target)
    for port in range(1, 65536):
        t = Thread(target=portscan, args=(target, port))
        t.start()


# 1. 定义portscan函数，用来进行TCP 端口扫描
def portscan(target, port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target, port))
        print("[*] %s:%d 开放" % (target, port,))
        print(port)
        client.close()
    except:
        pass


if __name__ == '__main__':
    target = input("请输入IP: ")
    start = time.time()
    target = str(target)
    main(target)
    end = time.time()
    print("用时 %.2f s" % (end - start))
