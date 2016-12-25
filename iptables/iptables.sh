#!/bin/sh
# updated 12/25/16

iptables -X

iptables -P INPUT ACCEPT
iptables -P OUTPUT ACCEPT
iptables -P FORWARD ACCEPT

# allow loopback
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -i lo -j ACCEPT

# openvpn
iptables -t nat -A POSTROUTING -s 10.10.0.0/16 -o eth0 -j MASQUERADE

# the basics (related/established, icmp echo, ssh)
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A INPUT -p udp --sport 67 --dport 68 -j ACCEPT
iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
iptables -A INPUT -p tcp -dport 22 -j ACCEPT

# nginx (http, https)
iptables -A INPUT -p tcp -m multiport --dports 80,443,8080 -j ACCEPT

# teamspeak 3
iptables -A INPUT -p tcp -m multiport --dports 10011,30033 -j ACCEPT
iptables -A INPUT -p udp --dport 9987 -j ACCEPT

iptables -A INPUT -j DROP

. $HOME/bin/fw/ip6tables.sh
