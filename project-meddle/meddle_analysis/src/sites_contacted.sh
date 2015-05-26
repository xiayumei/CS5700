#!/bin/bash

datapath=$1
outpath=$2
srcpath=`[ "$3" = "" ] && echo . || echo $3`
datasuffix=.pcap.enc.clr
tsharkfile=tshark.dump
ipfile=ips.filtered
ipstatsfile=ipmap.txt
ipstatsfile_merged=ipmap.merged.txt
ipstatsfile_merged_sorted=ipmap.merged.sorted.txt

mkdir -p $outpath
files=`find $datapath -name "*$datasuffix"`

for file in ${files[@]};
do
    echo "processing $file"
    # get IPs
    ips=`echo $file | sed -E 's/(.*tcpdump-yuanyin-([^-]*-){6})(.*)(\.pcap\.enc\.clr)/\3/g'`
    meddle_server_ip=`echo $ips | cut -d- -f1`
    device_vpn_ip=`echo $ips | cut -d- -f2`
    device_isp_ip=`echo $ips | cut -d- -f3`
    # decompress a pcap file
    tshark -o http.decompress_body:TRUE -nlr $file -T text -V > $outpath/$tsharkfile
    # preliminary grep
    grep -iE "nternet Protocol Version.*Src: $device_vpn_ip" $outpath/$tsharkfile | cut -d, -f2,3 > $outpath/$ipfile
    # use a Python script to do stats
    python $srcpath/statsip.py $outpath/$ipfile $meddle_server_ip $device_vpn_ip $device_isp_ip $outpath $ipstatsfile
done

# merge the ip stats
echo "merging file $outpath/$ipstatsfile into $outpath/$ipstatsfile_merged"
python $srcpath/mergeipstats.py $outpath/$ipstatsfile $outpath/$ipstatsfile_merged

# sorting merged result
echo "sorting merged file $outpath/$ipstatsfile_merged into $outpath/$ipstatsfile_merged_sorted"
sort $outpath/$ipstatsfile_merged > $outpath/$ipstatsfile_merged_sorted
