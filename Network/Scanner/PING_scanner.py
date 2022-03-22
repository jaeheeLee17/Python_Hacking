from socket import *
import os
import struct

# IP 헤더 데이터 파싱
def parse_ipheader(data):
    ipheader = struct.unpack('!BBHHHBBH4s4s', data[:20])
    return ipheader

# IP 데이터그램 크기 출력
def getDatagramSize(ipheader):
    return ipheader[2]

# 프로토콜 정보 출력
def getProtocol(ipheader):
    protocols = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
    proto = ipheader[6]
    if proto in protocols:
        return protocols[proto]
    else:
        return 'OTHERS'

# IP 정보 출력
def getIP(ipheader):
    src_ip = inet_ntoa(ipheader[8])
    dest_ip = inet_ntoa(ipheader[9])
    return (src_ip, dest_ip)

# IP 헤더 길이 출력
def getIPHeaderLen(ipheader):
    ipheaderlen = ipheader[0] & 0x0F
    ipheaderlen *= 4
    return ipheaderlen

# ICMP 메시지 유형 출력
def getTypeCode(icmp):
    icmpheader = struct.unpack('!BB', icmp[:2])
    icmp_type = icmpheader[0]
    icmp_code = icmpheader[1]
    return (icmp_type, icmp_code)

# 소켓으로부터 데이터 수신
def recvData(sock):
    data = ''
    try:
        data = sock.recvfrom(65565)
    except timeout:
        data = ''
    return data[0]

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
    try:
        while True:
            data = recvData(sniffer)
            ipheader = parse_ipheader(data[:20])
            ipheaderlen = getIPHeaderLen(ipheader)
            protocol = getProtocol(ipheader)
            src_ip, dest_ip = getIP(ipheader)
            if protocol == 'ICMP':
                offset = ipheaderlen
                icmp_type, icmp_code = getTypeCode(data[offset:])
                if icmp_type == 0:
                    print('HOST ALIVE: {}'.format(src_ip))
    except KeyboardInterrupt:
        # promiscuous 모드 비활성화
        if os.name == 'nt':
            sniffer.ioctl(SIO_RCVALL, RCVALL_OFF)

def main():
    host = gethostbyname(gethostname())
    print('START SNIFFING at {}'.format(host))
    sniffing(host)

if __name__ == "__main__":
    main()