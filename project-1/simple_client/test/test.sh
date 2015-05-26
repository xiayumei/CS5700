#!/bin/bash

RED='\e[0;31m'
GREEN='\e[0;32m'
NOC='\e[0m'

COUNT=1
NUIDS=(001176107 001954575)
PORTS=(27993 27994)
HOST=cs5700.ccs.neu.edu

SEARCH_PATH=`pwd | xargs dirname`
TARGET=`find $SEARCH_PATH -name client`

function alerting()
{
    if [ $? -eq 0 ]; then
        echo -e " -> [${GREEN}PASS${NOC}]"
    else
        echo -e " -> [${RED}ERROR${NOC}]"
    fi
}

if [ "$TARGET" == "" ]; then
    echo -e "${RED}Please run 'make' first before running this \
script standalone or just run 'make test'${NOC}"
    exit
fi

for ((i=1; i<=$COUNT; i++))
do
    for nuid in "${NUIDS[@]}"
    do
        for port in "${PORTS[@]}"
        do
            if [ $port -eq 27993 ]; then
                echo "$i time general testing with NUID: $nuid"
                $TARGET -p $port $HOST $nuid
            else
                echo "$i time ssl testing with NUID: $nuid"
                $TARGET -p $port -s $HOST $nuid
            fi
            alerting
        done
    done
    echo ""
done

