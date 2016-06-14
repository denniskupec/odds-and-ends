#!/su/bin/sush
# Linux version 3.10.73-g4c64553 (inky@cyanogenmod) (gcc version 4.9.x-google 20140827 (prerelease) (GCC))

IPTABLES=/system/bin/iptables
IP=/system/bin/ip
 
cd /sdcard
 
#$IPTABLES -F
$IPTABLES -t filter -F FORWARD
$IPTABLES -t nat -F POSTROUTING
$IPTABLES -t filter -I FORWARD -j ACCEPT
$IPTABLES -t nat -I POSTROUTING -j MASQUERADE
 
# tun0 being OpenVPN
# rndis0 being RNDIS (USB) tethering
$IP rule add from 192.168.42.0/24 lookup 61
$IP route add default dev tun0 scope link table 61
$IP route add 192.168.42.0/24 dev rndis0 scope link table 61
$IP route add broadcast 255.255.255.255 dev rndis0 scope link table 61
