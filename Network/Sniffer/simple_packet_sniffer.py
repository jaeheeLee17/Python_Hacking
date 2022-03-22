from socket import *
import os

# 호스트 패킷 스니핑
def sniffing(host):
    # 호스트 운영체제가 윈도우일 때
    if os.name == 'nt':
        socket_protocol = IPPROTO_IP
    else:
        socket_protocol = IPPROTO_ICMP
    sniffer = socket(AF_INET, SOCK_RAW, socket_protocol)
    sniffer.bind((host, 0))
    sniffer.setsockopt(IPPROTO_IP, IP_HDRINCL, 1)
    if os.name == 'nt':
        # promiscuous 모드 활성화
        sniffer.ioctl(SIO_RCVALL, RCVALL_ON)
    packet = sniffer.recvfrom(65565)
    print(packet)
    if os.name == 'nt':
        # promiscuous 모드 비활성화
        sniffer.ioctl(SIO_RCVALL, RCVALL_OFF)

def main():
    host = gethostbyname(gethostname())
    print('START SNIFFING at {}'.format(host))
    sniffing(host)

if __name__ == "__main__":
    main()