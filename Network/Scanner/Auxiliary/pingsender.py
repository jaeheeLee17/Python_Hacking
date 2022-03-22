import os
from netaddr import IPNetwork, IPAddress
from socket import *
from threading import Thread

def sendPing(ip):
    try:
        ret = os.system('ping -n 1 {}'.format(ip));
    except Exception as e:
        print(e)

def main():
    host = gethostbyname(gethostname())
    subnet = host + '/24'
    for ip in IPNetwork(subnet):
        t = Thread(target=sendPing, args=(ip,))
        t.start()

if __name__ == "__main__":
    main()