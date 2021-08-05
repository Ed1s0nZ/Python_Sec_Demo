# 1. 创建socket套接字
# 2. 建立TCP 连接
# 3. 接收、发送数据
import socket


def main(target, port):
    # 1. 创建socket套接字
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 2. 建立TCP 连接
    client.connect((target, port))

    # 3. 接收、发送数据
    client.send(b"successful to connection...")
    response = client.recv(1024)
    print(response)
    client.close()


if __name__ == "__main__":
    target = "127.0.0.1"
    port = 4444
    main(target, port)
