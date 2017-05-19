#!/bin/bash
# Start
# Configure IP address for WLAN
sudo nmcli radio wifi off
sudo rfkill unblock wlan
sudo kill `sudo lsof -t -i:53`
sudo ifconfig wlan0 192.168.10.1
# Start DHCP/DNS server
sudo service dnsmasq restart
# Enable routing
sudo sysctl net.ipv4.ip_forward=1
# Enable NAT
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
# Run access point daemon

sudo service apache2 restart
sudo service dnsmasq restart

#for captive page purposes
#sudo iptables -t mangle -N internet
#sudo iptables -t mangle -A PREROUTING -i wlan0 -p tcp -m tcp --dport 80 -j internet
#sudo iptables -t mangle -A internet -j MARK --set-mark 99
#sudo iptables -t nat -A PREROUTING -i wlan0 -p tcp -m mark --mark 99 -m tcp --dport 80 -j DNAT --to-destination 10.0.0.1

sudo hostapd -dd /etc/hostapd.conf

# Stop
# Disable NAT
sudo iptables -D POSTROUTING -t nat -o eth0 -j MASQUERADE
# Disable routing
sudo sysctl net.ipv4.ip_forward=0
# Disable DHCP/DNS server
sudo service dnsmasq stop
sudo service hostapd stop

sudo ../networking/restore_iptables.sh
