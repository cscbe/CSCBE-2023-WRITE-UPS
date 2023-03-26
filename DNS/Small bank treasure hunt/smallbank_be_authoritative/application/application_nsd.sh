#!/bin/bash
#We want
#1) logging to local file
#2) logging to stderror so docker logs work
#3) Logging for config parse errors



#Advantage for -g of over -f is that config parse errors are logged to stderr
#Disadvantage of -g is that nothing is logged to file
#So -g only complies with 2 and 3
#/usr/sbin/named -u named -g

#To satisfy req 2  use -L and -V 
#To satisfy req 1 log is configured by default in nsd.conf
#-L debug logging -V verbosity non debug logging
/usr/sbin/nsd -d -L 9 -V 9
#Enable debug
#/usr/sbin/named -u named -f -d 3
