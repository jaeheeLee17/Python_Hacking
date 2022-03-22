from scapy.all import *
from scapy.layers.inet import IP, ICMP


def ipSpoof(srcip, dstip):
    ip_packet = IP(src=srcip, dst=dstip) / ICMP()
    print(ip_packet.show())
    send(ip_packet)

def main():
    srcip = '192.168.0.6'
    dstip = '192.168.0.3'
    ipSpoof(srcip, dstip)
    print('SENT SPOOFED IP [{}] to [{}}]'.format(srcip, dstip))

if __name__ == "__main__":
    main()