#!/bin/sh
# updated 12/25/16

ip6tables -A INPUT -p icmpv6 --icmpv6-type router-advertisement -m hl --hl-eq 255 -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type neighbor-solicitation -m hl --hl-eq 255 -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type neighbor-advertisement -m hl --hl-eq 255 -j ACCEPT
ip6tables -A INPUT -p icmpv6 --icmpv6-type redirect -m hl --hl-eq 255 -j ACCEPT

# the basics (related/established, icmp echo, ssh)
ip6tables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
ip6tables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
ip6tables -A INPUT -p tcp -dport 22 -j ACCEPT

# nginx (http, https)
ip6tables -A INPUT -p tcp -m multiport --dports 80,443,8080 -j ACCEPT

ip6tables -A INPUT -j DROP
