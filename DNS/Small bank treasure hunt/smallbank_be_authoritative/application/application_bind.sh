#!/bin/bash
#We want
#1) logging to local file
#2) logging to stderror so docker logs work
#3) Logging for config parse errors



#Advantage for -g of over -f is that config parse errors are logged to stderr
#Disadvantage of -g is that nothing is logged to file
#So -g only complies with 2 and 3
#/usr/sbin/named -u named -g


#To satisfy req 3:
/usr/sbin/named-checkconf -z /etc/named.conf
#To satisfy req 2 log channel to stderr in named.conf and use -f
#To satisfy req 1 log channel to local file in named.conf
/usr/sbin/named -u named -f
#Enable debug
#/usr/sbin/named -u named -f -d 3