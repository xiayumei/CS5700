#!/bin/bash

datapath=$1
outpath=$2
srcpath=`[ "$3" = "" ] && echo . || echo $3`
datasuffix=.pcap.enc.clr

mkdir -p $outpath
files=`find $datapath -name "*$datasuffix"`

# first grep
for file in ${files[@]};
do
    outfile=`echo $file | sed -E 's/(.*tcpdump-yuanyin-)(.*)(\.pcap\.enc\.clr)/\2.grep/g'`
    /bin/bash $srcpath/grepForStuff.sh $file 2>&1> $outpath/$outfile
done

# second grep, aggregation
grep -ivE "Looking for|\./tcpdump/2014-|lat|kugo" $outpath/* > $outpath/pii.grep
