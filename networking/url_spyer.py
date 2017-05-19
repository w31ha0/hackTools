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
    print("[*]Usage: python url_spyer.py [network interface] [hosts to track]")
    
def http_parse(packet):
    if packet.haslayer(IP):
        ipSrc = packet.getlayer(IP).src
        if ipSrc in hostsToTrack:
            decoded = packet.sprintf("%Raw.load%").split('\\r\\n')
            if len(decoded) > 3:
                path = decoded[0].split('/')[1].split(' ')[0]
                host = decoded[1][6:]
                userAgent = decoded[2]
                url = host+"/"+path
                print ipSrc+" visited " + url
                
def main():
    print "Beginning to sniff on " + argv[1]
    print "Tracking hosts: " + str(hostsToTrack)
    while 1:
        packet = sniff(iface=argv[1], prn=http_parse,lfilter=lambda p: "GET" in str(p), filter="", count=1)[0]

if len(sys.argv) < 3:
    usage()
    exit(0)

if __name__ == '__main__':
    hostsToTrack = sys.argv[2].split(',')
    main()
