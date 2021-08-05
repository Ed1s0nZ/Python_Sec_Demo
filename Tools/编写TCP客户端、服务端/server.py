# 1. 创建socket套接字
# 2. 绑定IP和端口
# 3. 进行监听
# 4. 接收发送数据
import socket


def main(target, port):
    # 1. 创建socket套接字
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. 绑定IP和端口
    server.bind((target, port))

    # 3. 进行监听
    server.listen(10)
    print("[*] Listening on %s:%d" % (target, port))

    # 4. 接收发送数据
    while True:
        client, addr = server.accept()

        print("[*] Accept from %s:%d" % (addr[0], addr[1]))
        response = client.recv(1024)
        print(response)
        client.send(b"[*] successful to connection...")
        client.close()


if __name__ == "__main__":
    target = '0.0.0.0'
    port = 4444
    main(target, port)
