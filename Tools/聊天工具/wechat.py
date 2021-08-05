# 1. 编写usage函数
# 2. 利用getopt模块从命令行获取参数
# 3. 区分客户端、服务端
# 4. 利用多线程定义全双工客户端
# 5. 利用多线程定义全双工服务端
# 6. 定义接收数据函数、发送数据函数
import socket
import sys
import getopt
import time
from threading import Thread

class wechat:
    # 4. 利用多线程定义全双工客户端
    def wechat_client(self, target, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target, port))
        print("[*] try to connect the target...")
        response = client.recv(1024)  # bytes
        print(response.decode())  # srt

        # 实现全双工的关键代码
        t = Thread(target=self.send_data, args=(client, ))  # 调用类里的方法要用self指定一下
        # t.setDaemon 指定当主进程结束时退出子进程
        t.setDaemon(True)
        t.start()

        c = Thread(target=self.recv_data, args=("server_>", client))
        c.setDaemon(True)
        c.start()

        try:
            time.sleep(10000)
        # except KeyboardInterrupt: 用来接收 Ctrl+c
        except KeyboardInterrupt:
            sys.exit()

    # 5. 利用多线程定义全双工服务端
    def wechat_server(self, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', port))
        server.listen(1)
        print("[*] Listening on 0.0.0.0:%d" % port)
        client_handle, addr = server.accept()
        print("[*] Accept connection from %s:%d" % (addr[0], addr[1]))
        client_handle.send(b"[*] connection successful...")

        # 实现全双工的关键代码
        t = Thread(target=self.send_data, args=(client_handle, ))
        # t.setDaemon 指定当主进程结束时退出子进程
        t.setDaemon(True)
        t.start()

        c = Thread(target=self.recv_data, args=("client_>", client_handle))
        c.setDaemon(True)
        c.start()

        try:
            time.sleep(10000)
        # except KeyboardInterrupt: 用来接收 Ctrl+c
        except KeyboardInterrupt:
            sys.exit()

    # 6. 定义接收数据函数、发送数据函数
    def send_data(self, socket):
        while True:
            data = input()  # str
            data = data.encode('utf-8')  # bytes
            socket.send(data)

    def recv_data(self, who, socket):
        while True:
            response = socket.recv(1024)  # bytes
            if response:
                response = response.decode()  # str
                print(who, response)

    # 1. 编写usage函数
    def usage(self):
        print("help info: python wechat.py -h")
        print("client: python wechat.py -t [target] -p [port]")
        print("server: python wechat.py -lp [port]")
        sys.exit()


if __name__ == "__main__":
    target = ""
    port = 0
    listen = False
    help = False
    # 2. 利用getopt模块从命令行获取参数值
    opts, args = getopt.getopt(sys.argv[1:], "t:p:lh")
    for o, a in opts:
        if o == "-t":
            target = a
        elif o == "-p":
            port = int(a)
        elif o == "-l":
            listen = True
        elif o == "-h":
            help = True
        else:
            assert False, "Unhandled Option"

    test = wechat()  # 新建一个test对象
    if help:
        test.usage()
    # 3. 区分客户端、服务端
    elif not listen:
        test.wechat_client(target, port)
    else:
        test.wechat_server(port)
