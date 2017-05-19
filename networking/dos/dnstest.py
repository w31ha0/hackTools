from scapy.all import *
from sys import argv

q="isc.org"
dns = "192.168.8.2"
packet = Ether(dst="11:11:11:11")/(IP(src='192.168.8.1',dst=dns)/UDP(sport=RandShort())/DNS(id=1000,rd=1,qd=DNSQR(qname=q,qtype="ALL"), ar=DNSRROPT(rclass=4096)))
packet.display()
sendp(packet,iface=sys.argv[1].strip(), count=1,verbose=0)

