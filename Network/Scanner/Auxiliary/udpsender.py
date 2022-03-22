from socket import *
from netaddr import IPNetwork, IPAddress

def sendMessage(subnet, msg):
    sock = socket(AF_INET, SOCK_DGRAM)
    for ip in IPNetwork(subnet):
        try:
            print('SENDING MESSAGE to [{}]'.format(ip))
            sock.sendto(msg.encode('utf-8'), ('{}'.format(ip), 9000))
        except Exception as e:
            print(e)

def main():
    host = gethostbyname(gethostname())
    subnet = host + '/24'
    msg = 'KNOCK! KNOCK!'
    sendMessage(subnet, msg)

if __name__ == "__main__":
    main()