from scapy.all import *
import sys


def get_MAC(interface, target_IP):
    # get the MAC address of target_IP and return it

    source_IP = get_if_addr(interface)
    source_MAC = get_if_hwaddr(interface)
    p = ARP(hwsrc=source_MAC, psrc=source_IP)  # ARP request by default

    p.hwdst = 'ff:ff:ff:ff:ff:ff'
    p.pdst = target_IP

    reply, unans = sr(p, timeout=5, verbose=0)
    if len(unans) > 0:
        # received no reply
        raise Exception('Error finding MAC for %s, try using -i' % target_IP)
    return reply[0][1].hwsrc


interface = sys.argv[1]
target = sys.argv[2]
SELF_MAC =  get_if_hwaddr(interface)    # fill in with your MAC address
TARGET_MAC = get_MAC(interface,target)
BCAST_MAC = 'ff:ff:ff:ff:ff:ff'
EMPTY_MAC = '00:00:00:00:00:00'
EMPTY_IP = '0.0.0.0'

def create_ARP_request_gratuituous(ipaddr_to_broadcast):
    arp = ARP(hwsrc=EMPTY_MAC, psrc=EMPTY_IP,hwdst=EMPTY_MAC,pdst=EMPTY_IP)
    return Ether(src=TARGET_MAC,dst=SELF_MAC) / arp

pkt = create_ARP_request_gratuituous(target)
pkt.display()
sendp(packet,iface=interface)
