#!/bin/bash
#This script should be run on a base centos image
#Demo file should not use in production should import known trusted rpm keys


BASEPATH="$(cd $(dirname "${BASH_SOURCE[0]}");pwd)"
cd "$BASEPATH"

yum -y install epel-release 
yum -y install bind bind-utils nsd

ZONE="smallbank.be"
ZONEFOLDER=${ZONE}


#ephemeral config
cp -vf "$BASEPATH"/nsd.conf /etc/nsd/


#Dnssec config
install -d  -o nsd -g nsd -Z nsd_zone_t /etc/nsd/primary/${ZONEFOLDER}/
install -o nsd -g nsd -Z nsd_zone_t "$BASEPATH"/${ZONEFOLDER}.zone.unsigned /etc/nsd/primary/${ZONEFOLDER}/
install -d -o named -g named -Z named_cache_t /var/named/dynamic/${ZONEFOLDER}/keys

#Create ZSK
#dnssec-keygen -r /dev/urandom -a RSASHA256 -b 1024 -3 -K "/var/named/dynamic/${ZONEFOLDER}/keys/" $ZONE
#Create KSK dummy key
#dnssec-keygen -r /dev/urandom -a RSASHA256 -b 2048 -3 -K "/var/named/dynamic/${ZONEFOLDER}/keys/" -fk $ZONE
cp -vr "$BASEPATH"/keys/* /var/named/dynamic/${ZONEFOLDER}/keys/


chown -Rv named. /var/named/dynamic/${ZONEFOLDER}/keys/


#Do not sign, to prevent zone walking
cp -v /etc/nsd/primary/${ZONEFOLDER}/${ZONEFOLDER}.zone.unsigned /etc/nsd/primary/${ZONEFOLDER}/${ZONEFOLDER}.zone 
# SIGVALIDITYNORMAL=10000
# SIGVALIDITYNORMALSEC=$(( ${SIGVALIDITYNORMAL} * 24 * 3600 ))
# dnssec-signzone -v 3 -S -K /var/named/dynamic/${ZONEFOLDER}/keys/ -x -T 86400 -a -o $ZONE -3 1A4E9B6C -H 5 -A -X now+3456000 -e now+${SIGVALIDITYNORMALSEC} -j 259200 -I text -O text -f /etc/nsd/primary/${ZONEFOLDER}/${ZONEFOLDER}.zone /etc/nsd/primary/${ZONEFOLDER}/${ZONEFOLDER}.zone.unsigned


