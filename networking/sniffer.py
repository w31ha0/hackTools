#!/usr/bin/env python
# This code is strictly for demonstration purposes.
# If used in any other way or for any other purposes. In no way am I responsible
# for your actions or any damage which may occur as a result of its usage
# dnsSpoof.py
# Author: Nik Alleyne - nikalleyne at gmail dot com
# http://securitynik.blogspot.com

from sys import argv, exit
from scapy.all import *
from binascii import hexlify


def usage():
    print("[*]Usage: python sniffer.py [network interface] [file with keywords]")
    
def scan(packet):
    if packet.haslayer(ARP):
    	packet.display()
    return
    string = str(packet).lower()
    for keyword in keywords:
        keyword = keyword.strip()
        if string.find(keyword) != -1:
            print string
            return
                
def main():
    print "Beginning to sniff on " + argv[1]
    print "Loaded keywords " + str(keywords)
    while 1:
        packet = sniff(iface=argv[1], prn=scan, filter="", count=1)[0]

if len(sys.argv) < 3:
    usage()
    exit(0)

if __name__ == '__main__':
    file = sys.argv[2]
    with open(file) as f:
        keywords = f.readlines()
    main()
