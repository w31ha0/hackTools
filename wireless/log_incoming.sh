iptables -t nat -I PREROUTING 1 -j LOG
tail -f /var/log/messages
