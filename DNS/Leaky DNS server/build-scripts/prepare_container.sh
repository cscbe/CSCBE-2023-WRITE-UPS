#!/bin/bash

cd /etc/yum.repos.d/

sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

echo "minrate=1" >> /etc/yum.conf
echo "timeout=300" >> /etc/yum.conf
yum -y install net-tools epel-release less bind bind-utils iptables

#iptables -I INPUT -p tcp --dport 53 -m string --hex-string "|0000FF0001|" --algo bm --from 52 -j DROP
#iptables -I INPUT -p udp --dport 53 -m string --hex-string "|0000FF0001|" --algo bm --from 40 -j DROP
#iptables-restore < /tmp/iptables.rules