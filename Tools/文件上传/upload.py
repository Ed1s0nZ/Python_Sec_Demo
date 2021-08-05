# 1. 首先定义usage函数
# 2. 利用getopt模块获取命令行参数
# 3. 区分客户端和服务端
# 4. 编写客户端和服务端函数
# 5. 编写文件上传函数、文件下载函数

import sys
import socket
import getopt
import time

upfile = ""


def main():
    global upfile
    help = False
    listen = False
    target = ""
    port = 0

    # 2. 利用getopt模块获取命令行参数
    opts, args = getopt.getopt(sys.argv[1:], "t:p:u:hl")
    for o, a in opts:
        if o == "-t":
            target = a
        elif o == "-p":
            port = int(a)
        elif o == "-u":
            upfile = a
        elif o == "-h":
            help = True
        elif o == "-l":
            listen = True
        else:
            assert False, "Unhandled Option"

    if help:
        usage()
    # 3. 区分客户端和服务端
    if not listen:
        client_handle(target, port)
    else:
        server_handle(port)


# 4. 编写客户端和服务端函数
# 编写client_handle
def client_handle(target, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target, port))
    client.send(upfile.encode('utf-8'))
    time.sleep(1)
    upload_file(client)
    client.close()


# 编写server_handle
def server_handle(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(10)
    print("[*] Listening on 0.0.0.0:%d" % port)
    while True:
        client_socket, addr = server.accept()
        download_file(client_socket)


# 5. 编写文件上传函数、文件下载函数
# 定义upload_file
def upload_file(client):
    f = open(upfile, 'rb')
    data = f.read()
    client.send(data)
    f.close()
    print("发送完毕")


# 定义download_file
def download_file(client_socket):
    filename = client_socket.recv(1024)
    filename = filename.decode()
    print("[*]Receive the file: %s" % filename)
    file_buffer = "".encode('utf-8')
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        else:
            file_buffer += data
    f = open(filename, 'wb')
    f.write(file_buffer)
    f.close()
    print("文件上传完成")


# 1. 首先定义usage函数
def usage():
    print("help info: python upload.py -h")
    print("client: python upload.py -t [target] -p [port] -u [uploadfile]")
    print("server: python filename.py -lp [port]")
    sys.exit()


if __name__ == '__main__':
    main()
