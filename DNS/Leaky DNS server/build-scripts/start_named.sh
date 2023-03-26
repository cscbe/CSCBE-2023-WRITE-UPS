#!/bin/bash

#/usr/sbin/iptables-restore < /tmp/iptables.rules

exec nohup /usr/sbin/named -f -u named -c /etc/named.conf
