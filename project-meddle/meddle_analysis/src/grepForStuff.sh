#!/bin/bash

filename="$1"

tcpdump -Ar $filename| grep -v 'TCP' | grep -v 'HTTP' | grep -v 'seq' > httpdata.txt
echo $filename

echo "-Looking for lat=, latitude="
egrep -io "[^a-zA-Z]?lat([^a-zA-Z]|itude).*[0-9]+(\.?)[0-9]+" httpdata.txt | sort | uniq -c

echo "Looking for phone specific things"
#phone-specific searches
grep -i "013334003608401" httpdata.txt | sort | uniq -c
grep -i "355031040753366" httpdata.txt | sort | uniq -c
grep -iE "robinsyuan|yingq.yuan@gmail.com|robins1990@sina.com" httpdata.txt | sort| uniq -c
grep -iE "dummy stuff here" httpdata.txt | sort | uniq -c

#contact info (phone specific)
# grep -i "[strings in your contacts list]" httpdata.txt | sort | uniq -c
grep -iE "857[^0-9]*210[^0-9]*4593" httpdata.txt | sort | uniq -c

echo " Looking for phone number, also phone=, number=  "
egrep -io "[^a-zA-Z]?number[^a-zA-Z]?([:=])+(\"?).........." httpdata.txt | sort | uniq -c
egrep -io "[^a-zA-Z]?phone[^a-zA-Z]?([:=])+(\"?)........." httpdata.txt | sort | uniq -c

echo " Looking for credit card numbers "
egrep -io '4[0-9]{12}(?:[0-9]{3})?' httpdata.txt | sort  | uniq -c #Visa
egrep -io '5[1-5][0-9]{14}' httpdata.txt | sort | uniq -c #MasterCard
egrep -io '[47][0-9]{13}' httpdata.txt | sort | uniq -c #AmEx
egrep -io '3(?:0[0-5]|[68][0-9])[0-9]{11}' httpdata.txt | sort | uniq -c #DinersClub
egrep -io '6(?:011|5[0-9]{2})[0-9]{12}' httpdata.txt | sort | uniq -c #Discover
egrep -io '(?:2131|1800|35\d{3})\d{11}' httpdata.txt | sort | uniq -c #JCB

echo "Looking for email addresses"
egrep -io "[^ ]+@([a-z]+\.)+(((com)|(org))|((edu)|(net)))" httpdata.txt
