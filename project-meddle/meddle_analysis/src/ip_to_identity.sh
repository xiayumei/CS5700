#!/bin/bash
#This script takes an IP address and spits out an IP -> Identity mapping
echo "Reading from file $1" 1>&2

outpath=`dirname $1`
orgmapfile=orgmap.txt
while read line;
do
    ip=`echo $line | cut -d\  -f1`
    count=`echo $line| cut -d\  -f2`
    echo "querying IP address: $ip"
    ipinfo=`whois $ip | grep -E "OrgName|netname" | sed 's/   *//g' | cut -d: -f2`
    orgname=`echo $ipinfo | head -n1`
    if [[ ("$orgname" == *Asia*Centre*) || ("$orgname" == "") ]]; then
        orgname=`echo $ipinfo | tail -n1`
    fi
    if [ "$orgname" = "" ]; then orgname=$ip; fi
    echo "$orgname<->$count" >> $outpath/$orgmapfile
done < "$1"

echo "sorting $outpath/$orgmapfile"
