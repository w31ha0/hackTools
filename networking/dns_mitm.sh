iptables -t nat -A PREROUTING -i eth0 -p udp --dport 53 -j REDIRECT --to-port 53
